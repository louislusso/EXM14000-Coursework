# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:31:47 2021

@author: louis
"""
import csv
local_filename = 'Data.csv'
def extract_local_data(local_filename):
    covid_local_data =[]
    f = open(local_filename, "r")
    next(csv.reader(f))
    for lines in csv.reader(f):
        covid_local_data.append(lines)

    return(covid_local_data)

def process_local_data(covid_local_data):
    local_last_7_days = 0
    days = 0 
    for rows in covid_local_data:
        if days == 7:
            break
        if not rows[6]:
            days=days+1
            continue
        else:
            print(rows[3])
            days = days+1
            local_last_7_days = local_last_7_days + int(rows[3])
    print(local_last_7_days)        
    





def update_local_covid_data():
    
    


