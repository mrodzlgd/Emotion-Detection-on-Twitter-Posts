import pandas as pd
import re
import re
from pycontractions import Contractions
import emoji
from textblob import Word


def get_hashtags(series):
    hashtags = (series.apply(lambda x: re.findall('#[\w]*', x))).tolist()
    #change list of lists to a single list
    hashtag_list = []
    for h in hashtags:
        for item in h:
            hashtag_list.append(item)
    hashtag_df=pd.DataFrame(hashtag_list, columns = ['hashtag'])
    return hashtag_df
    
def set_lower(series):
    #set everything to lower case
    lowercase = series.apply(lambda x: " ".join(x.lower() for x in x.split()))
    return lowercase

def remove_usernames(series):
    no_username = series.apply(lambda x: re.sub('@[\w]*', "", x))
    return no_username

def remove_hashtags(series):
    no_hash = series.apply(lambda x: re.sub('#[\w]*', "", x))
    return no_hash
   
def ReplaceThreeOrMore(s):
    # pattern to look for three or more repetitions of any character, including
    # newlines.
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)


def preprocessing_text(df,series):
    #removing usernames
    df[series] = df[series].apply(lambda x: re.sub('@[\w]*', "", x))
    #remove hashtag from clean text
    df[series] = remove_hashtags(df[series])
    # de-emojizing 
    df[series] = df[series].apply(lambda x: emoji.demojize(x))
    #remove characters repeated more than 2 times
    df[series] = df[series].apply(lambda x: ReplaceThreeOrMore(x))
    #removing links to websites
    df[series] = df[series].apply(lambda x: re.sub(r"http\S+", "", x))
    #remove html characters
    df[series] = df[series].apply(lambda x: x.replace('&amp',''))
    df[series] = df[series].apply(lambda x: x.replace('\n',''))
    df[series] = df[series].apply(lambda x: x.replace('á',''))
    df[series] = df[series].apply(lambda x: x.replace('&lt;',''))
    df[series] = df[series].apply(lambda x: x.replace('&gt;',''))          
    #handle contractions
    cont = Contractions(api_key="glove-twitter-100")
    df[series] = df[series].apply(lambda x: list(cont.expand_texts([x])))
    df[series] = df[series].apply(lambda x: str(x))
    #removing numbers
    df[series] = df[series].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))
    #remove punctuation
    twitter_df['clean_text'] = twitter_df['clean_text'].str.replace('[^\w\s]',' ')
    twitter_df['clean_text'] = twitter_df['clean_text'].apply(lambda x: x.replace('[',''))
    twitter_df['clean_text'] = twitter_df['clean_text'].apply(lambda x: x.replace(']',''))
    twitter_df['clean_text'] = twitter_df['clean_text'].apply(lambda x: x.replace("'",''))    
    #set to lowercase
    df[series] = df[series].apply(lambda x: " ".join(x.lower() for x in x.split()))
    #lemmatization
    df[series] = df[series].apply(lambda x: str(x))
    df[series] = df[series].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    return df