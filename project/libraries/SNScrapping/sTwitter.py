#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
if __name__ == "__main__":
	from models.accountTwitter import *
	from models.tweet import *
	from utils import utils
	from settings.settingsTwitter import *
else:
	from .models.accountTwitter import *
	from .models import tweet
	from .utils import utils
	from .settings.settingsTwitter import *
import sys
import time

""" Keys variables keep in settings
consumer_key
consumer_secret
access_token
access_token_secret
"""

""" Variables of a tweet (see models/tweet.py)"""
""" Variables of a user (see models/accountTwitter.py)"""

""" A listener handles tweets that are received from the stream.
This is a basic listener that just prints received tweets to stdout.
"""
class StdOutListener(StreamListener):

	def __init__(self, start_time, time_limit=60):
		StreamListener.__init__(self)
		self.time = start_time
		self.limit = time_limit
		self.tweet_data = []

	def on_error(self, status_code):
		if status_code == 420:
			#returning False in on_data disconnects the stream
			print("too much request")
			return False
		return False

	def on_status(self, status):
		if(time.time() - self.time)<self.limit:
			mentions =""
			hashtags = ""

			#here we use screen_name, we could have keep their id
			for var in status.entities.get("user_mentions"):
				mentions = mentions + " " + var.get("screen_name")
			for var in status.entities.get("hashtags"):
				hashtags = hashtags + " " + var.get("text")
			self.tweet_data.append(Tweet(status.id, status.created_at, status.text, hashtags, status.in_reply_to_user_id,
				mentions, status.user.id, status.user.screen_name, status.user.name, status.user.location, status.user.description))
			return True

		""" stop streaming """
		return False

	""" Return a optional numbers of tweet starting from an index, by default return all"""
	def get(self, default=True, index=0, numbers=10):
		if not default:
			# return what possible if the size of the list of tweets is less than numbers
			if (index+numbers)<len(self.tweet_data):
				return self.tweet_data[index, index+numbers]
			else:
				return self.tweet_data[index, len(self.tweet_data)]
		else:
			return self.tweet_data

""" Streaming with parameters """
def stream(filter_list, time_out=30):
	t = time.time()
	l = StdOutListener(t,time_out)
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	print("Launch...")
	stream = Stream(auth, l)
	stream.filter(track=filter_list)
	print("End of streaming")
	return l.get()

""" Return the user account of a specified id with an optional number of last tweets of the account to instanciate """
def get_account(id_account, number_tweets = 10):
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	statut = api.get_user(id = id_account)

	tweets = profil_tweets(id_account, number_tweets)
	account = AccountTwitter(statut.id, statut.followers_count, statut.location, statut.statuses_count, statut.description,
		statut.friends_count, statut.notifications, statut.screen_name, statut.favourites_count, statut.name,
		statut.url, statut.created_at, statut.following, tweets)
	return account

""" Return the specified numbers of tweets last posted by a specified id account """
def profil_tweets(id_account, numbers):
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	statuses = api.user_timeline(id = id_account, count = numbers)
	result = []
	for status in statuses:
		mentions =""
		hashtags = ""
		for var in status.entities.get("user_mentions"):
			mentions = mentions + " " + var.get("screen_name")
		for var in status.entities.get("hashtags"):
			hashtags = hashtags + " " + var.get("text")
		result.append(Tweet(status.id, status.created_at, status.text, hashtags, status.in_reply_to_user_id,
			mentions, status.user.id, status.user.screen_name, status.user.name, status.user.location, status.user.description))
	return result

if __name__ == '__main__':
	result = stream(["affair", "russia"], time_out=10)
	#for tweet in result:
	#    print(tweet.synthese())
	id_user_one = result[0].user_id
	tweets = profil_tweets(id_user_one, 50)
	#for tweet in tweets:
	#	print(tweet.synthese())
	account = get_account(id_user_one)
	for tweet in account.tweets:
		print(tweet.synthese())
