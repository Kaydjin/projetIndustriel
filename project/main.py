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
	accounts = []
	for tAccount in inst.accountFacebookPerson:
		accounts.append((tAccount[0], tAccount[1], matchCompteFacebookPersonTweet(tweet, tAccount[1], analyser)))
	inst.accountFacebookPerson = accounts

	""" Step seven : Keep only the five best results for the next part of the search """
	fiveBestFacebook = inst.getFiveBestAccountsFacebook()

	""" Step eight : search company datas for all experiences of facebook 5 five best accounts """
	for tAccount in fiveBestFacebook:
		for exp in tAccount[1].experiences:
			searchPersonCompanyFacebook(exp, manager)

	""" Step nine : second matching Tweet datas/5 Facebook best accounts with company datas specified """
	accounts = []
	for tAccount in fiveBestFacebook:
		accounts.append((tAccount[0], tAccount[1], matchCompteFacebookPersonTweet(tweet, tAccount[1], analyser)))
	inst.accountFacebookPerson = accounts

	""" Connect the selenium manager on a Linkedin search: operate identification on login page """
	searcherLinkedin = sLinkedin.SearcherLinkedin(manager)

	""" Step ten and twelve: search accounts from linkedin url from google + matching"""
	searchPersonLinkedin(tweet, inst, searcherLinkedin, analyser)

	""" Step eleven and twelve : search accounts by linking from facebook datas """
	for link,compte,star in fiveBestFacebook:
		searchPersonLinkedinLinked(tweet, inst, compte, searcherLinkedin, analyser)

	#show results #TODO comment
	show_result_person(inst)
	#show results #TODO comment
	show_company_person(tweet, inst, analyser)

""" Search for company tweet """
def searchCompany(tweet, manager, analyser):
	inst = Instance(tweet)

	resultFacebookC = sGoogle.search_google(nomEntreprise, "", "facebook", True)
	resultLinkedinC = sGoogle.search_google(nomEntreprise, "", "linkedin", True)

	for link,desc in resultFacebookC:
		new_url = sFacebook.standardUrl(link)
		if sFacebook.certifiatePage(new_url) and (not inst.existFacebookCompanyLink(new_url)):
			inst.addFacebookCompanyLink((new_url, 0))

	for link,desc in resultLinkedinC:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None) and not inst.existLinkedinCompanyLink(new_url):
			inst.addLinkedinCompanyLink((new_url,0))

	""" Connect the selenium manager on a Linkedin search: operate identification on login page """
	searcherLinkedin = sLinkedin.SearcherLinkedin(manager)

	""" Linkedin link in priority """
	if len(inst.linkLinkedinCompany)>0:
		# retourne un tuple (nomE, location, domaine, descriptionE)
		result = searcherLinkedin.findLinkedinCompany(inst.linkLinkedinCompany[0])
		value = len(analyser.getMatchingNouns(tweet.synthese(), result[0]+" "+result[1]+" "+result[2]+" "+result[3]))
		inst.addAccountLinkedinCompany(inst.linkLinkedinCompany[0], result, value)
	#else: TODO facebook search


""" method of step 5 : show company found"""
def show_company_person(tweet, inst, analyser):

	print("[company]")
	for link,linkF,compte,valueF,valueT in inst.accountLinkedinPerson:
		for work in compte.experiences:
			result = len(analyser.getMatchingNouns(tweet.synthese(), work.syntheseExperienceC()))
			if result > 3:
				if work.nomEntreprise=="":
					print("\t Links:"+link+" / "+linkF+" entreprise:"+work.nomExperience +" star:"+str(result))
				else:
					print("\t Links:"+link+" / "+linkF+ " / " + work.urlEntreprise)
					print("\t Entreprise:"+work.nomEntreprise +" star:"+str(result))

""" method of step 5: show only pertinent datas """
def show_result_person(inst):
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

""" Second and third step : starting urls Facebook/Linkedin + normalization of the urls found  """
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

""" Step four: Instanciate Facebook's account from the facebook urls in the instance """
def searchPersonFacebook(tweet, inst, analyser):
	for link,desc in inst.linkFacebookPerson:
		compte = sFacebook.findFacebook(tweet.userSurname, tweet.userFirstname, link)
		#initially 0 for the matching
		inst.addAccountFacebookPerson((link, compte, 0))

