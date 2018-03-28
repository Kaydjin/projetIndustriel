#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 																																 """
""" 												DOCUMENTATION VARIABLES	OF A TWEET(tweepy) 										 """
""" 																																 """
""" 																																 """

""" """
""" variables of a tweet via tweepy """
""" ""
quote_count
contributors
truncated
text
is_quote_status
in_reply_to_status_id
reply_count
id
favorite_count
_api
source
_json
coordinates
timestamp_ms
entities{
	user_mentions{
		[] example:{u'id': 1864591632, u'indices': [0, 13], u'id_str': u'1864591632', u'screen_name': u'TheoMoudakis', u'name': u'Theo Moudaki}
	}
	hashtags{
		[] example:{u'indices': [14, 17], u'text': u'EU'}
	}
	urls
	symbols
}
in_reply_to_screen_name
in_reply_to_user_id
retweet_count
id_str
favorited
source_url
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
geo
in_reply_to_user_id_str
possibly_sensitive
lang
created_at
author
filter_level
in_reply_to_status_id_str
place
retweeted
"""

""" 																																 """
""" 												CLASS												 							 """
""" 																																 """
""" 																																 """

class Tweet:
	#Variables of a tweet in a csv format
    #tweet_id                   -> 0
	#tweet_created_at           -> 1
	#tweet_text                 -> 2
	#hashtags                   -> 3
	#tweet_quoted_status_id     -> 4
	#tweet_mtion                -> 5    -> tweet_mention
	#user_id                    -> 8
	#user_screenname            -> 9
	#user_name                  -> 10
	#user_location              -> 11
	#user_description           -> 12

	def __init__(self, idd, date, text, tags, quotedId, mention, userId, userScreenname, userName, userLocation, userDescription):
		self.tweet_id = idd
		self.tweet_created_at = date
		self.tweet_text = text

		if tags==None:
			tags = ""
		self.hashtags   = tags

		if quotedId==None:
			quotedId = ""
		self.tweet_quoted_status_id = quotedId
		
		if mention==None:
			mention = ""
		self.tweet_mention = mention

		self.user_id = userId
		
		if userScreenname==None:
			userScreenname = ""
		self.user_screenname  = userScreenname

		if userName==None:
			self.userName = ""
		self.user_name = userName

		if userLocation==None:
			userLocation = ""
		self.user_location = userLocation

		if userDescription==None:
			userDescription = ""
		self.user_description = userDescription

	def synthese(self):
		return self.tweet_text + " " + self.hashtags + " " + self.tweet_mention +" " + self.user_location + " " + self.user_description
