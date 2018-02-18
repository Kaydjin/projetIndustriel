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

#from linkedIn_Recherche import *

""" Step 2 for a tweet, return an instance for the result of the search for this tweet """
def search(tweet):
	instance = Instance(tweet)

	""" The first search google is with location, we will add a value for the given url """
	resultFacebook = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "facebook", False)
	resultLinkedin = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "linkedin", False)
	resultFacebookC = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "facebook", True)
	resultLinkedinC = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "linkedin", True)

	for d in resultFacebook:
		new_url = sFacebook.standardUrl(d)
		if not sFacebook.certifiatePage(new_url):
			instance.addAccountFacebookPerson((x, 2))
	for d in resultLinkedin:
		instance.addAccountLinkedinPerson((x,2))
	for d in resultFacebookC:
		new_url = sFacebook.standardUrl(d)
		if sFacebook.certifiatePage(new_url):
			instance.addAccountFacebookCompany((x, 2))
	for d in resultLinkedinC:
		instance.addAccountLinkedinCompany((x,2))

	""" The second search google is without location, no add value for the given url """
	resultFacebook2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "facebook", False)
	resultLinkedin2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "linkedin", False)
	resultFacebookC2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "facebook", True)
	resultLinkedinC2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "linkedin", True)

if __name__ == '__main__':

	""" First step, Initialize : instanciation and determinate type of author for a majority of the tweet """
	reader = Datas()
	reader.readFromCsv("res/iteration_500.csv")

	""" Second step: Search : instanciate for Person or Indeterminate tweets, the result for search on linkedin and facebook"""
	tweets = reader.getPeopleTweets(True)

	for val in tweets[:20]:

		""" The first search is with location, the second without """
		print(val.user_name)
		resultFacebook = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "facebook", False)
		resultLinkedin = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "linkedin", False)
		resultFacebookC = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "facebook", True)
		resultLinkedinC = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "linkedin", True)
		for d in resultFacebook:
			new_url = sFacebook.standardUrl(d)
			if not sFacebook.certifiatePage(new_url):
				print("person:"+d)
		for d in resultLinkedin:
			print("person:"+d)
		for d,j in resultFacebookC:
			print("company:"+d)
		for d,j in resultLinkedinC:
			print("company:"+d)
"""
		resultFacebook2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "facebook", False)
		resultLinkedin2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "linkedin", False)
		resultFacebookC2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "facebook", True)
		resultLinkedinC2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "linkedin", True)

		print(len(resultFacebook) - len(resultFacebook2))
		print(len(resultLinkedin) - len(resultLinkedin2))
		print(len(resultFacebookC) - len(resultFacebookC2))
		print(len(resultLinkedinC) - len(resultLinkedinC2))"""



