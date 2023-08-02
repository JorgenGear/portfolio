#this code uses functions to grab covid related data from web json apis, then saves the data to python libraries
#the covid data is analyzed a couple different ways and displayed. Data is from all us states/territorries 

#importing libraries
import requests
import json
import time
from datetime import datetime, timedelta
import numpy as np

#creating list of territories for use in url
territorries = ['al', 'ar', 'as', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 
'ga', 'gu', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me',
'mi', 'mn', 'mo', 'mp', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 
'ny', 'oh', 'ok', 'or', 'pa', 'pr', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'va', 
'vi', 'vt', 'wa', 'wi', 'wv', 'wy']

#creating list of territory names to for use in the output
territory_names = ['Alabama', 'Arkansas', 'American Samoa', 'Arizona', 'California', 'Colorado', 'Connecticut', 'District of Columbia', 'Delaware', 'Florida', 
'Georgia', 'Guam', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 
'Michigan', 'Minnesota', 'Missouri', 'Northern Mariana Islands', 'Mississippi', 'Montana', 'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 
'New Mexico', 'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 
'Tennessee', 'Texas', 'Utah', 'Virginia', 'Virgin Islands', 'Vermont', 'Washington', 'Wisconsin', 'West Virginia', 'Wyoming']

#combining lists to connect territory code to territory name in order to output territory name while using the territory code
territory_dict = dict(zip(territorries, territory_names))

#defining keys for dictionary
posinc_key = "positiveIncrease" #New Daily Cases
date_key = "date" #Date key

#defining function for data grab
def data_grab():
    #breaking up the url to place in territory
    url_1 = "https://api.covidtracking.com/v1/states/"
    url_2 = "/daily.json"
    #for loop to piece together individual urls and grab data from each to save as individual json files
    for t in territorries:
        fil = open("/home/ubuntu/environment/hw5/" + t + ".json", "w")
        url = url_1 + t + url_2
        print(url)
        req = requests.get(url)
        rdict = json.loads(req.text)
        json.dump(rdict, fil, indent = 4)
        fil.close()
        time.sleep(1)
        
#defining function for analyzing average daily new cases for the whole set
def avg_new_cases(t):
    #creating a list for the cases and opening data
    new_daily_cases = []
    ndict = open("/home/ubuntu/environment/hw5/" + t + ".json", "r")
    lines = json.load(ndict)
    #for loop to add just the "positive increase" values to the list
    for line in lines:
        daily_cases = line[posinc_key]
        new_daily_cases.append(daily_cases)
    ndict.close()
    #turning the list into a numpy array and using numpy to find the average
    tot_new_daily = np.array(new_daily_cases)
    average_daily_cases = np.mean(tot_new_daily)
    print("The average number of new daily covid cases is:", average_daily_cases)
            

#defining function for analyzing the date with the highest number of new cases        
def highest_new_cases(t):
    #defining values and opening data
    max_inc = 0
    form_date = "Not available due to lack of information, positive increase is always represented"
    ndict = open("/home/ubuntu/environment/hw5/" + t + ".json", "r")
    lines = json.load(ndict)
    #for loop to find the highest value in 'positive increase'
    for line in lines:
        pos_inc = line[posinc_key]
        if pos_inc > max_inc:
            max_inc = pos_inc
            #grabbing the date associated with the value and converting it into a nicer format
            max_inc_date = str(line[date_key])
            max_date = datetime.strptime(max_inc_date, "%Y%m%d")
            form_date = max_date.strftime("%B %d, %Y")
    print("The date with the highest number of new COVID cases is:", form_date, "with an increase of:", max_inc)
    ndict.close()
        
#defining function for analyzing the most recent date with 0 new cases
def recent_0_cases(t):
    #defining variables and opening data
    recent_0_date = "There has never been a day without increase"
    ndict = open("/home/ubuntu/environment/hw5/" + t + ".json", "r")
    lines = json.load(ndict)
    #for loop to find the most recent date with 0 new cases
    for line in lines:
        positive_inc = line[posinc_key]
        if positive_inc == 0:
            #grabbing the date associated with the value and converting it into a nicer format
            recent_0_date = str(line[date_key])
            rec_date = datetime.strptime(recent_0_date, "%Y%m%d")
            form_date = rec_date.strftime("%B %d, %Y")
            print("The most recent date with no new COVID cases is:", form_date)
            #breaking the loop once it finds the date with 0 new cases
            break
    ndict.close()

