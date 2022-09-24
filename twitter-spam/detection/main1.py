# from asyncio.windows_events import PipeServer
import numpy as np
import pandas as pd
from genpipes import declare, compose
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# input1 = "You've Won! Winning an unexpected prize sounds great, in theory"
df = pd.read_csv('/home/devilsaint/Documents/Omkar/Pipeline/SpamAndHam.csv')

import string 
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
stopwords = nltk.corpus.stopwords.words('english')

def text_process(mess):
    STOPWORDS = stopwords+ ['u', 'ü', 'ur', '4', '2', 'im', 'dont', 'doin', 'ure']
    nopunc = [char for char in mess if char not in string.punctuation]#puntuations
    nopunc = ''.join(nopunc)
    return ' '.join([word for word in nopunc.split() if word.lower() not in STOPWORDS])#stopwords

df['clean_msg'] = df.TweetText.apply(text_process)
print(df)


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





# pipe = compose.Pipeline(steps=[
#     ("tokenize_remove_punctuations", tokenize_remove_punctuations, {}),
#     ("remove_stopwords",remove_stopwords, {} ),
#     ("pos_tagging",pos_tagging, {} ),
#     ("get_wordnet",get_wordnet, {} ),
#     ("lemmatize",lemmatize, {} ),
#     ("clean_text",clean_text, {} ),
#     ("transform_input",transform_input, {} )
# ])

def clean_text(text):
    text = str(text)
    #Converting text to lower-case
    text = text.lower()
    #Tokenize and remove punctuations from the text
    text = tokenize_remove_punctuations(text)
    #Remove words containing numericals
    text = [word for word in text if not any(c.isdigit() for c in word)]
    #Remove stopwords
    text = remove_stopwords(text)
    #Remove empty tokens
    text = [ t for t in text if len(t) > 0]
    #POS tagging
    pos_tags = pos_tagging(text)
    #Lemmatize text
    text = lemmatize(pos_tags)
    #Remove words with only one letter
    text = [ t for t in text if len(t)>1]
    #Join all words
    text = " ".join(text)
    return text


df['Processed_Comment'] = df['clean_msg'].map(clean_text)
print(df)


pickle_in = open("vectorizer.pkl","rb")
vect=pickle.load(pickle_in)

from sklearn.feature_extraction.text import CountVectorizer
# count_vector = CountVectorizer()
# df = count_vector.fit_transform(df)
# df = count_vector.transform(df)

pickle_in = open("MultinomialNB.pkl","rb")
MultinomialNB = pickle.load(pickle_in)

comment = np.array(df['Processed_Comment'])
comment = pd.Series(comment)
comment =vect.transform(comment)
print(comment)
pred = MultinomialNB.predict(comment)

final_data = {'Tweet':df.TweetText, 'Survived': pred}
submission = pd.DataFrame(data=final_data)

print(submission)