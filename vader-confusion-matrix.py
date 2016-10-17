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
THRESHOLD = 0.15

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

confusion_matrix = {
	'pos_pos': 0,
	'pos_neg': 0,
	'pos_neu': 0,
	#############
	'neg_pos': 0,
	'neg_neg': 0,
	'neg_neu': 0,
	#############
	'neu_pos': 0,
	'neu_neg': 0,
	'neu_neu': 0
}

vaderAnalyzer = SentimentIntensityAnalyzer()
for tweet in hand_coded_tweets:
	scores = vaderAnalyzer.polarity_scores(tweet['text'])
	if scores['compound'] >= THRESHOLD:
		tweet['sentiment'] = Positivity.positive
	elif scores['compound'] <= -THRESHOLD:
		tweet['sentiment'] = Positivity.negative
	else:
		tweet['sentiment'] = Positivity.neutral


	if int(tweet['code']) == 1:
		if tweet['sentiment'] == Positivity.positive:
			confusion_matrix['pos_pos'] += 1				
		elif tweet['sentiment'] == Positivity.negative:
			confusion_matrix['pos_neg'] += 1				
		else:
			confusion_matrix['pos_neu'] += 1				
	elif int(tweet['code']) == -1:
		if tweet['sentiment'] == Positivity.positive:
			confusion_matrix['neg_pos'] += 1				
		elif tweet['sentiment'] == Positivity.negative:
			confusion_matrix['neg_neg'] += 1				
		else:
			confusion_matrix['neg_neu'] += 1				
	else:
		if tweet['sentiment'] == Positivity.positive:
			confusion_matrix['neu_pos'] += 1				
		elif tweet['sentiment'] == Positivity.negative:
			confusion_matrix['neu_neg'] += 1				
		else:
			confusion_matrix['neu_neu'] += 1				
print("Total Tweets Analyzed: {0}\n".format(len(hand_coded_tweets)))

for key, value in sorted(confusion_matrix.items()): # Note the () after items!
    print(key, value)
