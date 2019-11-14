#!/usr/bin/env python
# coding: utf-8
import os
import re
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import BatchNormalization, Conv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense
from tensorflow.keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import accuracy_score, classification_report, roc_curve, auc, balanced_accuracy_score, \
    confusion_matrix, roc_auc_score
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.keras import balanced_batch_generator
from scipy import interp
from imutils import paths

# Move images (Unless images already moved)
campfire_df = pd.read_csv('dataset/campfire_subset.csv')
images = list(paths.list_images('dataset/'))

# for img_path in images:
#     obj_id = int(img_path.strip('dataset/OBJID_').strip('.tif'))
#     if obj_id in campfire_df.OBJECTID.values:
#         damage = campfire_df.loc[campfire_df.OBJECTID == obj_id].iloc[0].DAMAGE
#         os.rename('dataset/OBJID_{}.tif'.format(obj_id), 'dataset/{0}/OBJID_{1}.tif'.format(damage, obj_id))
#     else:
#         os.rename('dataset/OBJID_{}.tif'.format(obj_id), 'dataset/Unburned (0%)/OBJID_{}.tif'.format(obj_id))

# Settings

EPOCHS = 50
INIT_LR = 1e-3
BS = 16
IMAGE_DIMS = (128, 128, 3)


# Create Dataset

def create_dataset(path, width, height, resample=None, random_state=0):
    """
    Converts a dataset of images in the directory structure {CLASS_LABEL}/{FILENAME}.{IMAGE_EXTENSION} 
    to list of 3D NumPy arrays and their corresponding labels. Images resized to (width, height). Dataset 
    is resampled to balance class distribution based on resample='over'|'under'.
    # Arguments
        path: path to dataset 
        width: width of resized image 
        height: height of resized image 
        (optional) resample: resample dataset using ROS('over')/RUS('under')
    # Returns
        data: A list of 3D NumPy arrays converted from images 
        labels: A list of labels of the images 
    """
    image_paths = list(paths.list_images(path))
    labels = [image_path.split(os.path.sep)[-2] for image_path in image_paths]

    if resample:
        if resample == 'over':
            sampler = RandomOverSampler(random_state=random_state)
        elif resample == 'under':
            sampler = RandomUnderSampler(random_state=random_state)
        image_paths = [[image_path] for image_path in image_paths]
        image_paths_resampled, labels = sampler.fit_resample(image_paths, labels)
        image_paths = image_paths_resampled.ravel()

    data = [img_to_array(load_img(img_path, target_size=(width, height))) for img_path in image_paths]

    return np.array(data, dtype="float") / 255.0, np.array(labels)


data, labels = create_dataset('dataset/', IMAGE_DIMS[0], IMAGE_DIMS[1])

np.save('dataset/data.npy', data)
np.save('dataset/labels.npy', labels)

# Load Dataset

data, labels = np.load('dataset/data.npy'), np.load('dataset/labels.npy')

classes = np.unique(labels)
n_classes = len(classes)

labels

fig, axs = plt.subplots(2, 3)
axs = axs.flatten()
fig.set_size_inches((8, 8))
for i, c in enumerate(classes):
    axs[i].imshow(data[labels == c][np.random.choice(data[labels == c].shape[0], 1)[0]])
    axs[i].set_title(c)
fig.delaxes(axs[5])
fig.delaxes(axs[4])
for ax in axs:
    ax.label_outer()

# explicitly call the chart
plt.show()

# Create Training/Testing Data

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=0, stratify=labels)

Counter(y_train)

Counter(y_test)


def class_distribution(arr):
    total = sum(Counter(arr).values())
    return {c: c_count / total for c, c_count in Counter(arr).items()}


class_distribution(y_train)

class_distribution(y_test)

lb = LabelBinarizer()
y_train_bin = lb.fit_transform(y_train)
y_test_bin = lb.transform(y_test)


# Model Building and Configuration


