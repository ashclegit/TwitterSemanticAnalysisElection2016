import requests
import json

hillary_tweets = []
trump_tweets = []

limit = 15

with open("../data/simple_tweets_hillary.json",mode="r") as tweet_ids:
    count = 0
    ids = json.load(tweet_ids)

    for tweet_id in ids:
        r = requests.get("http://www.twitter.com/anyuser/status/{0}".format(tweet_id['id']))
        if r.status_code == 200:
            hillary_tweets.append(tweet_id)
            print("Found tweet! {0}".format(tweet_id))
            count+=1
            if count >= 15:
                break

    with open("../data/simple_tweets_hillary_confirmed.json",mode="w") as dumping_file:
        json.dump(hillary_tweets, dumping_file)

with open("../data/simple_tweets_trump.json",mode="r") as tweet_ids:
    count = 0
    ids = json.load(tweet_ids)

    for tweet_id in ids:
        r = requests.get("http://www.twitter.com/anyuser/status/{0}".format(tweet_id['id']))
        if r.status_code == 200:
            trump_tweets.append(tweet_id)
            print("Found tweet! {0}".format(tweet_id))
            count+=1
            if count >= 15:
                break

    with open("../data/simple_tweets_trump_confirmed.json",mode="w") as dumping_file:
        json.dump(trump_tweets, dumping_file)
