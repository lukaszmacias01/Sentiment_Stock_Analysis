# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:01:34 2024

@author: PC
"""

import pandas as pd 
import matplotlib.pyplot as plt

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

df = pd.read_excel('tesla_comments.xlsx')
print(df['time'].min()) # start: 2024-04-18 12:36:47

# initalize analyzer 
sia = SentimentIntensityAnalyzer()

# demo 
sentiment = sia.polarity_scores("This is a great day!")
print(sentiment) 

sentiment = sia.polarity_scores("This is a terrible day!")
print(sentiment) 

sentiment = sia.polarity_scores("A day has 24 hours")
print(sentiment) 

# -----------------------------------------------------------------------------

def get_sentiment_score(x): 
    try:
        return sia.polarity_scores(x)
    except AttributeError:
        return None

# -----------------------------------------------------------------------------

# apply score 

df['sentiment_score_full'] = df['text'].apply(get_sentiment_score)

# -----------------------------------------------------------------------------

df_score_decoposed = pd.json_normalize(df['sentiment_score_full']).add_prefix('sentiment_')

df_combined = pd.concat([df, df_score_decoposed], axis=1)

df_combined.to_excel('tsla_comments_plus_sentiment.xlsx')
