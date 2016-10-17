from nltk.sentiment.vader import SentimentIntensityAnalyzer
from enum import IntEnum
import json
import codecs
# For classification
class Positivity(IntEnum):
    positive = 1
    negative = -1
    neutral = 0

file_name = "CompiledTweets.txt"

# Threshold for classifier, > 0.25 is positive, < -0.25 is negative, else neutral
THRESHOLD = 0.25

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

vaderAnalyzer = SentimentIntensityAnalyzer()
for tweet in hand_coded_tweets:
	scores = vaderAnalyzer.polarity_scores(tweet['text'])
	if scores['compound'] >= THRESHOLD:
		tweet['sentiment'] = Positivity.positive
	elif scores['compound'] <= -THRESHOLD:
		tweet['sentiment'] = Positivity.negative
	else:
		tweet['sentiment'] = Positivity.neutral
	print(tweet)

