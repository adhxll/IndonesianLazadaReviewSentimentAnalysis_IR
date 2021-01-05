# -*- coding: utf-8 -*-
"""IR_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15U5Vz5JSaize7LJLBsQVSA3M7kZI26I6
"""

#pip install Sastrawi

import nltk
nltk.download('punkt')
nltk.download('stopwords')
import Sastrawi
import numpy as np
import pandas as pd
import re
from nltk.tokenize import word_tokenize 
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize.treebank import TreebankWordDetokenizer as Detok
from scipy import spatial
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import confusion_matrix 
import pickle

def clean_str(string):
  """
  Tokenization/string cleaning for all datasets except for SST.
  Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
  """
  string = re.sub(r"[^A-Za-z0-9()\,!?\'\`]", " ", string)
  string = re.sub(r"[0-9!@#$&()\\-`.+,/\"]", " ", string)
  string = re.sub(r"\'s", " \'s", string)
  string = re.sub(r"\'ve", " \'ve", string)
  string = re.sub(r"n\'t", " n\'t", string)
  string = re.sub(r"\'re", " \'re", string)
  string = re.sub(r"\'d", " \'d", string)
  string = re.sub(r"\'ll", " \'ll", string)
  string = re.sub(r",", " , ", string)
  string = re.sub(r"!", " ! ", string)
  string = re.sub(r"\(", " \( ", string)
  string = re.sub(r"\)", " \) ", string)
  string = re.sub(r"\?", " \? ", string)
  string = re.sub(r"\s{2,}", " ", string)

  return string.strip().lower()

def importData(path):
  data = pd.read_csv(path)
  return data

def detokenize(string):
  detokenizer = Detok()
  temp = detokenizer.detokenize(string)
  return temp

def preprocessing(string):
  #casefolding and string cleaning
  string = clean_str(string)
  
  #tokenizing1
  string = nltk.tokenize.word_tokenize(string)

  #no need for stopwords removal because the TF-IDF will remove it
  #stopwords removal
  # listStopword =  set(nltk.corpus.stopwords.words('indonesian'))
  # removed = []
  # for s in string:
  #     if s not in listStopword:
  #         removed.append(s)
  # string = removed

  #stemming
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()

  string = [stemmer.stem(sent) for sent in string]

  #detokenizing preprocessed dataset to use as an input for TfidfVectorizer
  string = detokenize(string)

  return string


def load_train_test(x, y):
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.33, random_state=42)

    return xtrain, xtest, ytrain, ytest

if __name__ == "__main__":
  column = 'review' #change into the column name where exists the data that you want to process
  label_column = 'room' #COLUMN NAME FOR LABEL/TARGET
  
  path = '/content/drive/MyDrive/Colab Notebooks/IR/review_data.csv' #csv path

  data = importData(path)
  data[column] = [preprocessing(sent) for sent in data[column]]

  vectorizer = TfidfVectorizer(min_df = 5, max_df = 0.8)
  X = vectorizer.fit_transform(np.array(data[column]))
  xtrain, xtest, ytrain, ytest = train_test_split(X, data[label_column], test_size=0.33, random_state=42)
  model = svm.SVC(kernel='rbf')
  model.fit(xtrain, ytrain)

  prediction = model.predict(xtest)

  #accuracy and confusion matrix
  accuracy = model.score(xtest, ytest) 
  cm = confusion_matrix(ytest, prediction)
  print("accuracy:", accuracy)
  print("confusion matrix:")
  print(cm)

  #saving the model to working directory as "model.pkl
  model_filename = "model.pkl"
  vectorizer_filename = 'vectorizer.pkl'
  with open(model_filename, 'wb') as file:
    pickle.dump(model, file)

  with open(vectorizer_filename, 'wb') as file:
    pickle.dump(vectorizer, file)