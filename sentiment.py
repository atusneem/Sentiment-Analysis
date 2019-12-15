#Ayra Tusneem
#CPSC 353-02
#Assignment 2: Twitter Sentiment Analysis

import twitter
import json
import sys
import codecs

# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information
# on Twitter's OAuth implementation.

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print('Example 1')
print('Establish Authentication Credentials')

CONSUMER_KEY = 'ftyzJKRgJpic0c77u7GMvwsxS'
CONSUMER_SECRET = '6uBZu8ab0AlSkamQprQ0P80kBLg1dCkmbTK3jlVf85l75m7sej'
OAUTH_TOKEN = '970370538-UuwT1VLbd9c0Wln5HRqqfN3huBcEvyFJ1HxDpSl6'
OAUTH_TOKEN_SECRET = 'W5AlWTEwwCSfQA9HzRVGYv2IfDu5HMhd4vVDNqxle39v8'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

print("Nothing to see by displaying twitter_api")
print(" except that it's now a defined variable")
print()
print(twitter_api)

# Import unquote to prevent url encoding errors in next_results


# XXX: Set this variable to a trending topic,
# or anything else for that matter. The example query below
# was a trending topic when this content was being developed
# and is used throughout the remainder of this chapter.

# q = '#MentionSomeoneImportantForYou'
# finds tweets with sentiment term and returns the score of the sentiment analysis
def sentiment(term):
    count = 1000
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses']
    for _ in range(5):
        print("Length of statuses", len(statuses))
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:
            break
        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
    print(json.dumps(statuses[0], indent=1))
    status_texts = [status['text']
                    for status in statuses]
    words = [w
             for t in status_texts
             for w in t.split()]
    print(json.dumps(words[0:5], indent=1))
    print()
    sent_file = open('AFINN-111.txt')
    scores = {}  # initialize an empty dictionary
    for line in sent_file:
        term, score = line.split("\t")
        # The file is tab-delimited.
        # "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    score = 0
    for word in words:
        if word in scores.keys():
            score = score + scores[word]
    return float(score)

#user enters two search terms and recieves sentiment score, output of which word has higher sentiment
q = input('Enter a search term: ')
senOne = sentiment(q)
print("Sentiment for " + q)
print(senOne)
p = input('Enter a second search term: ')
senTwo = sentiment(p)
print("Sentiment for " + p)
print(senTwo)

if senOne > senTwo:
    print(q + "has a higher sentiment")
elif senOne == senTwo:
    print("The sentiment scores are equal")
else:
    print(p + " has a higher sentiment")
