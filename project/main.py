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
from utils.utils import *

""" Search for people and indeterminate tweets """
def search(tweet, searcherLinkedin, searcherFacebook, analyser):

	""" In all following methods the instance will be modified to incorporate the results."""
	inst = Instance(tweet)

	""" Second and third step : starting urls Facebook/Linkedin + normalization of the urls found """

	#The first search google is with location, we will add a value for the given url
	print("STEP 2-3: google+normalize urls")
	searchGoogle(tweet, tweet.user_location, inst, 2)
	#The second search google is without location, no add value for the given url
	searchGoogle(tweet, "", inst, 0)
	#show results #TODO comment
	inst.printLinks()

	""" Step four: Instanciate Facebook's account from the urls found by google """
	print("STEP 4: Facebook")
	searchPersonFacebook(tweet, inst, analyser)

	""" Step five: Explore and add all homonymes links for a optional specified time """
	print("STEP 5: Homonymes Facebook")
	searchPersonFacebookHomonymes(tweet, inst, analyser, time_limit=30)

	""" Step six : first matching Tweet datas/Facebook accounts with only datas find on facebook page """
	print("STEP 6: First match facebook")
	for tAccount in inst.accountFacebookPerson:
		tAccount.value = matchCompteFacebookPersonTweet(tweet, tAccount.account, analyser)

	""" Step seven : Keep only the five best results for the next part of the search """
	print("STEP 7: Keep best facebook")
	inst.keepFiveBestAccountsFacebook()

	""" Step eight : search company datas for all experiences of facebook 5 five best accounts """
	print("STEP 8: Find company linked to 5 best facebook account")
	for tAccount in inst.accountFacebookPerson:
		for exp in tAccount.account.experiences:
			try:
				searchPersonCompanyFacebook(exp, searcherLinkedin, searcherFacebook)
			except ValueError as e:
				print(str(e))

	""" Step nine : second matching Tweet/Facebook for 5 best accounts with company datas specified """
	print("STEP 9: Second matching facebook")
	for tAccount in inst.accountFacebookPerson:
		tAccount.value = matchCompteFacebookPersonTweet(tweet, tAccount.account, analyser)

	""" Step ten and twelve: search accounts from linkedin url from google + matching"""
	print("STEP 10-12: accounts linkedin + matching")
	searchPersonLinkedin(tweet, inst, searcherLinkedin, analyser)

	""" Step eleven and twelve : search accounts by linking from facebook datas + matching"""
	print("STEP 11-12: accounts Linkedin(link facebook) + matching")
	for tAccount in inst.accountFacebookPerson:
		searchPersonLinkedinLinked(tweet, inst, tAccount.account, searcherLinkedin, analyser)

	#show results #TODO comment
	show_result_person(inst)
	#show results #TODO comment
	show_company_person(tweet, inst, analyser)

	return inst

""" method of step 5 : show company found"""
def show_company_person(tweet, inst, analyser, minCompany=0):
	print("\t[company]{")
	for val in inst.accountLinkedinPerson:
		for work in val.account.experiences:
			#account of type person, with company link with experience
			result = len(analyser.getMatchingNouns(tweet.synthese(), work.syntheseExperienceC()))
			if result >= minCompany:
				print(work.toJson()+"[valueT]"+str(result))

	for val in inst.accountFacebookPerson:
		for work in val.account.experiences:
			#account of type person, with company link with experience
			result = len(analyser.getMatchingNouns(tweet.synthese(), work.syntheseExperienceC()))
			if result >= minCompany:
				print(work.toJson()+"[valueT]"+str(result))
	#end
	print("\t}")

""" method to save the result """ 
def instanceToCsv(analyser, minCompany=0,minFacebook=0, minLinkedinWithoutPair=0, minLinkedinWithPair=0,minMatchFacebookLinkedin=0):
	if inst.tweet.typeAuthor=="PERSON":
		return instanceToCsvPerson(analyser, inst, minCompany,minFacebook, minLinkedinWithoutPair, minLinkedinWithPair, minMatchFacebookLinkedin)
	if inst.tweet.typeAuthor=="INDETERMINED":
		res = instanceToCsvPerson(analyser, inst, minCompany,minFacebook, minLinkedinWithoutPair, minLinkedinWithPair, minMatchFacebookLinkedin)
		return res.extend(instanceToCsvCompany(inst, minCompany))
	if inst.tweet.typeAuthor=="COMPANY":
		return instanceToCsvCompany(inst, minCompany)

