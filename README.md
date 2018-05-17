# ChatBot
                                          
This is my implementation of google's DialogFlow Smalltalk chatbot built using tflearn built on top of Tensorflow. 

### Training Data
The training Data used is built using smalltalk in dialogflow and my own data. The data is situated inside the **Dataset** folder.
The latest dataset compiled is by the name of new-dataset.json .

The dataset is of the following format:

    {
        0:{
            "intent": "smalltalk.intentvalue",
            "inputs": ["input phrase 1", "input phrase 2"],
            "response": ["response 1", "response 2"]
            "context_set": "contextval",
            "context_filter": "required_context_val",
            "webhook": "attached webhook"
        }
        1:{
            "intent": "smalltalk.intentvalue",
            "inputs": ["input phrase 1", "input phrase 2"],
            "response": ["response 1", "response 2"]
            "context_set": "contextval",
            "context_filter": "required_context_val",
            "webhook": "attached webhook"
        }
        ...
    }

### Model Used

The current model that is used in the chatbot is DeepNeuralNetwork i.e tflearn.dnn().

### Architecture Of Chatbot

This chatbot uses a simple DNN as its brain. The data that is fed to this model is a **bag of words**. The bag of words is generated using a simple concept i.e,
it assigns '0' if the word is not present and '1' if the word is present in the input.

For eg. If the documents that we have are: 
1. This is a chatbot
2. This chatbot is built using tflearn
3. This chatbot was built for learning purpose

Here we can see that vocabulary consist of: 

['This', 'is', 'a', 'chatbot', 'built', 'using', 'tflearn', 'was', 'for', 'learning', 'purpose']

so the length of vector = number of elements in vocabulary(here 11)

so the bag of words for **"This chatbot is built using tflearn "** is: **[1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0]**

We have used **softmax** as activation function. The main advantage of using Softmax is the output probabilities range. The range will 0 to 1, and the sum of all the probabilities will be equal to one. If the softmax function used for multi-classification model it returns the probabilities of each class and the target class will have the high probability.

### Details about the files

 1. The main file is updated-chatbot.py which trains and classifies the DNN model
 2. dataset.py creates the dataset from the raw files in dataset folder
 3. intent.py contains functions to add or edit intents inside the dataset
	1. a. add_new_intent(intent): takes a whole intent as an argument and adds it to new-dataset.py
    2. edit_intent(intent, parameter, value): takes as input the value of intent to match and then updates the value if parameter is present as key else creates a new key value pair in the current intent.


