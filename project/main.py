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
from libraries import sGoogle
from libraries import sLinkedin
from libraries import sFacebook
from libraries.SNScrapping.seleniumClass.managerSelenium import *
from libraries.SNScrapping.models.accountLinkedin import *
from textAnalyser import *

""" Search for people and indeterminate tweets """
def search(tweet, manager, analyser):

	""" In all following methods the instance will be modified to incorporate the results."""
	inst = Instance(tweet)

	""" Second and third step : starting urls Facebook/Linkedin + normalization of the urls found """

	#The first search google is with location, we will add a value for the given url
	searchGoogle(tweet, tweet.user_location, inst, 2)
	#The second search google is without location, no add value for the given url
	searchGoogle(tweet, "", inst, 0)
	#show results #TODO comment
	inst.printLinks()

	""" Step four: Instanciate Facebook's account from the urls found by google """
	searchPersonFacebook(tweet, inst, analyser)

	""" Step five: Explore and add all homonymes links for a optional specified time """
	searchPersonFacebookHomonymes(tweet, inst, analyser, time_limit=30)

	""" Step six : first matching Tweet datas/Facebook accounts with only datas find on facebook page """
	for tAccount in inst.accountFacebookPerson:
		tAccount.value = matchCompteFacebookPersonTweet(tweet, tAccount.account, analyser)

	""" Step seven : Keep only the five best results for the next part of the search """
	inst.keepFiveBestAccountsFacebook()

	""" Step eight : search company datas for all experiences of facebook 5 five best accounts """
	for tAccount in inst.accountFacebookPerson:
		for exp in tAccount.account.experiences:
			searchPersonCompanyFacebook(exp, manager)

	""" Step nine : second matching Tweet/Facebook for 5 best accounts with company datas specified """
	for tAccount in inst.accountFacebookPerson:
		tAccount.value = matchCompteFacebookPersonTweet(tweet, tAccount.account, analyser)

	""" Connect the selenium manager on a Linkedin search: operate identification on login page """
	searcherLinkedin = sLinkedin.SearcherLinkedin(manager)

	""" Step ten and twelve: search accounts from linkedin url from google + matching"""
	searchPersonLinkedin(tweet, inst, searcherLinkedin, analyser)

	""" Step eleven and twelve : search accounts by linking from facebook datas + matching"""
	for tAccount in inst.accountFacebookPerson:
		searchPersonLinkedinLinked(tweet, inst, tAccount.account, searcherLinkedin, analyser)

	#show results #TODO comment
	show_result_person(inst)
	#show results #TODO comment
	show_company_person(tweet, inst, analyser)

""" method of step 5 : show company found"""
def show_company_person(tweet, inst, analyser, minCompany=3):
	print("\t[company]{")
	for val in inst.accountLinkedinPerson:
		for work in val.account.experiences:
			#account of type person, with company link with experience
			result = len(analyser.getMatchingNouns(tweet.synthese(), work.syntheseExperienceC()))
			if result >= minCompany:
				print(work.toJson())

	for val in inst.accountFacebookPerson:
		for work in val.account.experiences:
			#account of type person, with company link with experience
			result = len(analyser.getMatchingNouns(tweet.synthese(), work.syntheseExperienceC()))
			if result >= minCompany:
				print(work.toJson())
	#end
	print("\t}")

""" method of step 5: show only pertinent datas """
def show_result_person(inst, minFacebook=3, minLinkedinWithoutPair = 3, minLinkedinWithPair = 4):
	#Name person
	print("["+inst.tweet.userFirstname +" "+inst.tweet.userSurname+"]")

	""" print Facebook accounts with a minimum value of matching with the tweet """
	print("\t[Facebook]{")
	for val in inst.accountFacebookPerson:
		start_value = inst.getValueFacebookPersonLink(val.link)
		if start_value + val.valueT >= minFacebook:
			print(val.account.toJson())
	print("\t}")

	"""print Linkedin accounts with a minimum value of matching with the tweet	"""
	print("\t[Linkedin]{")
	for val in inst.accountLinkedinPerson:

		#no matching with a facebook account
		if (val.linkF=="") and (val.valueT >= minLinkedinWithoutPair):
			print(val.account.toJson())

		#matching with a facebook account
		if val.linkF!="":

			#if the matching between the facebook and linkedin account is good:
			if val.valueF >= 5:
				values = inst.getValuesAccountFacebookPerson(val.linkF)
				if values!=None:
					#value of matching facebook/Tweet
					matchFTValue = values[1]
					#value indicating the importance of the link initial
					valueInitialLink = inst.getValueFacebookPersonLink(val.linkF)

					#minimum value to print for two matching accounts.
					if (valueInitialLink!=None) and (valueInitialLink + val.valueT + matchFTValue >= minLinkedinWithPair):
						print(val.account.toJson())
			else:
				#if the matching is not good, but the linkedin account is, suppress the link before printing
				if val.valueT > minLinkedinWithoutPair:
					val.linkF = ""
					print(val.account.toJson())
	#end
	print("\t}")

