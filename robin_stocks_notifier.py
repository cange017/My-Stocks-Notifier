# Author: Catherine Angelini
# Notification system to retrieve the real time data of the stocks a user holds and 
# send a desktop notification or text message if any of their stocks increases or falls 
# by more than set limit. It can run at any time interval (with Windows Task Scheduler 
# or Cron for Mac and Linux) 

import robin_stocks as r
import numpy as np
from win10toast import ToastNotifier
from twilio.rest import Client

# credentials
EMAIL = "[ROBINHOOD EMAIL]"
PASSWORD = "[ROBINHOOD PASSWORD]"
ACCOUNT_SID = "[TWILIO ACCOUNT SID]"
AUTH_TOKEN = "[TWILIO AUTH TOKEN]"
MY_NUMBER = "[PHONE NUMBER]"
TWILIO_NUMBER = "[TWILIO PHONE NUMBER]"

r.login(EMAIL, PASSWORD)
client = Client(ACCOUNT_SID, AUTH_TOKEN)
hr = ToastNotifier()

names = []
current_price = []                                  
close_price = []                                    
percent_change = []                                 

def stocks(my_stocks, limit):
    # calculate percent change for each stock
    for stock in my_stocks:
        names.append(stock)
        current_price.append(float(my_stocks[stock]['price']))
        close_price.append(float(r.stocks.get_stock_quote_by_symbol(stock, info=None)['previous_close']))
        percent_change = np.divide(np.subtract(current_price, close_price), close_price) * 100

    # map the stock with its percent change
    values = dict(zip(names, percent_change))

    for stock in values:
            # if percent change increased or decreased more than set amount for any of the stocks
            if abs(values[stock]) > limit:
                # Send Windows notification 
                hr.show_toast(title = stock + " stock update:", msg=str(round(values[stock], 2)) + '%', duration=20)
                # Send text message 
                client.messages.create(to=MY_NUMBER, 
                                       from_=TWILIO_NUMBER, 
                                       body=stock + " stock update: " + str(round(values[stock], 2)) + '%')

if __name__ == "__main__":
    # load stocks user owns
    my_stocks = r.account.build_holdings()

    # percent change limit
    limit = 2    
    
    stocks(my_stocks, limit)
