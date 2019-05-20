"""
Summary Statistics with Numpy
"""

import numpy as np

# Define a python list
a_list = [2, 4, -1, 5.5, 3.5, -2, 5, 4, 6.5, 7.5]

# Convert the list into numpy array
an_array = np.array(a_list)

# Compute and print various statistics
print('Mean:', an_array.mean())
print('Median:', np.median(an_array))
print('Range (Max - min):', np.ptp(an_array))
print('Standard deviation:', an_array.std())
print('80th percentile:', np.percentile(an_array, 80))
print('0.2-quantile:', np.quantile(an_array, 0.2))

"""
Visualization with Matplotlib and Seaborn
"""

import matplotlib.pyplot as plt

plt.plot(an_array)
plt.show()

plt.figure(figsize=(9, 5))
plt.title('A basic plot', fontsize=18)
plt.plot(an_array, color='blue', linestyle='--',
         linewidth=4, marker='o', markersize=20)
plt.xlabel('X-axis points', fontsize=14)
plt.ylabel('Y-axis points', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.show()

"""
Statsmodels
"""

import numpy as np
import statsmodels.api as sm

# Input variables
nobs = 100
X = np.random.random((nobs, 2))
X = sm.add_constant(X)

# Regression coefficients
beta = [1, .1, .5]

# Random errors
e = np.random.random(nobs)

# Output y
y = np.dot(X, beta) + e

# Fit the regression model
reg_model = sm.OLS(y, X).fit()

# Print the summary
print(reg_model.summary())