def instanceToCsvPerson(analyser, inst, minCompany,minFacebook, minLinkedinWithoutPair, minLinkedinWithPair, minMatchFacebookLinkedin):
	rows = []

	#FACEBOOK
	for val in inst.accountFacebookPerson:
		start_value = inst.getValueFacebookPersonLink(val.link)
		if start_value + val.valueT >= minFacebook:
			atleastone = False
			for work in val.account.experiences:
				result = len(analyser.getMatchingNouns(inst.tweet.synthese(), work.syntheseExperienceC()))
				if result >= minCompany:
					atleastone = True
					rows.append(formLine(inst, val.link, "", work.positionCompany, 
						work.domainCompany, work.nameCompany, work.urlCompany, val.valueT, result))

			#if no company match we only form a row for the facebook account
			if not atleastone:
				rows.append(formLine(inst, val.link, "", "", "", "", "", val.valueT, ""))

	#LINKEDIN
	for val in inst.accountLinkedinPerson:

		#no matching with a facebook account
		if (val.linkF=="") and (val.valueT >= minLinkedinWithoutPair):
			atleastone = False
			for work in val.account.experiences:
				result = len(analyser.getMatchingNouns(inst.tweet.synthese(), work.syntheseExperienceC()))
				if result >= minCompany:
					atleastone = True
					rows.append(formLine(inst, "", val.link, work.geolocalisation, 
						work.domaineEntreprise, work.nomEntreprise, work.urlEntreprise, val.valueT, result))

			#if no company match we only form a row for the linkedin account
			if not atleastone:
				rows.append(formLine(inst, "", val.link, "", "", "", "", val.valueT, ""))

		#matching with a facebook account
		if val.linkF!="":

			#if the matching between the facebook and linkedin account is good:
			if val.valueF >= minMatchFacebookLinkedin:
				values = inst.getValuesAccountFacebookPerson(val.linkF)
				if values!=None:
					#value of matching facebook/Tweet
					matchFTValue = values[1]
					#value indicating the importance of the link initial
					valueInitialLink = inst.getValueFacebookPersonLink(val.linkF)

					#minimum value to print for two matching accounts.
					if (valueInitialLink!=None) and (valueInitialLink + val.valueT + matchFTValue >= minLinkedinWithPair):
						atleastone = False
						for work in val.account.experiences:
							result = len(analyser.getMatchingNouns(inst.tweet.synthese(), work.syntheseExperienceC()))
							if result >= minCompany:
								atleastone = True
								rows.append(formLine(inst, val.linkF, val.link, work.geolocalisation, 
									work.domaineEntreprise, work.nomEntreprise, work.urlEntreprise, val.valueT+matchFTValue, result))

						#if no company match we only form a row for the linkedin account
						if not atleastone:
							rows.append(formLine(inst, val.linkF, val.link, "", "", "", "", val.valueT+matchFTValue, ""))
			else:
				#if the matching is not good, but the linkedin account is, suppress the link before printing
				if val.valueT > minLinkedinWithoutPair:
					rows.append(formLine(inst, "", val.link, "", "", "", "", val.valueT, ""))

	return rows



def formLine(inst, accountUrl, accountUrl2, companyPos, companyName, companyDomain, companyUrl, accountsLinkedValue, companyValue):
	tid = inst.tweet.tweet_id
	uid = inst.tweet.user_id
	tauth = inst.tweet.typeAuthor
	name = inst.tweet.user_name
	screename = inst.tweet.user_screenname
	text = inst.tweet.tweet_text
	location = inst.tweet.user_location
	desc = inst.tweet.user_description
	pert = inst.tweet.pertinent
	return (tid, uid, pert, tauth, e(name), e(screename), e(text), e(location), e(desc), 
		accountUrl, accountUrl2, e(companyPos), e(companyName), e(companyDomain), companyUrl, accountsLinkedValue, companyValue)


def instanceToCsvCompany(inst, minCompany):
	rows = []
	"""print Facebook company accounts with a minimum value of matching with the tweet	"""
	for val in inst.accountFacebookCompany:
		if val.valueT >= minCompany:
			rows.append(formLine(inst, "", "", val.account.position, val.account.domaine, val.account.nomComplet, val.account.url, "", val.valueT))

	"""print Linkedin company accounts with a minimum value of matching with the tweet	"""
	for val in inst.accountLinkedinCompany:
		if val.valueT >= minCompany:
			rows.append(formLine(inst, "", "", val.account.position, val.account.domaine, val.account.nomComplet, val.account.url, "", val.valueT))

	return rows

