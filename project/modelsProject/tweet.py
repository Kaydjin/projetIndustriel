#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tweet:
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
		self.tweet_id = idd
		self.tweet_created_at = date
		self.tweet_text = text
		self.hashtags   = tags
		self.tweet_quoted_status_id = quotedId
		self.tweet_mention = mention
		self.pertinent = pertinent
		self.proba_pertinence = p
		self.user_id = userId
		self.user_screenname  = userScreenname
		self.user_name = userName
		self.user_location = userLocation
		self.user_description = userDescription

		""" Parametre supplementaire pour les cas personnes, on separe le nom et le prenom """
		self.userSurname = nom
		self.userFirstname = prenom

		""" Parametre supplementaire, trois types d'auteurs: PERSON, INDETERMINED, COMPANY. """
		self.typeAuthor = typeAuteur

	def synthese(self):
		return self.tweet_text + " " + self.hashtags + " " + self.tweet_mention +" " + self.user_location + " " + self.user_description
