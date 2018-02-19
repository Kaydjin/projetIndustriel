#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import os
import re
import sys
import time
from modelsProject.instance import *
from normalizeDatas import *
from scrappingLibrary import sGoogle
from scrappingLibrary import sLinkedin
from scrappingLibrary import sFacebook
from scrappingLibrary.SNScrapping.seleniumClass.mSelenium import *
from textanalyser import *

""" Step 2 for a tweet, return an instance for the result of the search for this tweet """
def search(tweet):
	inst = Instance(tweet)

	""" The first search google is with location, we will add a value for the given url """
	searchGoogle(tweet, tweet.user_location, inst, 2)

	""" The second search google is without location, no add value for the given url """
	searchGoogle(tweet, "", inst, 0)
	inst.printLinks()

	searchFacebook(tweet, inst)
	searchFacebookHomonymes(tweet, inst)

	searchLinkedin(tweet, inst)

	fiveBestFacebook = inst.getFiveBestAccountsFacebook()
	for link,compte,star in fiveBestFacebook:
		searchLinkedinLinked(tweet, inst, compte)

	show_result(inst)
	
	show_company(tweet, inst)

""" method of step 5 : find company """
def show_company(tweet, inst):

	""" Initialize """
	analyser = TextAnalyser()

	print("[company]")
	for link,linkF,compte,valueF,valueT in inst.accountLinkedinPerson:
		for work in compte.experiences:
			result = len(analyser.getMatchingNouns(tweet.synthese(), work.syntheseExperienceC()))
			if result > 3:
				print("\t Links:"+link+" / "+linkF+" entreprise:"+work.nomEntreprise +" star:"+str(result))


""" method of step 5: show only pertinent datas """
def show_result(inst):
	print("["+inst.tweet.userFirstname +" "+inst.tweet.userSurname+"]")
	print("\t[Facebook]{")
	for link,compte,value in inst.accountFacebookPerson:
		start_value = inst.getValueFacebookPersonLink(link)
		if start_value + value > 3:
			print("\t\t[link]"+link)
			print("\t\t[star]"+str((start_value + value)))
	print("\t}")
	print("\t[Linkedin]{")
	for link,linkF,compte,valueF,valueT in inst.accountLinkedinPerson:
		if (linkF=="") and (valueT > 2):
			print("\t\t[link]"+link)
			print("\t\t[star]"+str(valueT))
		if linkF!="":
			facebookAccount = inst.getValueAccountFacebookPerson(linkF)
			if facebookAccount!=None:
				value = inst.getValueFacebookPersonLink(facebookAccount[0])
				value2 = facebookAccount[2]
				if (value!=None) and (value2!=None) and (valueF>5) and (valueT + value +value2 > 4):
					print("\t\t[links]"+link + " / " + linkF)
					print("\t\t[star]"+ str((valueT + value +value2)))
				else:
					if valueT > 3:
						print("\t\t[links]"+link + " / " + linkF)
						print("\t\t[star]"+ valueT)
	print("\t}")

""" method of step 2: insert the urls in instance """
def searchGoogle(tweet, complementaire, inst, nbEtoiles):

	resultFacebook = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "facebook", False)
	resultLinkedin = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "linkedin", False)
	resultFacebookC = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "facebook", True)
	resultLinkedinC = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "linkedin", True)

	for link in resultFacebook:
		new_url = sFacebook.standardUrl(link)
		if not sFacebook.certifiatePage(new_url) and (not inst.existFacebookPersonLink(new_url)):
			inst.addFacebookPersonLink((new_url, nbEtoiles))

	for link in resultLinkedin:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None) and not inst.existLinkedinPersonLink(new_url):
			inst.addLinkedinPersonLink((new_url,nbEtoiles))

	for link,desc in resultFacebookC:
		new_url = sFacebook.standardUrl(link)
		if sFacebook.certifiatePage(new_url) and (not inst.existFacebookCompanyLink(new_url)):
			inst.addFacebookCompanyLink((new_url, nbEtoiles))

	for link,desc in resultLinkedinC:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None) and not inst.existLinkedinCompanyLink(new_url):
			inst.addLinkedinCompanyLink((new_url,nbEtoiles))

""" method of step 2 : search all corresponding facebook """
def searchFacebook(tweet, inst):
	for link,desc in inst.linkFacebookPerson:
		compte = sFacebook.findFacebook(tweet.userSurname, tweet.userFirstname, link)
		value = matchCompteFacebookPersonTweet(tweet, compte)
		inst.addAccountFacebookPerson((link, compte, value))

""" method of step 2: search all homonymes not already found, beginning on the first link"""
def searchFacebookHomonymes(tweet, inst, time_limit=30):

	""" we instanciate the first link """
	link = inst.linkFacebookPerson[0][0]

	compte = sFacebook.findFacebook(tweet.userSurname, tweet.userFirstname, link)

	#Initialize
	urls = compte.homonymes
	accounts = []
	accounts.append(compte)

	"""Time limit"""
	start_time = time.time()

	""" while urls not empty and time limit not attain """
	while (len(urls) > 0) & (time.time()-start_time < time_limit):

		for url in urls:

			if not inst.existFacebookPersonLink(url):

				""" Scrapping limit """
				time.sleep(2)
				c = sFacebook.findFacebook(val.userSurname , val.userFirstname , url)

				""" we add 0 because we didn't get the link with geodatas """
				inst.addFacebookPersonLink((url,0))
				value = matchCompteFacebookPersonTweet(tweet, c)
				inst.addAccountFacebookPerson((url, c, value))

				accounts.append(c)

		urls = []
				
		""" we continue with the homonymes of the news accounts"""
		for c in accounts:

			""" we only add new urls """
			for new_url in c.homonymes:
				if (not inst.existFacebookPersonLink(new_url)) & (new_url not in urls):
					print(new_url)
					urls.append(new_url)

				analyser = TextAnalyser()

