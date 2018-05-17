# -*- coding: utf-8 -*-
"""
intent.py

This file creates and edits the intents from the dataset
"""

import json
import pandas as pd

"""
This function adds a new intent to the dataset
"""

def add_new_intent(new_intent):
    #reading the existing data
    with open('dataset/new-dataset.json') as json_data:
        existing_data = json.load(json_data)
    
    print(len(existing_data.keys()))    
    
    key=len(existing_data.keys())
        
    #adding the new intent to the last
    print("key is : "+ str(key))
    existing_data[key] = new_intent
    
    json_data = json.dumps(existing_data) 
    with open('dataset/new-dataset.json', 'w') as file:
        file.write(json_data)
      
def edit_intent(intent, parameter, value):
    with open('dataset/new-dataset.json') as json_data:
        existing_data = json.load(json_data)
    
    found = False
    
    for key in existing_data.keys():
        if existing_data[key]['intent'] == intent:
            #global found
            found = True
            print('intent found...')
            print(existing_data[key])
            existing_data[key][parameter] = value
            print('updated intent...')
            print(existing_data[key])
            
    if found is False:
        print('no such intent exist')            
    
    json_data = json.dumps(existing_data) 
    with open('dataset/new-dataset.json', 'w+') as file:
        file.write(json_data)            
                
            