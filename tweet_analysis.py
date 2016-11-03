'''
Author : Kunwar Deep Singh Toor
Date : 10-22-2016
Version : 1.1
'''

import os
import json
import random
import nltk
from nltk.tokenize import TweetTokenizer


hillary_dictionary = {}
trump_dictionary = {}
keyword_list = []


def dictionaryPopulation(candidate, keywords, rating):
    # add ratings to the dictionary of the purticular candidate

    for keyword in keywords:
        print(candidate,keywords,rating)
        if candidate == "hillary clinton":
            if keyword in hillary_dictionary.keys():
                rating_list = hillary_dictionary.get(keyword)
                rating_list.append(rating)
                hillary_dictionary[keyword] = rating_list
            else:
                rating_list = [rating]
                hillary_dictionary[keyword] = rating_list

        else:
            if keyword in trump_dictionary.keys():

                rating_list = trump_dictionary.get(keyword)

                rating_list.append(rating)
                trump_dictionary[keyword] = rating_list
            else:
                rating_list = [rating]
                trump_dictionary[keyword] = rating_list


def loadKeywords(url):
    #load the keyword list with the specified url
    with open(url,'r') as keywordfile:
        for line in keywordfile:
            keyword_list.append(line.strip())


def ratingAnalysis(tweet):
    #use Vader to analyze the rating

    rating = random.randrange(-1,1)
    return rating
    #generate rating
    #return rating


def findKeywords(tweet):
    #find keywords in a tweet
    found_keywords = []
    tweet_token = TweetTokenizer(reduce_len=True, strip_handles=True)
    word_list = tweet_token.tokenize(tweet.lower())

    if 'hillary' in word_list:
        candidate = "hillary clinton"
    else:
        candidate = "donald trump"

    for word in keyword_list:
        if word in word_list:
            found_keywords.append(word)

    vader_rating = ratingAnalysis(tweet)

    if not found_keywords:
        return 0
    else:
        dictionaryPopulation(candidate,found_keywords,vader_rating)


def dumpFile():
    print("in dump function")
    #produce the output file for R analysis
    with open('analysis_hillary.txt',mode='w') as dumping_file:
         for k, v in hillary_dictionary.items():
             line = '{}, {}'.format(k, v)
             print(line, file=dumping_file)

    with open('analysis_trump.txt',mode='w') as dumping_file:
        for k, v in trump_dictionary.items():
            line = '{}, {}'.format(k, v)
            print(line, file=dumping_file)






'''
Main Method. Execution point
'''
keyword_url = 'keywords.txt'
loadKeywords(keyword_url)

with open('debate_tweets.txt') as tweetfile:
    for line in tweetfile:
        tweet_data = json.loads(line)
        if u'id' in tweet_data:
            tweet = tweet_data[u'text']
            findKeywords(tweet)

dumpFile()
