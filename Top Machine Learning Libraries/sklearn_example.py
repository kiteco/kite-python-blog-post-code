import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

#load dataset containing images of digits
digits=datasets.load_digits()

#print the length of the dataset
print(len(digits.data))

#input vector excluding the last item to x 
#Assign the target vector to y
x,y=digits.data[:-1], digits.target[:-1]

#Initiate Support Vector Machines for Classification
clf=svm.SVC(gamma=0.001, C=100)

#Fit the classifier instance to the model so that it learns from it
clf.fit(x,y)

#Predict what digit is in the last item of the input array 
print(clf.predict(digits.data[-1:]))

#Plot the image
plt.imshow(digits.images[-1],cmap=plt.cm.gray_r,interpolation='nearest')
plt.show()