""" method of step 5: show only pertinent datas """
def show_result_company(inst, minCompany=0):

	"""print Facebook company accounts with a minimum value of matching with the tweet	"""
	print("\t[Facebook]{")
	for val in inst.accountFacebookPerson:
		if val.valueT >= minCompany:
			print(val.account.toJson()+"[valueT]"+str(val.valueT))

	"""print Linkedin company accounts with a minimum value of matching with the tweet	"""
	print("\t[Linkedin]{")
	for val in inst.accountLinkedinPerson:
		if val.valueT >= minCompany:
			print(val.account.toJson()+"[valueT]"+str(val.valueT))

""" method of step 5: show only pertinent datas """
def show_result_person(inst, minFacebook=0, minLinkedinWithoutPair = 0, minLinkedinWithPair = 0, minMatchFacebookLinkedin = 0):
	#Name person
	print("["+inst.tweet.userFirstname +" "+inst.tweet.userSurname+"]")

	""" print Facebook accounts with a minimum value of matching with the tweet """
	print("\t[Facebook]{")
	for val in inst.accountFacebookPerson:
		start_value = inst.getValueFacebookPersonLink(val.link)
		if start_value + val.valueT >= minFacebook:
			print(val.account.toJson()+"[valueT]"+str(val.valueT))
	print("\t}")

	"""print Linkedin accounts with a minimum value of matching with the tweet	"""
	print("\t[Linkedin]{")
	for val in inst.accountLinkedinPerson:

		#no matching with a facebook account
		if (val.linkF=="") and (val.valueT >= minLinkedinWithoutPair):
			print(val.account.toJson()+"[valueT]"+str(val.valueT))

		#matching with a facebook account
		if val.linkF!="":

			#if the matching between the facebook and linkedin account is good:
			if val.valueF >= minMatchFacebookLinkedin:
				values = inst.getValuesAccountFacebookPerson(val.linkF)
				if values!=None:
					#value of matching facebook/Tweet
					matchFTValue = values[1]
					#value indicating the importance of the link initial
					valueInitialLink = inst.getValueFacebookPersonLink(val.linkF)

					#minimum value to print for two matching accounts.
					if (valueInitialLink!=None) and (valueInitialLink + val.valueT + matchFTValue >= minLinkedinWithPair):
						print(val.account.toJson()+"[valueT]"+str(val.valueT)+"[valueF]"+str(val.valueF))
			else:
				#if the matching is not good, but the linkedin account is, suppress the link before printing
				if val.valueT > minLinkedinWithoutPair:
					val.linkF = ""
					print(val.account.toJson()+"[valueT]"+str(val.valueT))
	#end
	print("\t}")

""" Search for company tweet """
def searchCompany(tweet, searcherLinkedin, searcherFacebook, analyser):
	inst = Instance(tweet)

	resultFacebookC = sGoogle.search_google(tweet.user_name, "", "facebook", True)
	resultLinkedinC = sGoogle.search_google(tweet.user_name, "", "linkedin", True)
	
	for link,desc in resultFacebookC:
		new_url = sFacebook.standardUrl(link)
		if (new_url != None) and sFacebook.certifiatePage(new_url) and (not inst.existFacebookCompanyLink(new_url)):
			inst.addFacebookCompanyLink(new_url)

	for link,desc in resultLinkedinC:
		new_url = sLinkedin.standardUrl(link, company=True)
		if (new_url != None) and (not inst.existLinkedinCompanyLink(new_url)):
			inst.addLinkedinCompanyLink(new_url)

	""" Linkedin link in priority """
	if len(inst.linkLinkedinCompany)>0:

		# findLinkedinCompany: return AccountCompany: domain, position, nomComplet, description
		# inst.linkLinkedinCompany : we keep only the best result

		val = 0
		account = None
		for tLink in inst.linkLinkedinCompany:
			try:
				accountCompany = searcherLinkedin.findLinkedinCompany(tLink.link)
				value = len(analyser.getMatchingNouns(tweet.synthese(), accountCompany.toString()))
				if (accountCompany!=None) and (value >= val):
					account = accountCompany
					val = value
			except ValueError as e:
				print(str(e))

		if account!=None:
			inst.addAccountLinkedinCompany(account.url, accountCompany, valueT=val)
	#else: TODO facebook search

	return inst

