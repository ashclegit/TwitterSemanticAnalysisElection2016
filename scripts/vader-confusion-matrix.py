from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import codecs
import re
import numpy

# For classification
class Positivity():
    positive = 1
    negative = -1

file_name = "../data/CompiledTweets.txt"

def do_matrix(THRESHOLD = 0):

    hand_coded_tweets = []
    hand_coded_json = None

    # Read in file as JSON
    with codecs.open(file_name, "r", encoding='utf-8', errors='ignore') as CompiledTweets:
    	content = CompiledTweets.read()
    	CompiledTweets.close()

    	for line in content.splitlines():
    		fields = line.split("\t")
    		tweet = {}
    		tweet['text'] = fields[0]
    		tweet['code'] = fields[1]
    		hand_coded_tweets.append(tweet)

    	hand_coded_json  = json.dumps(hand_coded_tweets)
    print("Total Tweets {0}".format(len(hand_coded_tweets)))

    confusion_matrix = {
    	'pos_pos': 0,
    	'pos_neg': 0,
    	#############
    	'neg_pos': 0,
    	'neg_neg': 0
    }

    f = open('../data/ClassifiedTweets','w')

    vaderAnalyzer = SentimentIntensityAnalyzer()
    classified = 0
    for tweet in hand_coded_tweets:
    	scores = vaderAnalyzer.polarity_scores(tweet['text'])
    	if scores['compound'] >= THRESHOLD:
    		tweet['sentiment'] = Positivity.positive
    		classified += 1
    	elif scores['compound'] <= -THRESHOLD:
    		tweet['sentiment'] = Positivity.negative
    		classified += 1
    	else:
    		hand_coded_tweets.remove(tweet)
    		continue

    	if int(tweet['code']) == 1:
    		if tweet['sentiment'] == Positivity.positive:
    			confusion_matrix['pos_pos'] += 1
    		elif tweet['sentiment'] == Positivity.negative:
    			confusion_matrix['pos_neg'] += 1
    	elif int(tweet['code']) == -1:
    		if tweet['sentiment'] == Positivity.positive:
    			confusion_matrix['neg_pos'] += 1
    		elif tweet['sentiment'] == Positivity.negative:
    			confusion_matrix['neg_neg'] += 1

    print("\nTotal Tweets Analyzed: {0}".format(classified))
    print("THRESHOLD = {0}".format(THRESHOLD))

    for key, value in sorted(confusion_matrix.items()): # Note the () after items!
        print(key, value),

    print("Accuracy = {0}".format())

if __name__ == '__main__':
    for threshold in numpy.arange(0,1,0.05):
        do_matrix(threshold)