""" Step five : Explore and add all homonymes links for a specified time"""
def searchPersonFacebookHomonymes(tweet, inst, analyser, time_limit=30):

	""" we instanciate the first link if it exists """
	if len(inst.linkFacebookPerson)>0:
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

					""" we add 0 because we didn't get the link with geodatas, 0 for value matching initially """
					inst.addFacebookPersonLink((url,0))
					inst.addAccountFacebookPerson((url, c, 0))

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
		# retourne un tuple (nomE, location, domaine, descriptionE)
		result = searcherLinkedin.findLinkedinCompany(listeL[0])
		experience.specifyCompany(result[0], listeL[0], result[3], result[2])
	#else: TODO FACEBOOK SEARCH

""" method of step 3+4 : search all corresponding linkedin """
def searchPersonLinkedin(tweet, inst, searcher, analyser):

	for link,nbStars in inst.linkLinkedinPerson:
		compte = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, link, "")

		""" the first number of star in accountLinkedin is the relation facebook-linkedin, 
			the second star is the conjonction with the tweet"""

		value = matchCompteLinkedinPersonTweet(tweet, compte, analyser)
		inst.addAccountLinkedinPerson((link, "", compte, 0, value))
	

""" method of step 3+4 : matching compte/facebook and return a value with the degree of matching"""
def matchCompteFacebookPersonTweet(tweet, compte, analyser):
	return len(analyser.getMatchingNouns(tweet.synthese(), compte.synthese()))

""" method of step 4 : matching compte/tweet and return a value with the degree of matching"""
def matchCompteLinkedinPersonTweet(tweet, compte, analyser):
	return len(analyser.getMatchingNouns(tweet.synthese(), compte.synthesePerson()))

""" method of step 4 : matching comptes and return a value with the degree of matching"""
def matchCompteLinkedinCompteFacebook(tweet, compteLinkedin, compteFacebook, analyser):
	return len(analyser.getMatchingNouns(compteFacebook.synthese(), compteLinkedin.synthesePerson()))

""" method of step 3+4: search all homonymes linkedin not already found, beginning on the first link"""
def searchPersonLinkedinLinked(tweet, inst, compteF, searcher, analyser):

	""" search by propernouns give +4 star to the link facebook-linkedin"""
	propernounsExp = list(analyser.getPropersNounsFromList(compteF.getNamesExperiences()))
	propernounsEtud = list(analyser.getPropersNounsFromList(compteF.nomsEtudes))

	for val in propernounsExp:
		list_urls = searcher.findLinkedins(tweet.userSurname, tweet.userFirstname, ecole=None, entreprise=val)
		for url in list_urls:
			if not inst.existLinkedinPersonLink(url):
				inst.addLinkedinPersonLink((url,0))
				compte = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, url, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, compte, analyser)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, compte, compteF, analyser)
				inst.addAccountLinkedinPerson((url, compteF.url, compte, valueFacebookLinkedin+4, valueTweet))

	for val in propernounsEtud:
		list_urls = searcher.findLinkedins(tweet.userSurname, tweet.userFirstname, ecole=val, entreprise=None)
		for url in list_urls:
			if not inst.existLinkedinPersonLink(url):
				inst.addLinkedinPersonLink((url,0))
				compte = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, url, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, compte, analyser)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, compte, compteF, analyser)
				inst.addAccountLinkedinPerson((url, compteF.url, compte, valueFacebookLinkedin+4, valueTweet))

	""" search by keywords give +2 star to the link facebook-linkedin"""

	nouns = [tweet.userFirstname, tweet.userSurname]
	if len(compteF.experiences)>0:
		nouns.extend(analyser.getNomsCommuns(compteF.experiences[0].nameExperience))
	else:
		if len(compteF.nomsEtudes)>0:
			nouns.extend(analyser.getNomsCommuns(compteF.nomsEtudes[0]))

	""" we don't search with just name and surname, too much datas """
	if len(nouns)>2:
		set_urls = searcher.findLinkedinsByKeywordsByList(nouns)
		list_urls = list(set_urls)
		for val in list_urls:
			if not inst.existLinkedinPersonLink(val):
				inst.addLinkedinPersonLink((val,0))
				compte = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, val, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, compte, analyser)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, compte, compteF, analyser)
				inst.addAccountLinkedinPerson((val, compteF.url, compte, valueFacebookLinkedin+2, valueTweet))


if __name__ == '__main__':

	""" First step, Initialize : instanciation and determinate type of author for a majority of the tweet """
	reader = Datas()
	reader.readFromCsv("res/iteration_500.csv")

	""" Instanciate the manager selenium, the syntaxical analyser"""
	manager = SeleniumManager(3)
	analyser = TextAnalyser()

	""" 2-11 steps for person tweets """
	tweetsPeople = reader.getPeopleTweets(True)
	for val in tweetsPeople[19:20]:
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


