# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 11:49:23 2024

@author: PC
"""

import pandas as pd 

df_sentiment = pd.read_excel('tsla_comments_plus_sentiment.xlsx')
df_tsla_price = pd.read_excel('tsla_prices.xlsx')

'''
Article on sentiment analysis: 

https://medium.com/@rslavanyageetha/vader-a-comprehensive-guide-to-sentiment-analysis-in-python-c4f1868b0d2e
'''

# -----------------------------------------------------------------------------

print(df_sentiment['time'].min())

df_sentiment['day_of_year'] = df_sentiment['time'].dt.dayofyear

df_sentiment['day_of_year', 'sentiment_compound']

df_senti_non_0 = df_sentiment[df_sentiment['sentiment_compound'] != 0]

mean_sentiment_by_day = df_sentiment.groupby('day_of_year')['sentiment_compound'].mean().reset_index()

mean_senti_by_day_non_0 = df_senti_non_0.groupby('day_of_year')['sentiment_compound'].mean().reset_index()

# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt

plt.hist(mean_senti_by_day_non_0['sentiment_compound'], bins = 30)

# -----------------------------------------------------------------------------

df_tsla_price['day_of_year'] = df_tsla_price['Date'].dt.dayofyear

# -----------------------------------------------------------------------------

df_combined = pd.merge(df_tsla_price, mean_senti_by_day_non_0, on='day_of_year', how='inner')

# -----------------------------------------------------------------------------
# Create the histogram for the 'sentiment_compound' column
plt.figure(figsize=(10, 6))
plt.hist(df_senti_non_0['sentiment_compound'], bins=100, color='skyblue', edgecolor='black')

plt.xlabel('Sentiment Compound Score')
plt.ylabel('Frequency')
plt.title('Histogram of Sentiment Compound Scores')

plt.show()

# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting 'Close' on the primary y-axis
ax1.plot(df_combined['day_of_year'], df_combined['Close'], color='blue', label='Close Price')
ax1.set_xlabel('Day of Year')
ax1.set_ylabel('Share Price', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a secondary y-axis for 'sentiment_compound'
ax2 = ax1.twinx()
ax2.plot(df_combined['day_of_year'], df_combined['sentiment_compound'], color='red', label='Sentiment Compound')
ax2.set_ylabel('Sentiment Compound', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Set x-axis labels with vertical rotation
plt.xticks(rotation=90)

plt.title('Share Price and Sentiment Compound Over the Year by day')

# Show the plot
plt.show()





