# -*- coding: utf-8 -*-

"""
This files helps in creating the required dataset for the chatbot
"""

import json
import pandas as pd

#loading intent to reponse map
with open('dataset/smalltalk-intents.json') as json_data:
    intents = json.load(json_data)

#loading input to intent map    
input_intent_map = pd.read_csv('dataset/smalltalk.tsv', sep='\t', header = 0)

#dropping source column
input_intent_map = input_intent_map.drop(columns = ['Source'])

input_intent_map_grouped = input_intent_map.groupby('Question')

#writing the input-intent-response to a single file

required_data = {}
key = 0
for intent in intents.keys():
    data ={}
    data['intent'] = intent
    data['inputs'] = []
    data['response'] = intents[str(intent)] 
    for index,inputs in input_intent_map.loc[input_intent_map['Answer'] == intent].iterrows():
        data['inputs'].append(inputs['Question'])
    required_data[key] = data
    key = key+1
    
json_data = json.dumps(required_data)    
with open('dataset/dataset.json', 'w') as f:
       f.write(json_data)
            
with open('dataset/dataset.json') as json_data:
    intents = json.load(json_data)            
     
