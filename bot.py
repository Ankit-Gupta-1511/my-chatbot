"""
bot.py

This file contains the main code for the chatbot aand does machine learning operations using tensorflow.
Here we use a seq2seq model to build our chatbot.
"""

#import files
import numpy as np
import tensorflow as tf
import re 
import time
import json
import nltk
import pandas as pd
import tflearn

"""
Choosing a stemmer 
"""

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

"""
Data pre processing step

loading datasets from dataset folder
"""

with open('dataset/smalltalk-intents.json') as json_data:
    intents = json.load(json_data)

#mapping input with intents
input_intent_map = pd.read_csv('dataset/smalltalk.tsv', sep='\t', header = 0)

input_intent_map = input_intent_map.drop(columns = ['Source'])       


"""
Data structure to work with intents
"""
        
words = []
classes = []
documents = []
ignore_words = ['?']

for index,intent in input_intent_map.iterrows():
    token = intent['Question']
    response = intent['Answer']
    w = nltk.word_tokenize(token)
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, response))
    # add to our classes list
    if response not in classes:
       classes.append(response)
       
# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))       


"""
creating our training dataset
"""

training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
        
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
np.random.shuffle(training)
training = np.array(training)

# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])    

"""
Building and training our model
"""

# reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')

"""
Saving the model into pickle
"""

import pickle
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )        


"""
Creating bag of word from actual user input
"""

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))
    
    
"""
creating a response structure
"""   

ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for index,intent in input_intent_map.iterrows():
                # find a tag matching the first result
                if intent['Answer'] == results[0][0]:
                    # a random response from the intent
                    key = intent['Answer']
                    return print(np.random.choice(intents[key]))

    results.pop(0)