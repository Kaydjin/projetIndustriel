#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelsProject.tweet import *
import sys
import csv
import string
import re
from utils.utils import *

""" Transform initial datas(streaming, list[tweet], csv) in a normalized class """
class Datas:

	def __init__(self):
		self.corpus_company = []
		self.firstnames = []
		self.tweets = []
		self.initCorpusCompany()
		self.initCorpusFirstnames()

	def initCorpusCompany(self):
		""" open the file of the corpus_company and instanciate """
		with open("res/corpus_company.txt") as f:
			for line in f:
				if line.strip() != "":
					self.corpus_company.append(line.strip())

	def initCorpusFirstnames(self):
		fname = "res/prenoms.csv"

		""" code to open the csv file change with python version """
		file = ""
		if(sys.version_info > (3,0)):
			file = open(fname, "rt",encoding = "utf8")
		else:
			file = open(fname, "rt")

		try:	
			reader = csv.DictReader(file, delimiter=',')

			#we transform the firstname in a lower format
			for row in reader:
				self.firstnames.append(row.get('prenom').lower())

		finally:
			file.close()

	""" we obtain the datas from a flux """
	def addData(self, tweet):
		self.tweets.append(tweet)
		self.addTypeOfAuteurAndName(tweet)

	""" we obtain the datas by block """
	def addDatas(self, tweets):
		for val in tweets:
			self.addData(val)

	""" we obtain the datas from a csv """
	def readFromCsv(self, fileNameCsv):
		#instanciate
		if(sys.version_info > (3,0)):
			file = open(fileNameCsv, "rt",encoding = "utf8")
		else:
			file = open(fileNameCsv, "rt")

		try:
			reader = csv.DictReader(file, delimiter=',')

			#for all elements 
			for row in reader:

				""" Determinate if the data is pertinent or not """
				pertinent = False
				if 'VRAI' in row.get('Pertinent'):
					pertinent = True

				self.tweets.append(Tweet(row.get('tweet_id'),row.get('tweet_created_at'),d(row.get('tweet_text')),
										d(row.get('hashtags')),row.get('tweet_quoted_status_id'),d(row.get('tweet_mtion')),
										pertinent,row.get('proba_pertinence'),row.get('user_id'),d(row.get('user_screenname')),
										d(row.get('user_name')),d(row.get('user_location')),d(row.get('user_description')),"", "", ""))
		finally:
			file.close()

		#for all results
		for tweet in self.tweets:
			self.addTypeOfAuteurAndName(tweet)

	""" associate the type of author - and a firstname and surname if a person- to a tweet if there is enough datas available """
	def addTypeOfAuteurAndName(self,tweet):

		determinate = False
		typeAuthor = "INDETERMINED"
		for companyWord in self.corpus_company:
			if companyWord in tweet.user_name.lower():
				typeAuthor = "COMPANY"
				determinate = True

		if not determinate:
			""" separate all the words in the name """
			for val in tweet.user_name.split(' '):

				""" test if there is a firstname in these words """
				if val.lower() in self.firstnames:
					typeAuthor = "PERSON"
					tweet.userFirstname = val.lower()
					tweet.userSurname = tweet.user_name.replace(val, "").strip()
					break

		tweet.typeAuthor = typeAuthor



	def getSomeoneTweets(self, nom, prenom, pertinent=True):
		someoneTweets = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (nom.lower() in tweet.user_name.lower())& (prenom.lower() in tweet.user_name.lower()):
				someoneTweets.append(tweet)
		return someoneTweets

	def getIndeterminatedTweets(self, pertinent=True):
		indeterminer = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuthor == "INDETERMINED"):
				indeterminer.append(tweet)
		return indeterminer

	def getPeopleTweets(self, pertinent=True):
		people = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuthor == "PERSON"):
				people.append(tweet)
		return people

	def getCompanyTweets(self, pertinent=True):
		compagnie = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuthor == "COMPANY"):
				compagnie.append(tweet)
		return compagnie


if __name__ == '__main__':

	reader = Datas()
	reader.readFromCsv("res/iteration_500.csv")
	tweets = reader.getIndeterminatedTweets(True)
	tweets = reader.getCompanyTweets(True)
	tweets.extend(reader.getCompagnieTweets(False))
	tweets = list(set(tweets))
	print(len(tweets))
	for t in tweets:
		print(t.user_name)