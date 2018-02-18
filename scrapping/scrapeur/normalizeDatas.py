#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelsProject.tweet import *
import sys
import string
import re

""" Transform initial datas(streaming, list[tweet], csv) in a normalized class """
class Datas:

	def __init__(self):
		self.corpus_company = []
		self.firstnames = []
		self.tweets = []
		initCorpusCompany()
		initCorpusFirstnames()

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
			for row in reader2:
				self.firstnames.append(row.get('prenom').lower())

		finally:
			file.close()

	def read(self, fileNameCsv):

		try:
			#instanciate
			if(sys.version_info > (3,0)):
				file = open(self.fileNameCsv, "rt",encoding = "utf8")
			else:
				file = open(self.fileNameCsv, "rt")
			reader = csv.DictReader(file, delimiter=',')

			#for all elements 
			for row in reader:

				""" Determinate if the data is pertinent or not """
				pertinent = False
				if 'VRAI' in row.get('Pertinent'):
					pertinent = True

				self.tweets.append(Tweet(row.get('tweet_id'),
											row.get('tweet_created_at'),
											row.get('tweet_text'),
											row.get('hashtags'),
											row.get('tweet_quoted_status_id'),
											row.get('tweet_mtion'),
											pertinent,
											row.get('proba_pertinence'),
											row.get('user_id'),
											row.get('user_screenname'),
											row.get('user_name'),
											row.get('user_location'),
											row.get('user_description'),
											"", "", ""
											))

		finally:
			file.close()
			file2.close()

	""" associate the type of author - and a firstname and surname if a person- to a tweet if there is enough datas available """
	def addTypeOfAuteurAndName(self,tweet):

		determinate = False
		typeAuthor = "INDETERMINED"
		for companyWord in corpus_company:
			if companyWord in tweet.user_name.lower():
				typeAuthor = "COMPANY"
				determinate = True

		if not determinate:
			""" separate all the words in the name """
			for val in tweet.user_name.split(' '):

				""" test if there is a firstname in these words """
				if val.lower() in prenoms:
					typeAuthor = "PERSON"
					tweet.userFirstname = val.lower()
					tweet.userSurname = row.get('user_name').replace(val, "").strip()
					break

		tweet.typeAuthor = typeAuthor



	def getSomeoneTweets(self, nom, prenom, pertinent):
		someoneTweets = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (nom.lower() in tweet.userName.lower())& (prenom.lower() in tweet.userName.lower()):
				someoneTweets.append(tweet)
		return someoneTweets

	def getIndeterminatedTweets(self, pertinent):
		indeterminer = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuteur == "INDETERMINED"):
				indeterminer.append(tweet)
		return indeterminer

	def getPeopleTweets(self, pertinent):
		people = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuteur == "PERSON"):
				people.append(tweet)
		return people

	def getCompagnieTweets(self, pertinent):
		compagnie = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuteur == "COMPANY"):
				compagnie.append(tweet)
		return compagnie


# test de la class TweetCSVReader
if __name__ == '__main__':

	reader = Datas()
	reader.read("res/iteration_500.csv")
	
	#tweets = reader.getIndeterminatedTweets(True)
	tweets = reader.getCompagnieTweets(True)
	tweets.extend(reader.getCompagnieTweets(False))
	tweets = list(set(tweets))
	for t in tweets:
		print(t.user_name)