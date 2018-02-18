#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import re
import sys
import time
from modelsProject.instance import *
from normalizeDatas import *
from scrappingLibrary import sGoogle
from textanalyser import *
from scrappingLibrary import sFacebook

""" Step 2 for a tweet, return an instance for the result of the search for this tweet """
def search(tweet):
	inst = Instance(tweet)
	""" The first search google is with location, we will add a value for the given url """
	searchgoogle(tweet, tweet.user_location, inst, 2)
	""" The second search google is without location, no add value for the given url """
	searchgoogle(tweet, "", inst, 0)
	inst.printLinks()

""" method of step 2: insert the urls in instance """
def searchgoogle(tweet, complementaire, inst, nbEtoiles):

	""" The first search google is with location, we will add a value for the given url """
	resultFacebook = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "facebook", False)
	resultLinkedin = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "linkedin", False)
	resultFacebookC = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "facebook", True)
	resultLinkedinC = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "linkedin", True)

	for link in resultFacebook:
		new_url = sFacebook.standardUrl(link)
		if not sFacebook.certifiatePage(new_url) and (not inst.existFacebookCompanyLink(new_url, [0,nbEtoiles])):
			inst.addFacebookPersonLink((new_url, nbEtoiles))

	for link in resultLinkedin:
		if not inst.existLinkedinPersonLink(link, [0,nbEtoiles]):
			inst.addLinkedinPersonLink((link,nbEtoiles))

	for link,desc in resultFacebookC:
		new_url = sFacebook.standardUrl(link)
		if sFacebook.certifiatePage(new_url) and (not inst.existFacebookCompanyLink(new_url, [0,nbEtoiles])):
			inst.addFacebookCompanyLink((new_url, nbEtoiles))

	for link,desc in resultLinkedinC:
		if not inst.existLinkedinCompanyLink(link, [0,nbEtoiles]):
			inst.addLinkedinCompanyLink((link,nbEtoiles))



if __name__ == '__main__':

	""" First step, Initialize : instanciation and determinate type of author for a majority of the tweet """
	reader = Datas()
	reader.readFromCsv("res/iteration_500.csv")

	""" Second step: Search : instanciate for Person or Indeterminate tweets, the result for search on linkedin and facebook"""
	tweets = reader.getPeopleTweets(True)

	for val in tweets[18:21]:

		search(val)


