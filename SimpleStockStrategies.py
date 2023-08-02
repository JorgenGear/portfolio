#This code will run the stock prices through mean reversion strategy and simple moving average strategy
#It will determine the best time to buy and sell each stock based on the strategies used
#The results of each strategy will be saved in a "results" dictionary and saved in a json file

#importing json to save results dictionary to a json file
import json

#defining mean reversion strategy funcion to use on all the stock prices
def meanReversionStrategy(prices):
    current_price = 0
    buy = 0
    first_buy = 0
    total_profit = 0
    for price in prices:
        if current_price >= 5:
            #calculating the 5 day average
            five_day_average = (prices[current_price-1] + prices[current_price-2] + prices[current_price-3] + prices[current_price-4] + prices[current_price-5]) / 5
            #if statement to determine whether or not to buy
            if price < five_day_average * .96 and buy == 0:
                buy = price
                print("buying at: ", price)
                #updating the first_buy variable
                if first_buy == 0:
                    first_buy = price
            #if statement to determine whether or not to sell
            elif price > five_day_average * 1.04 and buy != 0:
                #calculating trade profit for individual buys and total amount
                trade_profit = price - buy
                total_profit += round(trade_profit, 2)
                print("selling at: ", price)
                print("trade profit: ", round(trade_profit,2))
                buy = 0
            else:
                pass
    #adding to current_price to move loop through list
        current_price += 1
    print("--------------------------")
    print("Total Profit: ", total_profit)
    print("First buy: ", first_buy)
    returns = round(total_profit / first_buy,2)
    print("Percentage Returns: ", returns, "%")
    return total_profit, returns

#defining the function that will be used to calculate simple moving average strategy
def simpleMovingAverageStrategy(prices):
    total_profit = 0
    i = 0
    buy = 0
    first_buy = 0
    for price in prices:
        if i >= 5:
            avg = (prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5
            if price < avg and buy == 0:
                print("buying at: ", price)
                buy = price
                if first_buy == 0:
                    first_buy = price
            elif price > avg and buy != 0:
                print("selling at: ", price)
                trade_profit = price - buy
                print("trade profit: ", round(trade_profit,2))
                total_profit += round(trade_profit,2)
                buy = 0
            else:
                pass
        i += 1
    print("--------------------------")
    print("Total Profit: ", total_profit)
    print("First buy: ", first_buy)
    returns = round(total_profit / first_buy, 2)
    print("Percentage Returns: ", returns, "%")
    return total_profit, returns
    
#defining the function to save the results dictionary into a json file
def saveResults(results):
    json.dump(results, open("/home/ubuntu/environment/hw5/results.json", "w"), indent=4)
    return print("results saved")

#Defining the tickers to find the txt files
tickers = ["AAPL", "ADBE", "ADSK", "AMD", "GOOG", "HOOD", "IBM", "META", "MSFT", "NVDA"]
results = {}

#code to loop all prices in each ticker through both strategies defined in the functions
for ticker in tickers:
    file = open("/home/ubuntu/environment/hw5/" + ticker + ".txt", "r")
    lines = file.readlines()
    #print("lines: ", lines)
    prices = []
    for line in lines:
        prices.append(round(float(line),2))
    results[ticker + "_prices"] = prices
    #print("prices: ", prices)
    
    #looping through SMA and saving results in the results dictionary
    print(ticker, "Simple Moving Average Strategy Output: 2022 Data")
    sma_profit, sma_returns = simpleMovingAverageStrategy(prices)
    results[ticker + "_sma_profit"] = round(sma_profit,2)
    #print("Profit: ", sma_profit)
    results[ticker + "_sma_returns"] = round(sma_returns,2)
    #print("Returns: ", sma_returns, "%")
    print()
        
    #looping through MRS and saving results in the results dictionary
    print(ticker, "Mean Reversion Strategy Output: 2022 Data")
    mrs_profit, mrs_returns = meanReversionStrategy(prices)
    results[ticker + "_mrs_profit"] = round(mrs_profit,2)
    #print("Profit: ", mrs_profit)
    results[ticker + "_mrs_returns"] = round(mrs_returns,2)
    #print("Returns: ", mrs_returns, "%")
    print()
    
    #saving the results to a json file using the previously defined function
    saveResults(results)
