vectorization = CountVectorizer(analyzer = transform_message )
X = vectorization.fit(data['messages'])

X_transform = X.transform([data['messages']])

tfidf_transformer = TfidfTransformer().fit(X_transform)

X_tfidf = tfidf_transformer.transform(X_transform)
print(X_tfidf.shape)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 12:22:51 2021
@author: adwaitkesharwani
"""
import numpy as np
import pandas as pd
import pickle
import base64
import string
from nltk import pos_tag
import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stopwords = nltk.corpus.stopwords.words('english')
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

#---------------Functions to clean the input text--------------#

def tokenize_remove_punctuations(text):
    clean_text = []
    text = text.split(" ")
    for word in text:
        word = list(word)
        new_word = []
        for c in word:
            if c not in string.punctuation:
                new_word.append(c)
        word = "".join(new_word)
        if len(word)>0:
            clean_text.append(word)
    return clean_text
    
def remove_stopwords(text):
    clean_text = []
    for word in text:
        if word not in stopwords:
            clean_text.append(word)
    return clean_text
    
def pos_tagging(text):
    tagged = nltk.pos_tag(text)
    return tagged
            
def get_wordnet(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatize(pos_tags):
    lemmatized_text = []
    for t in pos_tags:
        word = WordNetLemmatizer().lemmatize(t[0],get_wordnet(t[1]))
        lemmatized_text.append(word)
    return lemmatized_text
        
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = tokenize_remove_punctuations(text)
    text = [word for word in text if not any(c.isdigit() for c in word)]
    text = remove_stopwords(text)
    text = [ t for t in text if len(t) > 0]
    pos_tags = pos_tagging(text)
    text = lemmatize(pos_tags)
    text = [ t for t in text if len(t)>1]
    text = " ".join(text)
    return text
        
def transform_input(text):
        text = np.array([text])
        text = pd.Series(text)
        text = clean_text(text)
        return text

#---------------Loading trained models--------------#


pickle_in = open("Pickle Files/vectorizer.pkl","rb")
vect=pickle.load(pickle_in)

pickle_in = open("Pickle Files/LinearSVC.pkl","rb")
LinearSVC = pickle.load(pickle_in)

#---------------Input--------------#

comment = st.text_input("Enter any comment"," ")
comment = clean_text(comment)
comment = np.array([comment])
comment = pd.Series(comment)
comment =vect.transform(comment)
pred = [0]# creating a list to store the output value
     

#---------------Predicting output--------------#

                
pred = model.predict(comment)
if(pred[0] == 1):
    print('prediction: {}'.format("Bullying comment!!!!"))
else:
    print('prediction: {}'.format("Normal comment."))
