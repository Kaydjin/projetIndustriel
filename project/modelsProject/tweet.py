#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libraries.SNScrapping.models import tweet

class Tweet(tweet.Tweet):
   #tweet_id                   -> 0
	#tweet_created_at           -> 1
	#tweet_text                 -> 2
	#hashtags                   -> 3
	#tweet_quoted_status_id     -> 4
	#tweet_mtion                -> 5    -> tweet_mention
	#pertinents                 -> 6    -> pertinent
	#proba_pertinence           -> 7

	#user_id                    -> 8
	#user_screenname            -> 9

	#user_name                  -> 10
	#user_location              -> 11
	#user_description           -> 12

	def __init__(self, idd, date, text, tags, quotedId, mention, pertinent, p, 
		userId, userScreenname, userName, userLocation, userDescription, typeAuteur, prenom, nom):

		#Herite from models.tweet.Tweet
		tweet.Tweet.__init__(self, idd, date, text, tags, quotedId, mention, userId, userScreenname, userName, userLocation, userDescription)

		# parameter for pertinence of a tweet 
		self.pertinent = pertinent
		self.proba_pertinence = p

		# parameter for people type of tweet, we separate user_screename in two part
		self.userSurname = nom
		self.userFirstname = prenom

		# parameter to determinate the type of an author : PERSON, INDETERMINED, COMPANY.
		self.typeAuthor = typeAuteur
