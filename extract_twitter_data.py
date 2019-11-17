import tweepy
import pandas as pd
import datetime
import time

def import_data(filelist):
    """ Files provided will be imported and joined into one dataframe
    with twp series named:  tweet_id , emotion."""
    df = pd.concat([pd.read_csv(item , sep = '\t' , header = None , names = ['tweet_id','emotion']) for item in filelist], axis=0)
    df.reset_index(inplace = True)
    df.drop(columns = 'index', inplace = True)
    df.drop_duplicates(keep = 'first', inplace = True)
    df.reset_index(inplace = True)
    df.drop(columns = 'index', inplace = True)
    return df


def subsetting_emotions(data,label):
    """A subset of the input data will be returned based on the label provided"""
    df = data.loc[data.emotion == label]
    return df


def connect_to_twitter_OAuth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
    """This helper function sets up the connection to twitter by using tweepy API.
    You need to enter your authentication information provided by twiteer when you set 
    up your developer account"""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def get_tweets(api, category, label):
    """This helper function to download tweet posts based on ID
    each request pulls 100 id's, the max amount of request is 450 every 15 minutes
    will process 45k id's then will wait 15 mins and will continue.
    
    Inputs: category->the dataset that contains the tweet ids you want to download
            label-> the name of the emotion corresponding to those tweets which will be used to name the csv file
    """
    
    e = list(category.tweet_id)
    data = []
    total = len(e)
    start = 0
    end = 100
    counter = 0
    e_batch = e[start:end]
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(st,'- extracting ',label)
    while total>0:
        status = api.statuses_lookup(e_batch)
        count = list(range(0,len(status)))
        d_counter1 = len(data)         
        for x in count:
            post = status[x]
            tweet = post._json
            data.append({'id': tweet['id'] , 'text': tweet['text']})
        d_counter2 = len(data) 
        delta = d_counter2 - d_counter1
        counter += delta
        start += 100
        end += 100
        total -= 100
        e_batch = e[start:end]      
        #when counter is 45k or more it will stop for 15 mins, then the counter is restarted
        if counter >= 45000:
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print('records so far:', len(data))
            #wait 15 mins
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print(st,'- waiting 15 mins for next',label,'batch...')
            time.sleep(900)
            counter = 0
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print(st,'restarted counter:',counter)
    edf = pd.DataFrame(data)
    name = './data/'+label+'.csv'
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(st,'done with',label,'batch.')
    edf.to_csv(name)     