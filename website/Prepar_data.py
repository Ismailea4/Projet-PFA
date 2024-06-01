import pandas as pd     # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np      # linear algebra
import matplotlib.pylab as plt

import re #used for Regular Expression 
import string
from collections import defaultdict

from collections import Counter
from datetime import datetime


from sklearn.feature_extraction.text import CountVectorizer

import nltk
#from nltk.tokenize import regexp_tokenize, word_tokenize, TweetTokenizer
from nltk.corpus import stopwords # import English stopwords
#from nltk.stem import PorterStemmer
#from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

stopwords = set(stopwords.words('english'))


import spacy

from textblob import TextBlob


def convert_to_date(date_str):
    try:
        # Essayer de convertir en utilisant le format 1
        return datetime.strptime(date_str, "%b %d, %Y · %I:%M %p %Z")
    except ValueError:
        try:
            # Essayer de convertir en utilisant le format 2
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            # Gérer le cas où la chaîne n'est dans aucun des formats attendus
            print(f"Format de date non reconnu: {date_str}")
            return None

def columns_date(df):
    df['Date'] = df['Date'].apply(convert_to_date)
    df['Year']=df['Date'].dt.year
    df['Month']=df['Date'].dt.month
    df['Day']=df['Date'].dt.day
    df = df.drop('Date',axis=1)

# Remove all emojis, replace by EMOJI
def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Remove @ and mention, replace by USER
def remove_mention(text):
    at=re.compile(r'@\S+')
    return at.sub(r'',text)


# Remove numbers, replace it by NUMBER
def remove_number(text):
    num = re.compile(r'[-+]?[.\d]*[\d]+[:,.\d]*')
    return num.sub(r'', text)


# Remove all URLs, replace by URL
def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'',text)


# Factorize repeated punctuation, add REPEAT
def remove_repeat_punct(text):
    rep = re.compile(r'([!?.]){2,}')
    return rep.sub(r'\1', text)


# Factorize elongated words, add ELONG
def remove_elongated_words(text):
    rep = re.compile(r'\b(\S*?)([a-z])\2{2,}\b')
    return rep.sub(r'\1\2', text)


# Remove words in capslock, add ALLCAPS
def remove_allcaps(text):
    caps = re.compile(r'([^a-z0-9()<>\'`\-]){2,}')
    return caps.sub(r'', text)


# Remove all english stopwords
def remove_stopwords(text):
    text = ' '.join([word for word in text.split() if word not in (stopwords)])
    return text


# Remove all punctuations
def remove_all_punct(text):
    table = str.maketrans('','',string.punctuation)
    return text.translate(table)


# Remove punctuations
def remove_punct(text):
    punctuations = '@#!?+&*[]-%.:/();$=><|{}^' + "'`" 
    for p in punctuations:
        text = text.replace(p, f' {p} ')

    text = text.replace('...', ' ... ')
    if '...' not in text:
        text = text.replace('..', ' ... ')   
    return text

# Remove non printable characters
def remove_not_ASCII(text):
    text = ''.join([word for word in text if word in string.printable])
    return text


words_model = ['israeli','israelis','lsrael','endisraelsgenocide','palestinian','palestinians','gazaunderattack']
model_language = {'israel':['israeli','israelis','lsrael','endisraelsgenocide'],
                  'palestine':['palestinian','palestinians'],
                 'gaza':['gazaunderattack']}

def clean_lemma(text):
    data = text.split(' ')
    n=len(data)
    i=0
    while i < n:
        if len(data[i])<=2:
            data.pop(i)
            n-=1
        elif data[i] in words_model:
            for key,value in model_language.items():
                if data[i] in value:
                    data[i]=key
                    i+=1
                    break
        else:
            i+=1
    text = ' '.join(data)
    return text

nlp = spacy.load('en_core_web_md')

def lemmatizing2(text):
    # Process the text using spaCy
    doc = nlp(text)

    # Extract lemmatized tokens
    lemmatized_tokens = [token.lemma_ for token in doc]

    # Join the lemmatized tokens into a sentence
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text

# Clean text
def clean_tweet(text):
    
    # Remove non text
    text = remove_URL(text)      #remove links
    text = remove_not_ASCII(text)      #remove nonsense character
    
    # Lower text, replace abbreviations
    text = text.lower()          #replace all word to lower
    text = remove_mention(text)  #remove @--
    text = remove_number(text)   #remove numbers
    
    # Remove emojis / smileys
    text = remove_emoji(text) 
    
    # Remove repeated puntuations / words
    text = remove_elongated_words(text)    #revomve word repeated like HHHHHH
    text = remove_repeat_punct(text)       #remove repeated punctuation

    text = remove_all_punct(text)          #remove punctuation
    text = remove_punct(text)              #remove other punctuation
    text = remove_stopwords(text)          #remove basic words like (and,or,...)
    
    #Stemming or Lemmatization
    text = lemmatizing2(text)               #replace words to simple (infinitif , singular, ...)
    
    #My methode of lemmatization
    text =clean_lemma(text)

    return text


def polarity(text):
    return TextBlob(text).sentiment.polarity

def sentiment(label):
    if label <0:
        return -1
    elif label ==0:
        return 0
    elif label>0:
        return 1

def sentiment_data(df):
    df['Sentiment_polarity']=df['Text'].apply(polarity)
    df['Sentiment']=df['Sentiment_polarity'].apply(sentiment)

def most_common_words(df):
    texts=''
    for text in df['Text']:
        texts=texts+' '+text
    test = texts.split(' ')
    c=Counter(test)
    return c.most_common(200)

def create_feature_occurrence_table(comments, features):
    # Initialize an empty dictionary to store the feature counts
    feature_counts = {}

    # Iterate over each feature
    for feature in features:
        # Initialize an empty list to store the occurrence counts for the feature
        counts = []

        # Iterate over each comment
        for comment in comments:
            # Count the occurrences of the feature in the comment
            count = comment.count(feature)
            # Append the count to the list
            counts.append(count)

        # Store the list of counts in the feature_counts dictionary
        feature_counts[feature] = counts

    # Create a DataFrame from the feature_counts dictionary
    df = pd.DataFrame(feature_counts)

    # Return the DataFrame
    return df

def text_to_feature(df):

    columns=[]
    for i in most_common_words(df):
        columns.append(i[0])

    texts=list(df['Text'])

    return create_feature_occurrence_table(texts,columns)

def clean_data(df):
    columns_date(df)
    df = df.drop(['Username','Date'],axis=1)
    df['Text']=df['Text'].apply(clean_tweet)
    df_occurrence = text_to_feature(df)
    df = pd.concat([df,df_occurrence] , axis=1)
    sentiment_data(df)
    df_filtered = df.loc[~(df.iloc[:,8:-2] == 0).all(axis=1)]

    return df_filtered