""" Search for company tweet """
def searchCompany(tweet, manager, analyser):
	inst = Instance(tweet)

	resultFacebookC = sGoogle.search_google(nomEntreprise, "", "facebook", True)
	resultLinkedinC = sGoogle.search_google(nomEntreprise, "", "linkedin", True)

	for link,desc in resultFacebookC:
		new_url = sFacebook.standardUrl(link)
		if sFacebook.certifiatePage(new_url) and (not inst.existFacebookCompanyLink(new_url)):
			inst.addFacebookCompanyLink(new_url)

	for link,desc in resultLinkedinC:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None) and not inst.existLinkedinCompanyLink(new_url):
			inst.addLinkedinCompanyLink(new_url)

	""" Connect the selenium manager on a Linkedin search: operate identification on login page """
	searcherLinkedin = sLinkedin.SearcherLinkedin(manager)

	""" Linkedin link in priority """
	if len(inst.linkLinkedinCompany)>0:

		# findLinkedinCompany: return AccountCompany: domain, position, nomComplet, description
		# inst.linkLinkedinCompany[0] : we use only the first result.
		result = searcherLinkedin.findLinkedinCompany(inst.linkLinkedinCompany[0])

		value = len(analyser.getMatchingNouns(tweet.synthese(), result.toString()))

		inst.addAccountLinkedinCompany(inst.linkLinkedinCompany[0], result, valueT=value)

	#else: TODO facebook search

""" Second and third step : starting urls Facebook/Linkedin + normalization of the urls found  """
def searchGoogle(tweet, complementaire, inst, nbEtoiles):

	resultFacebook = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "facebook", False)
	resultLinkedin = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "linkedin", False)
	resultFacebookC = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "facebook", True)
	resultLinkedinC = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "linkedin", True)

	for link in resultFacebook:
		new_url = sFacebook.standardUrl(link)
		if not sFacebook.certifiatePage(new_url) and (not inst.existFacebookPersonLink(new_url)):
			inst.addFacebookPersonLink(new_url, nbEtoiles)

	for link in resultLinkedin:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None) and not inst.existLinkedinPersonLink(new_url):
			inst.addLinkedinPersonLink(new_url,nbEtoiles)

	for link,desc in resultFacebookC:
		new_url = sFacebook.standardUrl(link)
		if sFacebook.certifiatePage(new_url) and (not inst.existFacebookCompanyLink(new_url)):
			inst.addFacebookCompanyLink(new_url, nbEtoiles)

	for link,desc in resultLinkedinC:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None) and not inst.existLinkedinCompanyLink(new_url):
			inst.addLinkedinCompanyLink(new_url,nbEtoiles)

""" Step four: Instanciate Facebook's account from the facebook urls in the instance """
def searchPersonFacebook(tweet, inst, analyser):
	for tLink in inst.linkFacebookPerson:
		account = sFacebook.findFacebook(tweet.userSurname, tweet.userFirstname, tLink.link)
		inst.addAccountFacebookPerson(tLink.link, account)

""" Step five : Explore and add all homonymes links for a specified time"""
def searchPersonFacebookHomonymes(tweet, inst, analyser, time_limit=30):

	""" we instanciate the first link if it exists """
	if len(inst.linkFacebookPerson)>0:
		link = inst.linkFacebookPerson[0].link

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

					""" we add 0 because we didn't get the link with geodatas, 0 for value matching initially """
					inst.addFacebookPersonLink(url)
					inst.addAccountFacebookPerson(url, c)

					accounts.append(c)

			urls = []
					
			""" we continue with the homonymes of the news accounts"""
			for c in accounts:

				""" we only add new urls """
				for new_url in c.homonymes:
					if (not inst.existFacebookPersonLink(new_url)) & (new_url not in urls):
						print(new_url)
						urls.append(new_url)

""" Search company: search more information on the company of the experience of a person """
def searchPersonCompanyFacebook(experience, manager):
	resultFacebookC = sGoogle.search_google(experience.nameCompany, "", "facebook", True)
	resultLinkedinC = sGoogle.search_google(experience.nameCompany, "", "linkedin", True)
	listeF = []
	listeL = []
	for link,desc in resultFacebookC:
		new_url = sFacebook.standardUrl(link)
		if sFacebook.certifiatePage(new_url):
			listeF.append(new_url)

	for link,desc in resultLinkedinC:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None):
			listeL.append(new_url)

	""" Connect the selenium manager on a Linkedin search: operate identification on login page """
	searcherLinkedin = sLinkedin.SearcherLinkedin(manager)

	""" Linkedin link in priority """
	if len(listeL)>0:
		# findLinkedinCompany: return AccountCompany: domain, position, nomComplet, description
		# specifyCompany(nameCompany, urlCompany, descriptionCompany, domainCompany, geolocalizationCompany)
		result = searcherLinkedin.findLinkedinCompany(listeL[0])
		experience.specifyCompany(result.nomComplet, listeL[0], result.description, result.domain, result.position)
	#else: TODO FACEBOOK SEARCH

