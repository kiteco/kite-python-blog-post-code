"""This file will write CSV files with
   stock, crypto and other fun information!"""
import datetime
import os
from iexfinance.stocks import Stock
import requests

# Using theysaidso quote API, but
# limited to 10 requests per hour.


# QUOTE_REQ = requests.get('http://quotes.rest/qod.json')
# QUOTE_RESP = QUOTE_REQ.json()

# if 'contents' in QUOTE_RESP:
#     QUOTE = QUOTE_RESP['contents']['quotes'][0]['quote'] \
#           + " - " + QUOTE_RESP['contents']['quotes'][0]['author']
# else:
#     QUOTE = "Quote limit reached - no inspiration this time."

# print(QUOTE)



# Using FavQs API to grab qotd.
# Typically the quote changes per request.

QUOTE_REQ = requests.get('https://favqs.com/api/qotd')
QUOTE_RESP = QUOTE_REQ.json()

QUOTE = QUOTE_RESP['quote']['body'].replace(',', "&#x2c;") \
      + ' - ' + QUOTE_RESP['quote']['author']
print(QUOTE)


# Grab ETH and BTC prices in USD

BTC_PRICE_REQ = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy')
ETH_PRICE_REQ = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/buy')
LTC_PRICE_REQ = requests.get('https://api.coinbase.com/v2/prices/LTC-USD/buy')

BTC_PRICE = BTC_PRICE_REQ.json()['data']['amount']
ETH_PRICE = ETH_PRICE_REQ.json()['data']['amount']
LTC_PRICE = LTC_PRICE_REQ.json()['data']['amount']

print('BTC: $' + BTC_PRICE \
     + ' & ETH: $' + ETH_PRICE \
     + ' & LTC: $' + LTC_PRICE)

# Grab our favorite stocks and format them to String.
# The get_price() func returns a float
# This can also be done using a list of stocks.
# e.g. batch = Stock(['TSLA', 'AAPL', 'GOOGL'])

TSLA = Stock('TSLA')
AAPL = Stock('AAPL')
GOOGL = Stock('GOOGL')

TSLA_PRICE = str(TSLA.get_price())
AAPL_PRICE = str(AAPL.get_price())
GOOGL_PRICE = str(GOOGL.get_price())

print('TESLA: $' + TSLA_PRICE \
     + ' & APPLE: $' + AAPL_PRICE \
     + ' & GOOGLE: $' + GOOGL_PRICE)


# Get today's date and format it!
# One for master and the other for individual

DATE = datetime.datetime.today()

FORMATTED_FILE_DATE = DATE.strftime('%Y-%m-%d-%H-%M')
FORMATTED_MASTER_DATE = DATE.strftime('%Y-%m-%d %H:%M:%S')
FORMATTED_OUTPUT_DATE = DATE.strftime('%Y-%m-%d %H:%M')

# newline helper and formatted strings
NL = "\n"

CSV_HEADER = "TICKER,PRICE,DATE,QUOTE" + NL

FORMATTED_STOCK_STR = "TSLA," + TSLA_PRICE + ',,' + NL \
                    + "AAPL," + AAPL_PRICE + ',,' + NL \
                    + "GOOGL," + GOOGL_PRICE + ',,' + NL

FORMATTED_CRYPTO_STR = "BTC," + BTC_PRICE + ',,' + NL \
                     + "ETH," + ETH_PRICE + ',,' + NL \
                     + "LTC," + LTC_PRICE + ',,' + NL


# Write to the master CSV "a" (append) will create file
# if not already available. Also, create
# new files per script run to track individual

MASTER = open("output/master.csv", "a")

if os.stat("output/master.csv").st_size == 0:
    # only write header if file does not contain any information
    MASTER.write(CSV_HEADER)

MASTER.write(FORMATTED_STOCK_STR)
MASTER.write(FORMATTED_CRYPTO_STR)
# need a newline because we are appending
MASTER.write(',,' + FORMATTED_MASTER_DATE + ',' + QUOTE + NL)
MASTER.close()

# use FORMATTED_FILE_DATE for kebab casing
OUTPUT = open("output/individual/stock-crypto-check-" + FORMATTED_FILE_DATE + ".csv", "w")
OUTPUT.write(CSV_HEADER)
OUTPUT.write(FORMATTED_STOCK_STR)
OUTPUT.write(FORMATTED_CRYPTO_STR)
OUTPUT.write(',,' + FORMATTED_OUTPUT_DATE + ',' + QUOTE)
OUTPUT.close()
