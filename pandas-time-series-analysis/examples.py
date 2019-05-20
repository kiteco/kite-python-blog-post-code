# Importing required modules
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# Settings for pretty nice plots
plt.style.use('fivethirtyeight')
plt.show()

# Reading in the data
data = pd.read_csv('amazon_stock.csv')

# Inspecting the data
data.head()

# Remove the first two columns
data.drop(columns=['None', 'ticker'], inplace=True)
data.head()
data.info()

# Convert str to datetime
data['Date'] = data['Date'].apply(pd.to_datetime)
data.info()

# Set 'Date' as index
data.set_index('Date', inplace=True)
data.head()

# Plot the adjusted close
data['Adj_Close'].plot(figsize=(16, 8), title='Adjusted Closing Price')

"""
Dates and Times in Pandas
"""

from datetime import datetime

my_year = 2019
my_month = 4
my_day = 21
my_hour = 10
my_minute = 5
my_second = 30

test_date = datetime(my_year, my_month, my_day)
test_date

# Output
# datetime.datetime(2019, 4, 21, 0, 0)

test_date = datetime(my_year, my_month, my_day, my_hour, my_minute, my_second)
print("The day is : ", test_date.day)
print("The hour is : ", test_date.hour)
print("The month is : ", test_date.month)

# Index column is of type DatetimeIndex
data.info()

print(data.index.max())
print(data.index.min())

# Retrieve index of earliest and latest dates
data.index.argmin()
data.index.argmax()

"""
Time Resampling
"""
# Resample by year
data.resample(rule='A').mean()

# Plot charts for specific columns
data['Adj_Close'].resample('A').mean().plot(kind='bar', figsize=(10, 4))
plt.title('Yearly Mean Adj Close Price for Amazon')
plt.show()

"""
Time Shifting
"""

data.shift(1).head()
data.shift(-1).head()

# Using string value parameters
data.tshift(periods=3, freq='M').head()

"""
Rolling Windows
"""

data['Adj_Close'].plot(figsize=(16, 8))

data.rolling(7).mean().head(10)

data['Open'].plot()
data.rolling(window=30).mean()['Open'].plot(figsize=(16, 6))