""" method of step 3+4 : search all corresponding linkedin """
def searchLinkedin(tweet, inst):
	manager = SeleniumManager(3)
	search = sLinkedin.SearcherLinkedin(manager)

	for link,nbStars in inst.linkLinkedinPerson:
		compte = search.findLinkedin(tweet.userSurname, tweet.userFirstname, link, "")

		""" the first number of star in accountLinkedin is the relation facebook-linkedin, 
			the second star is the conjonction with the tweet"""

		value = matchCompteLinkedinPersonTweet(tweet, compte)
		inst.addAccountLinkedinPerson((link, "", compte, 0, value))

	manager.driver_quit()
	

""" method of step 3+4 : matching compte/facebook and return a value with the degree of matching"""
def matchCompteFacebookPersonTweet(tweet, compte):
	""" Initialize """
	analyser = TextAnalyser()
	return len(analyser.getMatchingNouns(tweet.synthese(), compte.synthese()))

""" method of step 4 : matching compte/tweet and return a value with the degree of matching"""
def matchCompteLinkedinPersonTweet(tweet, compte):
	""" Initialize """
	analyser = TextAnalyser()
	return len(analyser.getMatchingNouns(tweet.synthese(), compte.synthesePerson()))

""" method of step 4 : matching comptes and return a value with the degree of matching"""
def matchCompteLinkedinCompteFacebook(tweet, compteLinkedin, compteFacebook):
	""" Initialize """
	analyser = TextAnalyser()
	return len(analyser.getMatchingNouns(compteFacebook.synthese(), compteLinkedin.synthesePerson()))

""" method of step 3+4: search all homonymes linkedin not already found, beginning on the first link"""
def searchLinkedinLinked(tweet, inst, compteF):

	""" Initialize """
	analyser = TextAnalyser()
	manager = SeleniumManager(3)
	search = sLinkedin.SearcherLinkedin(manager)

	""" search by propernouns give +4 star to the link facebook-linkedin"""
	propernounsExp = list(analyser.getPropersNounsFromList(compteF.nomsExperiences))
	propernounsEtud = list(analyser.getPropersNounsFromList(compteF.nomsEtudes))

	for val in propernounsExp:
		list_urls = search.findLinkedins(tweet.userSurname, tweet.userFirstname, ecole=None, entreprise=val)
		for url in list_urls:
			if not inst.existLinkedinPersonLink(url):
				inst.addLinkedinPersonLink((url,0))
				compte = search.findLinkedin(tweet.userSurname, tweet.userFirstname, url, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, compte)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, compte, compteF)
				inst.addAccountLinkedinPerson((url, compteF.url, compte, valueFacebookLinkedin+4, valueTweet))

	for val in propernounsEtud:
		list_urls = search.findLinkedins(tweet.userSurname, tweet.userFirstname, ecole=val, entreprise=None)
		for url in list_urls:
			if not inst.existLinkedinPersonLink(url):
				inst.addLinkedinPersonLink((url,0))
				compte = search.findLinkedin(tweet.userSurname, tweet.userFirstname, url, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, compte)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, compte, compteF)
				inst.addAccountLinkedinPerson((url, compteF.url, compte, valueFacebookLinkedin+4, valueTweet))

	""" search by keywords give +2 star to the link facebook-linkedin"""

	nouns = [tweet.userFirstname, tweet.userSurname]
	if len(compteF.nomsExperiences)>0:
		nouns.extend(analyser.getNomsCommuns(compteF.nomsExperiences[0]))
	else:
		if len(compteF.nomsEtudes)>0:
			nouns.extend(analyser.getNomsCommuns(compteF.nomsEtudes[0]))

	""" we don't search with just name and surname, too much datas """
	if len(nouns)>2:
		set_urls = search.findLinkedinsByKeywordsByList(nouns)
		list_urls = list(set_urls)
		for val in list_urls:
			if not inst.existLinkedinPersonLink(val):
				inst.addLinkedinPersonLink((val,0))
				compte = search.findLinkedin(tweet.userSurname, tweet.userFirstname, val, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, compte)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, compte, compteF)
				inst.addAccountLinkedinPerson((val, compteF.url, compte, valueFacebookLinkedin+2, valueTweet))

	manager.driver_quit()


if __name__ == '__main__':

	""" First step, Initialize : instanciation and determinate type of author for a majority of the tweet """
	reader = Datas()
	reader.readFromCsv("res/iteration_500.csv")

	""" Second step: Search : instanciate for Person or Indeterminate tweets, the result for search on linkedin and facebook"""
	tweets = reader.getPeopleTweets(True)

	for val in tweets[3:4]:

		search(val)


