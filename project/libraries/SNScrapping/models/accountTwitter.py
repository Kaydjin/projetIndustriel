#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 																																 """
""" 												DOCUMENTATION USER VARIABLES (tweepy)				 							 """
""" 																																 """
""" 																																 """
"""
user{

	#VARIABLES OF A USER

	follow_request_sent
	profile_use_background_image
	_json
	id
	_api
	verified
	translator_type
	profile_image_url_https
	profile_sidebar_fill_color
	is_translator
	geo_enabled
	profile_text_color
	followers_count
	protected
	location
	default_profile_image
	id_str
	utc_offset
	statuses_count
	description
	friends_count
	profile_link_color
	profile_image_url
	notifications
	profile_background_image_url_https
	profile_background_color
	profile_background_image_url
	screen_name
	lang
	profile_background_tile
	favourites_count
	name
	url
	created_at
	contributors_enabled
	time_zone
	profile_sidebar_border_color
	default_profile
	following
	listed_count
}
"""
""" 																																 """
""" 												CLASS												 							 """
""" 																																 """
""" 																																 """

class AccountTwitter:

	def __init__(self, id_user, followers_count, location, statuses_count, description, friends_count, notifications, screen_name,
		favourites_count, name, url, created_at, following, tweets):
		self.id_user = id_user
		self.followers_count = followers_count
		self.location = location
		self.statuses_count = statuses_count
		self.description = description
		self.friends_count = friends_count
		self.notifications = notifications
		self.screen_name = screen_name
		self.favourites_count = favourites_count
		self.name = name
		self.url = url
		self.created_at = created_at
		self.following = following
		if (tweets==None) or (len(tweets)==0):
			self.tweets = []
		else:
			self.tweets = tweets

	def syntheseTweets(self):
		synthese = ""
		for var in self.last_tweets:
			synthese = synthese + " " + var.synthese()

		return synthese

	def synthese(self):
		return self.location + " " + self.description + " " + self.screen_name +" " + self.name