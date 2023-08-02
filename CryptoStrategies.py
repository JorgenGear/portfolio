#this code using a series of functions to obtain data on 6 cryptocurrencies from web json apis, saves it to csv
#files and runs that data through two trading strategies to determine the best time to buy and sell and stores the
#results in a json file
#cryptos: Bitcoin, Ethereum, Dogecoin, Shiba Inu, Solana, Litecoin

#importing libraries
import requests
import json
import time
from datetime import datetime, timedelta

#defining variables
#breaking up url to grab specific data and defining the coins
coins = ["bitcoin", "ethereum", "dogecoin", "shiba-inu", "solana", "litecoin"]
url1 = "https://api.coingecko.com/api/v3/coins/"
url2 = "/history?date="
url3 = "$localization=false"

#defining the keys for the json api
md_key = 'market_data'
prc_key = 'current_price'
usd_key = 'usd'

#defining results library
results = {}

#defining functions for retrieving data
#defining the function to grab the inital large data sets
def initial_data_grab():
    for coin in coins:
        dt = datetime(2023, 1, 1)
        fil = open("/home/ubuntu/environment/final_project/data/" + coin + "_prices.csv", "w")
        for i in range(90):
            dt += timedelta(days=1)
            dts = dt.strftime("%d-%m-%Y")
            url = url1 + coin + url2 + dts + url3
            req = requests.get(url)
            rdict = json.loads(req.text)
            print(rdict)
            lines = []
            lines.append(dts + "," + str(rdict[md_key][prc_key][usd_key]) + "\n")
            time.sleep(5)
            fil.writelines(lines)
        fil.close()

#defining the function for appending new data to the data sets
def append_data():
    for coin in coins:
        #getting the last date from each of the csv files
        last_date = open("/home/ubuntu/environment/final_project/data/" + coin + "_prices.csv").readlines()[-1].split(",")[0]
        #print(last_date)
        #finding the difference between the last date and today
        #using strptime to convert the last_date string into a datetime object for arithmetic purposes
        ldate = datetime.strptime(last_date, "%d-%m-%Y")
        today = datetime.now()
        gap = (today - ldate).days
        print(gap, "days since", coin, "was last updated")
        dt = ldate + timedelta(days=1)
        fil = open("/home/ubuntu/environment/final_project/data/" + coin + "_prices.csv", "a")
        #looping through the defined difference in days between last_date and today to append new prices
        for i in range(gap):
            dts = dt.strftime("%d-%m-%Y")
            url = url1 + coin + url2 + dts + url3
            req = requests.get(url)
            rdict = json.loads(req.text)
            lines = []
            if dts > last_date:
                lines.append(dts + "," + str(rdict[md_key][prc_key][usd_key]) + "\n")
                time.sleep(5)
                fil.writelines(lines)
                last_date = dts
            else:
                break
            dt += timedelta(days=1)
        fil.close()

#defining functions for trading strategies
#defining function for simple moving average strategy(previously written then modified for shortselling)
def simpleMovingAverageStrategy(prices):
    total_profit = 0.0
    i = 0
    buy = 0
    sell = 0
    for price in prices:
        if i >=5:
            avg = (float(prices[i-1]) + float(prices[i-2]) + float(prices[i-3]) + float(prices[i-4]) + float(prices[i-5])) / 5
            if float(price) > avg and buy == 0:
                print("buying at: ", price)
                buy = price
                if sell != 0 and buy != 0:
                    total_profit += float(sell) - float(buy)
                sell = 0
                if price == prices[-1]: #tells you if the last price (today) is a good time to buy
                    print("buy this crypto now!")
            elif float(price) < avg and buy != 0:
                print("selling at: ", price)
                sell = price
                if sell != 0 and buy != 0:
                    total_profit += float(sell) - float(buy)
                buy = 0
                if price == prices[-1]: #tells you if the last price (today) is a good time to sell
                    print("sell this crypto now!")
            else:
                pass
        i += 1
    print("--------------------------")
    print("Total Profit: ", "$", round(total_profit,2))
    returns = round(total_profit / float(prices[0]),2)
    print("Percentage Returns: ", returns * 100, "%")
    return total_profit, returns
    
