import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.svm import SVC


def train_SVM(df):
    # select the feature columns
    X = df.loc[:, df.columns != 'label']
    # select the label column
    y = df.label

    # train an SVM with linear kernel
    clf = SVC(kernel='linear')
    clf.fit(X, y)

    return clf


def plot_svm_boundary(clf, df, title):
    fig, ax = plt.subplots()
    X0, X1 = df.iloc[:, 0], df.iloc[:, 1]

    x_min, x_max = X0.min() - 1, X0.max() + 1
    y_min, y_max = X1.min() - 1, X1.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    ax.scatter(X0, X1, c=df.label, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
    ax.set_ylabel('y')
    ax.set_xlabel('x')
    ax.set_title(title)
    plt.show()
