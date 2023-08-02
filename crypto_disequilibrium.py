#This code will gather conversion information on 7 cryptocurrencies compared to eachother and place that data
#into a graph. Then it will traverse the graph to find all the possible pathways and compare the weights of each
#path. This will help us find disequalibrium and arbitrage opportunity.

#importing libraries that i may use
import networkx as nx
from networkx.classes.function import path_weight
import requests
import json
import time
import os
from datetime import datetime, timedelta
from itertools import permutations
from itertools import combinations

#creating a graph
g = nx.DiGraph()

#defining coins with tickers and segmenting the url for reassembly
coins = [("bitcoin", "btc"), ("ethereum", "eth"), ("ripple", "xrp"), ("cardano", "ada"), 
("bitcoin-cash", "bch"), ("eos", "eos"), ("litecoin", "ltc")]
url1 = "https://api.coingecko.com/api/v3/simple/price?ids="
url2n4 = ","
url3 = "&vs_currencies="

#function to reassemble the url for each coin/ticker in comparision to eachother. Then loading the url
#and saving the given data in a json file.
def data_grab():
    for coin1, coin2 in permutations(coins,2):
        fil = open("/home/ubuntu/environment/hw9/data/" + coin1[0] + "_to_" + coin2[0] + "exchange_rate.json", "w")
        url = url1 + coin1[0] + url2n4 + coin2[0] + url3 + coin1[1] + url2n4 + coin2[1]
        req = requests.get(url)
        rdict = json.loads(req.text)
        print(fil)
        print(rdict)
        print(url)
        time.sleep(5)
        json.dump(rdict, fil)

#data_grab()

#defining function to input the gathered data into the graph for analysis
def data_to_graph():
    for coin1, coin2 in permutations(coins,2):
        #print(coin1, coin2)
        fil = open("/home/ubuntu/environment/hw9/data/" + coin1[0] + "_to_" + coin2[0] + "exchange_rate.json", "r")
        data = json.load(fil)
        try:
            weight1 = data[coin1[0]][coin2[1]]
            weight2 = data[coin2[0]][coin1[1]]
            #print(weight1, weight2)
            g.add_weighted_edges_from([(coin1[1], coin2[1], weight1), (coin2[1], coin1[1], weight2)])
            #print(coin1[1], "to", coin2[1], "path added")
        except:
            try:
                weight_ada = data[coin1[0]][coin2[1]]
                #print(weight_ada)
                g.add_weighted_edges_from([(coin1[1], coin2[1], weight_ada)])
                #print(coin1[1], "to", coin2[1], "path added")
            except:
                pass
                #print("Cannot convert to ADA")
#data_to_graph()

#defining function to calculate the weight of each path and its reverse then multiplying them together
def find_disequalibrium():
    for coin1, coin2 in permutations(coins,2):
        print("Paths from", coin1[0], "to", coin2[0])
        paths = nx.all_simple_paths(g, source=coin1[1], target=coin2[1])
        largest = 0
        smallest = 0
        for path in paths:
            print(path)
            rev_path = path[::-1]
            print(rev_path)
            total_weight = 1
            total_weight_r = 1
            for w in range(len(path)-1):
                n1 = path[w]
                n2 = path[w + 1]
                weight = g[n1][n2]["weight"]
                if weight is not None:
                    total_weight *= weight
                    #print(total_weight)
                else:
                    pass
            try:
                for r in range(len(path)-1):
                    r1 = rev_path[r]
                    r2 = rev_path[r + 1]
                    weight_r = g[r1][r2]['weight']
                    if weight_r is not None:
                        total_weight_r *= weight_r
                    else:
                        pass
            except:
                pass
            #calculating the equalibrium number and keeping track of the smallest and largest per coin.
            e_num = total_weight * total_weight_r
            print("Path weight factor", e_num)
            if e_num > largest:
                largest = e_num
                largest_path = path, rev_path
            if smallest == 0:
                smallest = e_num
                smallest_path = path, rev_path
            elif e_num < smallest:
                smallest = e_num
                smallest_path = path, rev_path
                #time.sleep(2) #I put this here because it was crashing so if it crashes on you uncomment this
            print()
        print()
        print("Smallest path weight factor:", smallest)
        print("Corresponding (smallest) paths:", smallest_path)
        print("Greatest Paths weight factor:", largest)
        print("Corresponding (greatest) paths:", largest_path)
        print()

#find_disequalibrium()


def call_all():
    data_grab()
    data_to_graph()
    find_disequalibrium()

call_all()