""" method of step 3+4 : search all corresponding linkedin """
def searchPersonLinkedin(tweet, inst, searcher, analyser):

	for tLink in inst.linkLinkedinPerson:
		account = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, tLink.link, "")
		value = matchCompteLinkedinPersonTweet(tweet, account, analyser)
		inst.addAccountLinkedinPerson(tLink.link, account, valueT=value)
	

""" method of step 3+4 : matching account/facebook and return a value with the degree of matching"""
def matchCompteFacebookPersonTweet(tweet, account, analyser):
	return len(analyser.getMatchingNouns(tweet.synthese(), account.synthese()))

""" method of step 4 : matching account/tweet and return a value with the degree of matching"""
def matchCompteLinkedinPersonTweet(tweet, account, analyser):
	return len(analyser.getMatchingNouns(tweet.synthese(), account.synthesePerson()))

""" method of step 4 : matching accounts and return a value with the degree of matching"""
def matchCompteLinkedinCompteFacebook(tweet, accountLinkedin, accountFacebook, analyser):
	return len(analyser.getMatchingNouns(accountFacebook.synthese(), accountLinkedin.synthesePerson()))

""" method of step 3+4: search all homonymes linkedin not already found, beginning on the first link"""
def searchPersonLinkedinLinked(tweet, inst, accountF, searcher, analyser):

	""" search by propernouns give +4 star to the link facebook-linkedin"""
	propernounsExp = list(analyser.getPropersNounsFromList(accountF.getNamesExperiences()))
	propernounsEtud = list(analyser.getPropersNounsFromList(accountF.nomsEtudes))

	for val in propernounsExp:
		list_urls = searcher.findLinkedins(tweet.userSurname, tweet.userFirstname, ecole=None, entreprise=val)
		for url in list_urls:
			if not inst.existLinkedinPersonLink(url):
				inst.addLinkedinPersonLink(url,0)
				account = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, url, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, account, analyser)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, account, accountF, analyser)
				inst.addAccountLinkedinPerson(url, account, accountF.url, valueFacebookLinkedin+4, valueTweet)

	for val in propernounsEtud:
		list_urls = searcher.findLinkedins(tweet.userSurname, tweet.userFirstname, ecole=val, entreprise=None)
		for url in list_urls:
			if not inst.existLinkedinPersonLink(url):
				inst.addLinkedinPersonLink(url,0)
				account = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, url, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, account, analyser)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, account, accountF, analyser)
				inst.addAccountLinkedinPerson(url, account, accountF.url, valueFacebookLinkedin+4, valueTweet)

	""" search by keywords give +2 star to the link facebook-linkedin"""

	nouns = [tweet.userFirstname, tweet.userSurname]
	if len(accountF.experiences)>0:
		nouns.extend(analyser.getNomsCommuns(accountF.experiences[0].nameExperience))
	else:
		if len(accountF.nomsEtudes)>0:
			nouns.extend(analyser.getNomsCommuns(accountF.nomsEtudes[0]))

	""" we don't search with just name and surname, too much datas """
	if len(nouns)>2:
		set_urls = searcher.findLinkedinsByKeywordsByList(nouns)
		list_urls = list(set_urls)
		for val in list_urls:
			if not inst.existLinkedinPersonLink(val):
				inst.addLinkedinPersonLink((val,0))
				account = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, val, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, account, analyser)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, account, accountF, analyser)
				inst.addAccountLinkedinPerson(val, account, accountF.url, valueFacebookLinkedin+2, valueTweet)


if __name__ == '__main__':

	""" First step, Initialize : instanciation and determinate type of author for a majority of the tweet """
	reader = Datas()
	reader.readFromCsv("res/iteration_500.csv")

	""" Instanciate the manager selenium, the syntaxical analyser"""
	manager = SeleniumManager(3)
	analyser = TextAnalyser()

	""" 2-11 steps for person tweets """
	tweetsPeople = reader.getPeopleTweets(True)
	for val in tweetsPeople:
		search(val, manager, analyser)

	""" 2-11 steps for inderterminate tweets """
	tweetsIndeterminate = reader.getIndeterminatedTweets(True)
	for val in tweetsIndeterminate:
		search(val, manager, analyser)

	""" 2-11 steps for company tweets """
	tweetsCompany = getCompanyTweets(True)
	#for val in tweetsCompany:
		#searchCompany(val, manager, analyser)

	""" Kill driver selenium """
	manager.driver_quit()


