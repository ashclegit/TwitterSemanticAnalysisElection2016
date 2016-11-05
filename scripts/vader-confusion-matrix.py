from nltk.sentiment.vader import SentimentIntensityAnalyzer
from enum import IntEnum
import json
import codecs
import re

# For classification
class Positivity(IntEnum):
    positive = 1
    negative = -1

file_name = "CompiledTweets.txt"

# Threshold for classifier, > 0.25 is positive, < -0.25 is negative, else neutral
THRESHOLD = 0.35

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

f = open('ClassifiedTweets','w')

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
		print(scores)
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
	print(tweet, file=f)

print("Total Tweets Analyzed: {0}\n".format(classified))

for key, value in sorted(confusion_matrix.items()): # Note the () after items!
    print(key, value)
