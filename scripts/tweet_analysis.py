'''
Author : Kunwar Deep Singh Toor
Date : 10-22-2016
Version : 1.1
'''

import os
import json
import random
import timeit
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Candidate identifier
class Candidate():
    hillary = 1
    trump = -1

# Semantic Analyzer
vaderAnalyzer = SentimentIntensityAnalyzer()
# Tweet tokenizer
tweet_token = TweetTokenizer(reduce_len=True, strip_handles=True)

# Used to classify tweets as pertaining to Hillary
hillary_identifiers = [
    u'hillary',
    u'clinton'
]
hillary_hashtags = [
    u'#imwithher',
    u'#hillary',
    u'#clinton',
    u'#hillaryclinton'
]

# Used to classify tweets as pertaining to Trump
trump_identifiers = [
    u'donald',
    u'trump'
]
trump_hashtags = [
    u'#maga',
    u'#trump',
    u'#donaldtrump'
]

# Results objects
hillary_dictionary = {}
trump_dictionary = {}
keyword_list = []
used_tweets = []

def analyze_tweet(tweet):
    # Clean tweet using NLTK tokenizer
    tweet_text = " ".join(tweet_token.tokenize(tweet['text'].lower()))

    # Who is the tweet primarily talking about?
    candidate = identify_candidate(tweet_text)

    # Now, find any keywords
    found_keywords = []
    for word in keyword_list:
        if word in tweet_text:
            found_keywords.append(word)

    # If keywords are found, use VADER semantic analyzer
    if len(found_keywords) == 0:
        return None
    else:
        vader_rating = sentiment_score(tweet_text)
        if vader_rating != 0:
            record_ratings(candidate, found_keywords, vader_rating)
            used_tweets.append(tweet)

    return

def identify_candidate(tweet_text):
    # 2 stages, simple identifier search and keyword search
    # First, if we find a hashtag, we are fairly sure that is the candidate
    if any(hashtag in tweet_text for hashtag in hillary_hashtags):
        return Candidate.hillary
    if any(hashtag in tweet_text for hashtag in trump_hashtags):
        return Candidate.trump

    # Since we didn't find any hashtags, do an identifier search
    # Search for Hillary identifier
    hillary_index = -1
    for identifier in hillary_identifiers:
        hillary_index = tweet_text.find(identifier)
        if hillary_index != -1: break

    # Search for Trump identifier
    trump_index = -1
    for identifier in trump_identifiers:
        trump_index = tweet_text.find(identifier)
        if trump_index != -1: break

    # Can't determine who the tweet was for!
    if hillary_index == -1 and  trump_index == -1:
        return None

    # Only one candidate was mentioned
    if hillary_index == -1 or trump_index == -1:
        return Candidate.hillary if hillary_index == -1 else Candidate.trump

    # Both were mentioned, pick the one appearing first!
    if hillary_index < trump_index:
        return Candidate.hillary
    else:
        return Candidate.trump

    return None

def sentiment_score(tweet_text):
    # calculate sentiment score
    return vaderAnalyzer.polarity_scores(tweet_text)['compound']

def record_ratings(candidate, keywords, rating):
    # add ratings to the dictionary of the purticular candidate
    for keyword in keywords:
        if candidate == Candidate.hillary:
            if keyword in hillary_dictionary.keys():
                hillary_dictionary[keyword].append(rating)
            else:
                rating_list = [rating]
                hillary_dictionary[keyword] = rating_list
        else:
            if keyword in trump_dictionary.keys():
                trump_dictionary[keyword].append(rating)
            else:
                rating_list = [rating]
                trump_dictionary[keyword] = rating_list
    return


def dump_json():
    #produce the output file for R analysis
    with open('analysis_hillary.json',mode='w') as dumping_file:
        json.dump(hillary_dictionary, dumping_file)

    with open('analysis_trump.json',mode='w') as dumping_file:
        json.dump(trump_dictionary, dumping_file)

    with open('used_tweets.json',mode='w') as dumping_file:
        json.dump(used_tweets, dumping_file)

    return

def load_keywords(url):
    #load the keyword list with the specified url
    with open(url,'r') as keywordfile:
        for line in keywordfile:
            keyword_list.append(line.strip())

    return

def update_progress(progress):
    print '\rProcessing tweets... {0:.2f}%'.format(progress*100),
    return

'''
Main Method. Execution point
'''
if __name__ == '__main__':
    keyword_url = '../data/keywords.txt'
    load_keywords(keyword_url)

    num_tweets = 0
    with open('../data/debate_3.json') as tweetfile:
        num_tweets = sum(1 for line in tweetfile)

    with open('../data/debate_3.json') as tweetfile:
        for index, line in enumerate(tweetfile):
            tweet = json.loads(line)
            if index % 100 == 0 or index + 1 == num_tweets:
                update_progress(float(index)/float(num_tweets))
            if u'id' in tweet:
                analyze_tweet(tweet)

    # Save results
    dump_json()