""" Second and third step : starting urls Facebook/Linkedin + normalization of the urls found  """
def searchGoogle(tweet, complementaire, inst, nbEtoiles):

	resultFacebook = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "facebook", False)
	resultLinkedin = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "linkedin", False)
	resultFacebookC = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "facebook", True)
	resultLinkedinC = sGoogle.search_google(tweet.userFirstname  + " " + tweet.userSurname, complementaire, "linkedin", True)

	for link in resultFacebook:
		new_url = sFacebook.standardUrl(link)
		boolean = sFacebook.certifiatePage(new_url)
		if (boolean != None ) and (not boolean) and (not inst.existFacebookPersonLink(new_url)):
			inst.addFacebookPersonLink(new_url, nbEtoiles)

	for link in resultLinkedin:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None) and not inst.existLinkedinPersonLink(new_url):
			inst.addLinkedinPersonLink(new_url,nbEtoiles)

	for link,desc in resultFacebookC:
		new_url = sFacebook.standardUrl(link)
		boolean = sFacebook.certifiatePage(new_url)
		if (boolean != None ) and boolean and (not inst.existFacebookCompanyLink(new_url)):
			inst.addFacebookCompanyLink(new_url, nbEtoiles)

	for link,desc in resultLinkedinC:
		new_url = sLinkedin.standardUrl(link)
		if (new_url != None) and not inst.existLinkedinCompanyLink(new_url):
			inst.addLinkedinCompanyLink(new_url,nbEtoiles)

""" Step four: Instanciate Facebook's account from the facebook urls in the instance """
def searchPersonFacebook(tweet, inst, analyser):
	for tLink in inst.linkFacebookPerson:
		account = sFacebook.findFacebook(tweet.userSurname, tweet.userFirstname, tLink.link)
		if account != None:
			inst.addAccountFacebookPerson(tLink.link, account)

""" Step five : Explore and add all homonymes links for a specified time"""
def searchPersonFacebookHomonymes(tweet, inst, analyser, time_limit=30):

	""" we use the first available account to find the others """
	if len(inst.linkFacebookPerson)>0:

		index = 0
		found = False
		while not found:
			link = inst.linkFacebookPerson[index].link
			compte = sFacebook.findFacebook(tweet.userSurname, tweet.userFirstname, link)
			index = index + 1
			if compte!=None:
				found = True
			else:
				#No account to start with
				if index==len(inst.linkFacebookPerson):
					return

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
					if c != None:
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
def searchPersonCompanyFacebook(experience, searcherLinkedin, searcherFacebook):
	if experience==None:
		return 

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

	""" Only search of company with linkedin, take only the first company found for the moment TODO """
	if len(listeL)>0:
		""" Connect the selenium manager on a Linkedin search: operate identification on login page """
		result = searcherLinkedin.findLinkedinCompany(listeL[0])
		experience.specifyCompany(result.nomComplet, listeL[0], result.description, result.domain, result.position)
	else:
		if (searcherFacebook!=None) and (len(listeF)>0):
			result = searcherFacebook.scrappingProfilEntreprise(experience.nameCompany, listeF[0])
			experience.specifyCompany(result.nomComplet, listeF[0], result.description, result.domain, result.position)

""" method of step 3+4 : search all corresponding linkedin """
def searchPersonLinkedin(tweet, inst, searcher, analyser):

	for tLink in inst.linkLinkedinPerson:
		try:
			account = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, tLink.link, "")
			value = matchCompteLinkedinPersonTweet(tweet, account, analyser)
			inst.addAccountLinkedinPerson(tLink.link, account, valueT=value)
		except ValueError as e:
			print(str(e))
	

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
	if accountF==None:
		return 

	""" search by propernouns give +4 star to the link facebook-linkedin"""
	propernounsExp = list(analyser.getPropersNounsFromList(accountF.getNamesExperiences()))
	propernounsEtud = list(analyser.getPropersNounsFromList(accountF.nomsEtudes))

	print("Search linked linkedin by proper nouns in work experience")
	for val in propernounsExp:
		list_urls = searcher.findLinkedins(tweet.userSurname, tweet.userFirstname, ecole=None, entreprise=val)
		for url in list_urls:
			if not inst.existLinkedinPersonLink(url):
				try:
					inst.addLinkedinPersonLink(url,0)
					account = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, url, "")
					valueTweet = matchCompteLinkedinPersonTweet(tweet, account, analyser)
					valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, account, accountF, analyser)
					inst.addAccountLinkedinPerson(url, account, accountF.url, valueFacebookLinkedin+4, valueTweet)
				except ValueError as e:
					print(str(e))

	print("Search linked linkedin by proper nouns in studies")
	for val in propernounsEtud:
		list_urls = searcher.findLinkedins(tweet.userSurname, tweet.userFirstname, ecole=val, entreprise=None)
		for url in list_urls:
			if not inst.existLinkedinPersonLink(url):
				try:
					inst.addLinkedinPersonLink(url,0)
					account = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, url, "")
					valueTweet = matchCompteLinkedinPersonTweet(tweet, account, analyser)
					valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, account, accountF, analyser)
					inst.addAccountLinkedinPerson(url, account, accountF.url, valueFacebookLinkedin+4, valueTweet)
				except ValueError as e:
					print(str(e))

	""" search by keywords give +2 star to the link facebook-linkedin"""
	"""print("Search linked linkedin by nouns in first experiences and studies")
	nouns = [tweet.userFirstname, tweet.userSurname]
	if len(accountF.experiences)>0:
		nouns.extend(analyser.getNomsCommuns(accountF.experiences[0].nameExperience))
	else:
		if len(accountF.nomsEtudes)>0:
			nouns.extend(analyser.getNomsCommuns(accountF.nomsEtudes[0]))"""

	""" we don't search with just name and surname, too much datas """
	"""if len(nouns)>2:
		set_urls = searcher.findLinkedinsByKeywordsByList(nouns)
		list_urls = list(set_urls)
		for val in list_urls:
			if not inst.existLinkedinPersonLink(val):
				inst.addLinkedinPersonLink((val,0))
				account = searcher.findLinkedin(tweet.userSurname, tweet.userFirstname, val, "")
				valueTweet = matchCompteLinkedinPersonTweet(tweet, account, analyser)
				valueFacebookLinkedin = matchCompteLinkedinCompteFacebook(tweet, account, accountF, analyser)
				inst.addAccountLinkedinPerson(val, account, accountF.url, valueFacebookLinkedin+2, valueTweet)"""


