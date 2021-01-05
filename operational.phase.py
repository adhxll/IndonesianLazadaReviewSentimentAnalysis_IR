# -*- coding: utf-8 -*-
"""IR_project.app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XzTe1sg1wDopO5KDu7hg87EkR0kzXbAN
"""

import pickle
from train_phase import clean_str, detokenize, preprocessing

model_path = "model.pkl" #model.pkl's path
vectorizer_path = "vectorizer.pkl" 

vect = pickle.load(open(vectorizer_path,'rb'))
mod = pickle.load(open(model_path,'rb'))


print("Insert query: ")
user_input =  [input()]

#insert twitter scrapper for retrieving tweets
#returns csv file
column = 'review' #column name
data[column] = [preprocessing(sent) for sent in data[column]]

vector = vect.transform(np.array(data[column]))
pred = mod.predict(vector)

#insert method to count positive, neutral, and negative