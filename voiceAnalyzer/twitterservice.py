#!/usr/bin/env python

from functools import reduce
from pprint import pprint as pp
from datetime import datetime
import string
from pandas import pandas as pd
from voiceAnalyzer import twitterApi, sentimentDF


class TwitterService:
    """Service for retrieving and manipulating twitter data"""
    def __init__(self, username, countOfTweets):
        self._username = username
        self._count = countOfTweets
        self._stripped_tweets = self._get_stripped_tweets()
        self._tweet_df = self._get_tweets_df()
        self._words_df = self._get_words_df()

    def _retrieve_tweets(self):
        return twitterApi.statuses.user_timeline(
            screen_name=self._username,
            count=self._count
        )

    def _get_stripped_tweets(self):
        tweets = self._retrieve_tweets()
        return [{'text':x['text'].lower().encode('unicode_escape').decode('utf-8'),
                 'created':datetime.strptime(x['created_at'] + ' UTC',
                                             '%a %b %d %H:%M:%S +0000 %Y %Z')}
                for x in tweets if not bool(x['retweeted'])]

    def _get_tweets_df(self):
        stripped_tweets = self._get_stripped_tweets()
        tweet_df = pd.DataFrame(stripped_tweets)
        tweet_df['dayOfWeekNum'] = tweet_df.apply(lambda row: row['created'].weekday(), axis=1)
        tweet_df['dayOfWeek'] = tweet_df.apply(lambda row: row['created'].strftime('%A'), axis=1)
        tweet_df['hourOfDay'] = tweet_df.apply(lambda row: row['created'].hour, axis=1)
        return tweet_df

    def _get_words_df(self):
        punctuation_stripper = str.maketrans(
            {key: None for key in '\n' + string.punctuation.replace('#', '')})
        just_the_text_bits = [twt['text'].replace('\\n', ' ').translate(punctuation_stripper)
                              for twt in self._stripped_tweets]
        all_the_text = reduce(lambda x, y: x +' '+ y, just_the_text_bits)
        word_df = pd.DataFrame({'word':all_the_text.split(), 'numberOfOccurences':1})
        return word_df.groupby('word', as_index=False).agg({'numberOfOccurences':'count'})

    def get_tweet_day_of_week_data(self):
        """counts tweets per day of week"""
        group_count_df = self._tweet_df.groupby(['dayOfWeekNum', 'dayOfWeek'],
                                                as_index=False).agg({'created':'count'})
        group_count_df = group_count_df.rename(columns={'created':'dayOfWeekCount'})
        return TwitterService.add_percentage_column(group_count_df, 'dayOfWeekCount')

    def get_tweet_hour_of_day_data(self):
        """counts tweets per hour of the day"""
        hour_count_df = self._tweet_df.groupby('hourOfDay', as_index=False).agg({'created':'count'})
        hour_count_df = hour_count_df.rename(columns={'created':'hourCount'})
        return TwitterService.add_percentage_column(hour_count_df, 'hourCount')

    def get_tweet_sentiment_data(self):
        """parses tweet words, matches with sentiment data"""
        merged_df = self._words_df.merge(sentimentDF, left_on='word', right_on='word')
        grouped_sentiments = merged_df.groupby(
            'sentiment', as_index=False).agg(
                {'numberOfOccurences':'count'})
        return TwitterService.add_percentage_column(grouped_sentiments, 'numberOfOccurences')

    @staticmethod
    def add_percentage_column(dataframe, countcolumn):
        """take a numeric column in a dataframe, sum it and return the percentage of each row
            per specified column"""
        total_sum = dataframe[countcolumn].sum()
        dataframe['percentage'] = dataframe.apply(
            lambda row: row[countcolumn] / total_sum,
            axis=1)
        return dataframe

test_twitter_service = TwitterService('cullimoreorless', 1000)

pp(test_twitter_service.get_tweet_day_of_week_data())
pp(test_twitter_service.get_tweet_hour_of_day_data())
pp(test_twitter_service.get_tweet_sentiment_data())

pp(str(test_twitter_service.get_tweet_day_of_week_data().to_json()))