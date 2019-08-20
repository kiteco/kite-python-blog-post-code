"""This file will write CSV files with
   stock, crypto and other fun information!"""
import datetime
import os
from iexfinance.stocks import Stock
import requests

# Using theysaidso quote API, but
# limited to 10 requests per hour.


# quote_req = requests.get('http://quotes.rest/qod.json')
# quote_resp = quote_req.json()

# if 'contents' in quote_resp:
#     quote = quote_resp['contents']['quotes'][0]['quote'] \
#           + " - " + quote_resp['contents']['quotes'][0]['author']
# else:
#     quote = "Quote limit reached - no inspiration this time."

# print(quote)



# Using FavQs API to grab qotd.
# Typically the quote changes per request.

quote_req = requests.get('https://favqs.com/api/qotd')
quote_resp = quote_req.json()

quote = quote_resp['quote']['body'].replace(',', "&#x2c;") \
      + ' - ' + quote_resp['quote']['author']
print(quote)


# Grab ETH and BTC prices in USD

btc_price_req = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy')
eth_price_req = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/buy')
ltc_price_req = requests.get('https://api.coinbase.com/v2/prices/LTC-USD/buy')

btc_price = btc_price_req.json()['data']['amount']
eth_price = eth_price_req.json()['data']['amount']
ltc_price = ltc_price_req.json()['data']['amount']

print('BTC: $' + btc_price \
     + ' & ETH: $' + eth_price \
     + ' & LTC: $' + ltc_price)

# Grab our favorite stocks and format them to String.
# The get_price() func returns a float
# This can also be done using a list of stocks.
# e.g. batch = Stock(['TSLA', 'AAPL', 'GOOGL'])

tsla = Stock('TSLA')
aapl = Stock('AAPL')
googl = Stock('GOOGL')

tsla_price = str(tsla.get_price())
aapl_price = str(aapl.get_price())
googl_price = str(googl.get_price())

print('TESLA: $' + tsla_price \
     + ' & APPLE: $' + aapl_price \
     + ' & GOOGLE: $' + googl_price)


# Get today's date and format it!
# One for master and the other for individual

date = datetime.datetime.today()

formatted_file_date = date.strftime('%Y-%m-%d-%H-%M')
formatted_master_date = date.strftime('%Y-%m-%d %H:%M:%S')
formatted_output_date = date.strftime('%Y-%m-%d %H:%M')

# newline helper and formatted strings
nl = "\n"

csv_header = "TICKER,PRICE,DATE,QUOTE" + nl

formatted_stock_str = "TSLA," + tsla_price + ',,' + nl \
                    + "AAPL," + aapl_price + ',,' + nl \
                    + "GOOGL," + googl_price + ',,' + nl

formatted_crypto_str = "BTC," + btc_price + ',,' + nl \
                     + "ETH," + eth_price + ',,' + nl \
                     + "LTC," + ltc_price + ',,' + nl


# Write to the master CSV "a" (append) will create file
# if not already available. Also, create
# new files per script run to track individual

master = open("output/master.csv", "a")

if os.stat("output/master.csv").st_size == 0:
    # only write header if file does not contain any information
    master.write(csv_header)

master.write(formatted_stock_str)
master.write(formatted_crypto_str)
# need a newline because we are appending
master.write(',,' + formatted_master_date + ',' + quote + nl)
master.close()

# use formatted_file_date for kebab casing
output = open("output/individual/stock-crypto-check-" + formatted_file_date + ".csv", "w")
output.write(csv_header)
output.write(formatted_stock_str)
output.write(formatted_crypto_str)
output.write(',,' + formatted_output_date + ',' + quote)
output.close()
