# Emotion Detection on Twitter Posts
by Melissa Rodriguez

## Goal:

Create a Machine Learning Classification Model able to classify emotions from Twitter Posts. Ideally, an emotion detection model can help understand the emotional state of users and help identify trends that could require attention from healthcare providers, and/or close acquaintances.

 __Files:__

- Emotion_Detection_from_Twitter_Posts.pdf

- __Folder__: Jupyter_Notebooks_and_Scripts
    - 01-Twitter_Extract.ipynb
    - 02-Merging_Data.ipynb
    - 03-Data_Analysis_and_Pre-processing.ipynb
    - 04-Classification_with_Keras.ipynb
    - connect_and_create.py
    - extract_twitter_data.py
    - metrics_and_evaluation.py
    - preprocessing.py

## Process:

### Dataset

![Length of Twitter Posts](./images/dataflow.png)




- Data was downloaded from: http://knoesis.org/projects/emotion
- Dataset contains tweet id and emotion label
- Tweet texts needs to be downloaded by using the tweet id. - See notebook: 01-Twitter_Extract.ipynb
- __1339794__ records were extracted from Twitter using Tweepy.
    -  For more details about tweepy refer to: https://tweepy.readthedocs.io/en/latest/
- After noticing that not all records were saved in a csv file, decided to save all merged data into an SQLite Database. - See Notebook: 02-Merging_Data.ipynb


### Exploratory Data Analysis

__Counts per emotion classes:__

Classes are unbalanced.

![Emotion Counts](./images/Tweets_Emotion.png "Counts by Class")

__Reviewing text length:__

Text length ranges from 13 to 345 characters.

  Distribution:

  ![Length of Twitter Posts](./images/Tweets_Text_Length.png "Length of Twitter Posts Text")

  Text examples:

  These posts might not have any characters or be useful after preprocessing.

![Short Text](./images/text_lenght_example.PNG "Short Text")

![Long Text](./images/text_lenght_example_long.PNG "Long Text")


#### Preprocessing data

Since my interest is to work with the emotions that could show issues like depression, I decided to subset the data for the following classes:

 - Fear
 - Sadness
 - Anger
 - Joy

The following steps were performed to the texts from Twitter Posts:

- Removed usernames
- Removed hashtags (they were used for classification process, this will avoid leakage)
- Transformed emojis: used emoji module to change emojis to words.
    -For more details refer to: https://pypi.org/project/emoji/
- Removed characters repeated more than 2 times
- Removing links to websites
- Removed html characters
- Transformed contractions - replacing words like can't with can not.
    - For more details refer to:https://pypi.org/project/pycontractions/
- Removed numbers
- Removed punctuation
- Set to lowercase
- Lemmatization

__Sub setting by Text Length__

Will subset the data to only those posts where text length is more than 25 characters


__Undersampling__

Since Fear label is the smallest with about 65k records, selected 80k random records for the other three labels.

__Train and Test Model__



__References:__

http://knoesis.org/sites/default/files/wenbo_socialcom_2012_0.pdf
