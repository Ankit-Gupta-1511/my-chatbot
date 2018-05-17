# -*- coding: utf-8 -*-

"""
this python file enables to change the data through gui in spyder and other IDEs.
"""

import pandas as pd
import json
#load dataset

with open('dataset/new-dataset.json') as json_data:
        existing_data = json.load(json_data)
        
"""
Change the value through gui
"""        
        
json_data = json.dumps(existing_data) 
with open('dataset/new-dataset.json', 'w+') as file:
    file.write(json_data)           