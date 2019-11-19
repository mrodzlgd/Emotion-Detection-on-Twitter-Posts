import pandas as pd
import re
import re
from pycontractions import Contractions
import emoji
from textblob import Word

def remove_hashtags(series):
    no_hash = series.apply(lambda x: re.sub('#[\w]*', "", x))
    return no_hash
   
def ReplaceThreeOrMore(s):
    # pattern to look for three or more repetitions of any character, including
    # newlines.
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)
 
 
def remove_chars(df, series, char_list):
    for char in char_list:
        df[series] = df[series].apply(lambda x: x.replace(char,''))
    return df


def remove_patterns(df, series, pattern_list):
    for patt in pattern_list:
        df[series] = df[series].apply(lambda x: re.sub(patt, "", x))
    return df
    

def preprocessing_text(df,series):

    #removing patterns (usernames & links to websites)
    pattern_list = ['@[\w]*', r'http\S+']
    remove_patterns(df,series,pattern_list)
    
    #remove hashtag from clean text
    df[series] = remove_hashtags(df[series])
    
    # de-emojizing 
    df[series] = df[series].apply(lambda x: emoji.demojize(x))
    
    #remove characters repeated more than 2 times
    df[series] = df[series].apply(lambda x: ReplaceThreeOrMore(x))

    #remove html characters
    char_list = ['&amp','\n','á','&lt;','&gt;']
    remove_chars(df,series,char_list)  
    
    #handle contractions
    cont = Contractions(api_key="glove-twitter-100")
    df[series] = df[series].apply(lambda x: list(cont.expand_texts([x])))
    df[series] = df[series].apply(lambda x: str(x))
    
    #removing numbers
    df[series] = df[series].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))
   
   #remove punctuation
    df[series] = df[series].str.replace('[^\w\s]',' ')

    #set to lowercase
    df[series] = df[series].apply(lambda x: " ".join(x.lower() for x in x.split()))
    
    #lemmatization
    df[series] = df[series].apply(lambda x: str(x))
    df[series] = df[series].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    return df