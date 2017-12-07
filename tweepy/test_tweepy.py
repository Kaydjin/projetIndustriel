import time
import tweepy
from tweepy import OAuthHandler

consumer_key = "xYkxHM1NNNr7gxZC2pYCtQz62"
consumer_secret = "NAiTFQ96tjgz4Jgwg0uNv9ZCVifF1I1Haajhw4pBDwz8yg8AYO"
access_token = "935087442562048001-Wr2RsLYGJbEm2mWTOBloovWiwmqhriN"
access_secret = "YcT1Blbinq2kPBcIZpzoOcfp4VbQoyieJc4ttVbbwBnIe"

#Identification et connexion
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
statut = api.get_user(id = 4853014018)
statuses = api.user_timeline(id = 4853014018, count = 10)

for property, value in vars(statut).iteritems():
    print property, ": ", value

for status in statuses:
	print "***"
	print "Tweet id: " + status.id_str
	print status.text
	print "Retweet count: " + str(status.retweet_count)
	print "Favorite count: " + str(status.favorite_count)
	print status.created_at
	print "Status place: " + str(status.place)
	print "Source: " + status.source
	print "Coordinates: " + str(status.coordinates)
	
	time.sleep(1)