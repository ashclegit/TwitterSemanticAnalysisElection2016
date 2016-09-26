from nltk.sentiment.vader import SentimentIntensityAnalyzer

tweets = [
    "Hillary Clinton will be an amazing president!",
    "Donald Trump is going to make America great again! :)",
    "Hillary is a criminal, how could she be our president?",
    "Donald trump is an idiot, and has no clue how to be president!!!"
]

vaderAnalyzer = SentimentIntensityAnalyzer()
for tweet in tweets:
    print(tweet)
    scores = vaderAnalyzer.polarity_scores(tweet)
    for score in scores:
        print("{0} : {1}".format(score, scores[score]))
    print('\n')