#defining function to find the month with the highest number of new cases
def highest_month_new(t):
    #defining variables and opening data
    monthly_cases = {}
    new_case_high = 0
    ndict = open("/home/ubuntu/environment/hw5/" + t + ".json", "r")
    lines = json.load(ndict)
    #for loop to break up date into a usable dictionary key and grabbing positive increase values
    for line in lines:
        date = str(line[date_key])
        pos_inc = line[posinc_key]
        year = date[:4]
        month = date[4:6]
        #adding dates as keys in the previously defined dictionary
        if (year + "-" + month) not in monthly_cases:
            monthly_cases[year + "-" + month] = 0
        #adding each positive increase value together under their assigned month key
        monthly_cases[year + "-" + month] += pos_inc
    #finding the max of the values based on months in the dictionary
    new_case_high = max(monthly_cases.values())
    #for loop to return the key(month and year) for the max values found above
    for key in monthly_cases:
        if monthly_cases[key] == new_case_high:
            date_of_key = datetime.strptime(key, "%Y-%m")
    #if statement to account for lack of values and ties
    if list(monthly_cases.values()).count(new_case_high) > 1 and new_case_high != 0:
        print("There is a tie in months with the highest cases but one of the highest is: " + date_of_key.strftime("%B %Y"))
    elif list(monthly_cases.values()).count(new_case_high) > 2 and new_case_high == 0:
        print("There is not enough information available to calculate highest month of new cases, 'positive increase' is always represented as 0 in the data")
    else:
        print("Month with the highest new cases: " + date_of_key.strftime("%B %Y"))
    ndict.close()

#defining function to find the month with the lowest number of new cases
def lowest_month_new(t):
    #defining variables and opening data
    monthly_cases = {}
    new_case_low = 0
    ndict = open("/home/ubuntu/environment/hw5/" + t + ".json", "r")
    lines = json.load(ndict)
    #for loop to break up date into a usable dictionary key and grabbing positive increase values
    for line in lines:
        date = str(line[date_key])
        pos_inc = line[posinc_key]
        year = date[:4]
        month = date[4:6]
        #adding dates as keys in the previously defined dictionary
        if (year + "-" + month) not in monthly_cases:
            monthly_cases[year + "-" + month] = 0
        #adding each positive increase value together under their assigned month key
        monthly_cases[year + "-" + month] += pos_inc
    #finding the min of the values based on months in the dictionary
    new_case_low = min(monthly_cases.values())
    #for loop to return the key(month and year) for the min values found above
    for key in monthly_cases:
        if monthly_cases[key] == new_case_low:
            date_of_key = datetime.strptime(key, "%Y-%m")
    #if statement to account for lack of values and ties
    if list(monthly_cases.values()).count(new_case_low) > 1 and new_case_low != 0:
        print("There is a tie in months with the lowest cases but one of the lowest is: " + date_of_key.strftime("%B %Y"))
    elif list(monthly_cases.values()).count(new_case_low) > 2 and new_case_low == 0:
        print("There is not enough information available to calculate lowest month of new cases, 'positive increase' is always represented as 0 in the data")
    else:    
        print("Month with the lowest new cases: " + date_of_key.strftime("%B %Y"))
    ndict.close()


#defining function to call all analytics functions on the data excluding the initial data grab
def analyze_all_data():
    #for loop to run through all the territories
    for t in territorries:
        #outputting the actual territory names rather than the abbreviation
        territory_name = territory_dict[t]
        print(territory_name)
        #using t as the input for all functions to analyze all the data
        avg_new_cases(t)
        highest_new_cases(t)
        recent_0_cases(t)
        highest_month_new(t)
        lowest_month_new(t)
        print()
        
        

#calling the data grab function which puts all the data in their own json files
#i commented out this function call since I only needed to do it once
#data_grab()

#calling the analyze all data function to run the full analysis required for this assignment and outputting the resutls
analyze_all_data()