#defining function for mean reversion strategy (previously written then modified for shortselling)
def meanReversionStrategy(prices):
    i = 0
    buy = 0
    sell = 0
    total_profit = 0
    for price in prices:
        if i >= 5:
            #calculating the 5 day average
            avg = (float(prices[i-1]) + float(prices[i-2]) + float(prices[i-3]) + float(prices[i-4]) + float(prices[i-5])) / 5
            #if statement to determine whether or not to buy
            if float(price) < avg * .96 and buy == 0:
                buy = price
                print("buying at: ", price)
                if sell != 0 and buy != 0:
                    total_profit += float(sell) - float(buy)
                sell = 0
                if price == prices[-1]: #tells you if the last price (today) is a good time to buy
                    print("buy this crypto now!")
            #if statement to determine whether or not to sell
            elif float(price) > avg * 1.04 and buy != 0:
                #calculating trade profit for individual buys and total amount
                print("selling at: ", price)
                sell = price
                if sell != 0 and buy != 0:
                    total_profit += float(sell) - float(buy)
                buy = 0
                if price == prices[-1]: #tells you if the last price (today) is a good time to sell
                    print("sell this crypto now!")
            else:
                pass
    #adding to current_price to move loop through list
        i += 1
    print("--------------------------")
    print("Total Profit: ", "$", round(total_profit,2))
    returns = round(total_profit / float(prices[0]),2)
    print("Percentage Returns: ", returns * 100, "%")
    return total_profit, returns
    
    #defining the function to save results dictionary to a json file (previously written for last assignment)
def saveResults(results):
    json.dump(results, open("/home/ubuntu/environment/final_project/results.json", "w"), indent=4)
    return print("results saved")
    
    
    
#calling the functions
#initial_data_grab()
append_data()


#code to loop through and list all coin prices to run both strategies
for coin in coins:
    file = open("/home/ubuntu/environment/final_project/data/" + coin + "_prices.csv", "r")
    lines = file.readlines()
    #print(lines)
    prices = []
    for line in lines:
        #using split to get only the price not the date
        nums = line.split(",")[1]
        prices.append(nums)
        #print(prices)
    #saving the prices to the results dictionary
    results[coin + "_prices"] = prices
    #print(results)

#looping through both strategies (from hw5)
    #looping through SMA and saving results in the results dictionary
    print(coin, "Simple Moving Average Strategy Output: 2023 Data to present")
    sma_profit, sma_returns = simpleMovingAverageStrategy(prices)
    results[coin + "_sma_profit"] = round(sma_profit,2)
    #print("Profit: ", sma_profit)
    results[coin + "_sma_returns"] = round(sma_returns,2)
    #print("Returns: ", sma_returns, "%")
    print()
        
    #looping through MRS and saving results in the results dictionary
    print(coin, "Mean Reversion Strategy Output: 2023 Data to present")
    mrs_profit, mrs_returns = meanReversionStrategy(prices)
    results[coin + "_mrs_profit"] = round(mrs_profit,2)
    #print("Profit: ", mrs_profit)
    results[coin + "_mrs_returns"] = round(mrs_returns,2)
    #print("Returns: ", mrs_returns, "%")
    print()
    
    #finding the best perfroming strategy for each coin
    if sma_profit > mrs_profit:
        print(coin, "best strategy: simple moving average")
    else:
        print(coin, "best strategy: mean reversion")
    print()
    
    #calling function to save all results to json file
    saveResults(results)
    
#finding the best overall strategy
best_sma = 0
best_mrs = 0
for coin in coins:
    if results[coin + "_sma_profit"] > best_sma:
        best_sma = results[coin + "_sma_profit"]
        best_sma_coin = coin
    if results[coin + "_mrs_returns"] > best_mrs:
        best_mrs = results[coin + "_mrs_profit"]
        best_mrs_coin = coin
if best_sma > best_mrs:
    print("best overall strategy: simple moving average")
else:
    print("best overall strategy: mean reversion")
    
#code for finding the best performing code
best_coin = 0
for coin in coins:
    if results[coin + "_sma_profit"] > best_coin:
        best_coin = results[coin + "_sma_profit"]
        best_coin_name = coin
    if results[coin + "_mrs_returns"] > best_coin:
        best_coin = results[coin + "_mrs_profit"]
        best_coin_name = coin
print("best coin: ", best_coin_name)