class MiniVGGNet:

    def __init__(self, name, input_shape, n_classes, init_lr, epochs, batch_size):
        self.model = MiniVGGNet.build(input_shape=input_shape, n_classes=n_classes)
        self.epochs = epochs
        self.batch_size = batch_size
        opt = Adam(lr=init_lr, decay=init_lr / epochs)
        self.model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
        model_filepath = 'model_checkpoints/{}/model.h5'.format(name)
        mcp_save = ModelCheckpoint(model_filepath, save_best_only=True, monitor='val_loss', mode='min')
        csv_logger = CSVLogger('model_checkpoints/{}/log.csv'.format(name))
        self.callbacks = [mcp_save, csv_logger]

    def fit(self, X_train, y_train, X_test, y_test):
        return self.model.fit(
            X_train,
            y_train,
            batch_size=self.batch_size,
            validation_data=(X_test, y_test),
            epochs=self.epochs,
            callbacks=self.callbacks)

    def fit_generator(self, X_train, y_train, X_test, y_test, generator, steps_per_epoch):
        return self.model.fit_generator(
            generator,
            validation_data=(X_test, y_test),
            epochs=self.epochs,
            steps_per_epoch=steps_per_epoch,
            callbacks=self.callbacks)

    @staticmethod
    def build(input_shape, n_classes):
        model = Sequential()

        model.add(Conv2D(64, (3, 3), padding="same", input_shape=input_shape, data_format='channels_last'))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(256, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Conv2D(256, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        model.add(Dense(n_classes))
        model.add(Activation("softmax"))

        return model


# Model Fitting

baseline = MiniVGGNet('baseline', IMAGE_DIMS, n_classes, INIT_LR, EPOCHS, BS)

# takes some time to run, depending on hardware (resume here)
baseline.fit(X_train, y_train_bin, X_test, y_test_bin)

ros = MiniVGGNet('baseline_ros', IMAGE_DIMS, n_classes, INIT_LR, EPOCHS, BS)

# ValueError: Found array with dim 4. Estimator expected <= 2.
ros_generator, steps_per_epoch_ros = balanced_batch_generator(
    X_train,
    y_train_bin,
    sampler=RandomOverSampler(),
    batch_size=BS,
    random_state=0)

ros.fit_generator(X_train, y_train_bin, X_test, y_test_bin, ros_generator, steps_per_epoch_ros)

img_datagen = MiniVGGNet('baseline_datagen', IMAGE_DIMS, n_classes, INIT_LR, EPOCHS, BS)

img_data_generator = ImageDataGenerator(
    rotation_range=25,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest")

img_datagen.fit_generator(X_train, y_train_bin, X_test, y_test_bin,
                          img_data_generator.flow(X_train, y_train_bin, batch_size=BS), X_train.shape[0] // BS)

# ## Model Evaluation 


model = load_model('model_checkpoints/baseline_datagen/model.h5')

y_test_pred = model.predict(X_test)

y_test_pred_labels = np.argmax(y_test_pred, axis=-1)
y_test_labels = np.argmax(y_test_bin, axis=-1)

y_test_pred_bin = []
for l in y_test_pred_labels:
    pred_bin = [0] * n_classes
    pred_bin[l] = 1
    y_test_pred_bin.append(pred_bin)
y_test_pred_bin = np.array(y_test_pred_bin)

accuracy_score(y_test_labels, y_test_pred_labels)

balanced_accuracy_score(y_test_labels, y_test_pred_labels)

print(classification_report(y_test_labels, y_test_pred_labels, target_names=classes))


def plot_confusion_matrix(y_true, y_pred, classes, normalize=False, title=None, cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


class_names = [re.sub(r' ?\([^)]+\)', '', c) for c in classes]

ax = plot_confusion_matrix(y_test_labels, y_test_pred_labels, np.array(class_names), normalize=True,
                           title='Datagen Model Confusion Matrix')
plt.savefig('datagen_conf_matrix.png')
plt.show()

# Compute ROC curve and ROC area for each class
fpr, tpr, roc_auc = {}, {}, {}
for i, c in enumerate(class_names):
    fpr[c], tpr[c], _ = roc_curve(y_test_bin[:, i], y_test_pred_bin[:, i])
    roc_auc[c] = auc(fpr[c], tpr[c])

# Compute micro-average ROC curve and ROC area
fpr['micro'], tpr['micro'], _ = roc_curve(y_test_bin.ravel(), y_test_pred_bin.ravel())
roc_auc['micro'] = auc(fpr['micro'], tpr['micro'])

# Compute macro-average ROC curve and ROC area
lw = 2

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[c] for c in class_names]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for c in class_names:
    mean_tpr += interp(all_fpr, fpr[c], tpr[c])

# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()
plt.plot(fpr["micro"], tpr["micro"],
         label='micro-average (area = {0:0.2f})'
               ''.format(roc_auc["micro"]),
         color='deeppink', linestyle=':', linewidth=4)

plt.plot(fpr["macro"], tpr["macro"],
         label='macro-average (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         color='navy', linestyle=':', linewidth=4)

colors = ['aqua', 'darkorange', 'cornflowerblue', 'purple', 'green']
for c, color in zip(class_names, colors):
    plt.plot(fpr[c], tpr[c], color=color, lw=lw,
             label='{0} (area = {1:0.2f})'
                   ''.format(c, roc_auc[c]))

plt.plot([0, 1], [0, 1], 'k--', lw=lw)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Datagen Multiclass ROC/AUC')
plt.legend(loc="lower right")
plt.savefig('datagen_roc_auc.png')
plt.show()


# Extras


def get_class_weights(y):
    counter = Counter(y)
    majority = max(counter.values())
    return {cls: float(majority / count) for cls, count in counter.items()}


class_weights_train = get_class_weights(labels)
