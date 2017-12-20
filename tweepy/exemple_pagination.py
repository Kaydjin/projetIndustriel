import sys
import jsonpickle
import os

searchQuery = 'someHashtag'   this is what we're searching for
maxTweets = 10000000  Some arbitrary large number
tweetsPerQry = 100   this is the max the API permits
fName = 'tweets.txt'  We'll store the tweets in a text file.


 If results from a specific ID onwards are reqd, set since\_id to that ID.
 else default to no lower limit, go as far back as API allows
sinceId = None

 If results only below a specific ID are, set max\_id to that ID.
 else default to no upper limit, start from the most recent tweet matching the search query.
max\_id = -1L

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max\_id <= 0):
                if (not sinceId):
                    new\_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new\_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since\_id=sinceId)
            else:
                if (not sinceId):
                    new\_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max\_id=str(max\_id - 1))
                else:
                    new\_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max\_id=str(max\_id - 1),
                                            since\_id=sinceId)
            if not new\_tweets:
                print("No more tweets found")
                break
            for tweet in new\_tweets:
                f.write(jsonpickle.encode(tweet.\_json, unpicklable=False) +
                        '\\n')
            tweetCount += len(new\_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max\_id = new\_tweets[-1].id
        except tweepy.TweepError as e:
             Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