if __name__ == '__main__':

	""" First step, Initialize : instanciation and determinate type of author for a majority of the tweet """
	reader = Datas()
	reader.readFromCsv("res/iteration_500.csv")

	""" Instanciate the manager selenium"""
	manager = SeleniumManager(3)
	#managerFacebook = SeleniumManager(3)

	""" Connect the selenium manager on a Linkedin search: operate identification on login page """
	searcherLinkedin = sLinkedin.SearcherLinkedin(manager)
	searcherFacebook = None
	#searcherFacebook = sFacebook.SearcherFacebook_Selenium(managerFacebook)

	""" Instanciate corpus syntaxical matching class """
	analyser = TextAnalyser()

	instances = []

	""" 2-11 steps for person tweets """
	tweetsPeople = reader.getPeopleTweets(True)
	for val in tweetsPeople:
		instances.append(search(val, searcherLinkedin, searcherFacebook, analyser))

	""" 2-11 steps for inderterminate tweets """
	tweetsIndeterminate = reader.getIndeterminatedTweets(True)
	for val in tweetsIndeterminate:
		instances.append(search(val, searcherLinkedin, searcherFacebook, analyser))
		instances.append(searchCompany(val, searcherLinkedin, searcherFacebook, analyser))

	""" 2-11 steps for company tweets """
	tweetsCompany = reader.getCompanyTweets(True)
	for val in tweetsCompany:
		instances.append(searchCompany(val, searcherLinkedin, searcherFacebook, analyser))

	""" Kill driver selenium """
	manager.driver_quit()

	""" put results in csv """
	fname = "resultats.csv"
	fname2 = "resultats_pertinent.csv"
	if sys.version_info < (3, 0):
		file = open(fname, "wb")
		file2 = open(fname2, "wb")
	else:
		file = open(fname, "w")
		file2 = open(fname2, "w")

	try:
		writer = csv.writer(file)
		writer2 = csv.writer(file2)
		writer.writerow(("tweet_id", "user_id", "pertinence", "type_author",
				 "name", "screename", "tweet_text", "tweet_location",
				 "tweet_description", "url_facebook", "url_linkedin","company_location", 
				 "company_name", "company_domain", "company_url", "match_social_network", "match_company"))
		writer2.writerow(("tweet_id", "user_id", "pertinence", "type_author",
				 "name", "screename", "tweet_text", "tweet_location",
				 "tweet_description", "url_facebook", "url_linkedin","company_location", 
				 "company_name", "company_domain", "company_url", "match_social_network", "match_company"))

		""" Transform all the instances in tuple of format csv """
		for inst in instances:
			rows = instanceToCsv(analyser, minCompany=0,minFacebook=0, minLinkedinWithoutPair=0, minLinkedinWithPair=0,minMatchFacebookLinkedin=6)
			if rows!=None:
				for row in rows:
					writer.writerow(row)
			rows = instanceToCsv(analyser, minCompany=3,minFacebook=3, minLinkedinWithoutPair=3, minLinkedinWithPair=5,minMatchFacebookLinkedin=6)
			if rows!=None:
				for row in rows:
					writer2.writerow(row)
	finally:
		file.close()
		file2.close()
	


