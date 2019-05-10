from sklearn import datasets, linear_model
import matplotlib.pyplot as plt

iris = datasets.load_iris()

# data and features are both numpy arrays
data = iris.data
features = iris.feature_names

# create the regression model
regression = linear_model.LinearRegression()

# Reshape the Numpy arras so that they are columnar
x_data = data[:, 2].reshape(-1, 1)
y_data = data[:, 3].reshape(-1, 1)

# Train the regression model to fit the data from iris (comparing the petal width)
regression.fit(x_data, y_data)

plt.plot(x_data, regression.predict(x_data), color='black', linewidth=3)
plt.scatter(x_data, y_data)

plt.show()