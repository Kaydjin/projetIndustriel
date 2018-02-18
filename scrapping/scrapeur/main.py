#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import re
import sys
import time
from normalizeDatas import *
from scrappingLibrary import sGoogle
from textanalyser import *
from scrappingLibrary import sFacebook

#from linkedIn_Recherche import *

if __name__ == '__main__':

	""" First step, Initialize : instanciation and determinate type of author for a majority of the tweet """
	reader = Datas()
	reader.readFromCsv("res/iteration_500.csv")

	""" Second step: Search : instanciate for Person or Indeterminate tweets, the result for search on linkedin and facebook"""
	tweets = reader.getPeopleTweets(True)

	for val in tweets[:8]:

		""" The first search is with location, the second without """
		print(val.user_name)
		resultFacebook = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "facebook", False)
		resultLinkedin = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "linkedin", False)
		resultFacebookC = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "facebook", True)
		resultLinkedinC = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, val.user_location, "linkedin", True)
		for d in resultFacebook:
			print(d)
			new_url = sFacebook.standardUrl(d)
			if sFacebook.certifiatePagePersonnality(new_url):
				print("Page personnality, donc pas prise en compte")
		for d in resultLinkedin:
			print(d)
		for d in resultFacebookC:
			print(d)
		for d in resultLinkedinC:
			print(d)
"""
		resultFacebook2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "facebook", False)
		resultLinkedin2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "linkedin", False)
		resultFacebookC2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "facebook", True)
		resultLinkedinC2 = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "linkedin", True)

		print(len(resultFacebook) - len(resultFacebook2))
		print(len(resultLinkedin) - len(resultLinkedin2))
		print(len(resultFacebookC) - len(resultFacebookC2))
		print(len(resultLinkedinC) - len(resultLinkedinC2))"""



