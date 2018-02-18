#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelsProject.tweet import *
import sys
import csv
import string
import re

class Reader:

	def __init__(self, fileNameCsv):
		self.fileNameCsv = fileNameCsv
		self.tweets = []

	def read(self):

		#instanciation de fichier csv
		if(sys.version_info > (3,0)):
			file = open(self.fileNameCsv, "rt",encoding = "utf8")
		else:
			file = open(self.fileNameCsv, "rt")
			
		fname = "res/prenoms.csv"
		file2 = open(fname, "rt")

		try:
			#connection aux fichiers csv.
			reader = csv.DictReader(file, delimiter=',')
			reader2 = csv.DictReader(file2, delimiter=',')

			#on transforme les prenoms en une liste sans capital
			prenoms = []
			for row in reader2:
				prenoms.append(row.get('prenom').lower())

			""" open the file of corpus_company and instanciate them """
			corpus_company = []
			with open("res/corpus_company.txt") as f:
				for line in f:
					if line.strip() != "":
						corpus_company.append(line.strip())

			#pour tous les elements trouves dans le csv
			for row in reader:

				pertinent = False
				#si l'element est pertinent
				if 'VRAI' in row.get('Pertinent'):
					pertinent = True


				#on ne continue pas si l'element est une compagnie ou une organisation
				typeAuteur = "INDETERMINED"
				determiner = False
				for companyWord in corpus_company:
					if companyWord in row.get('user_name').lower():
						typeAuteur = "COMPANY"
						determiner = True

				#Instanciation à vide pour les tweets ne provenant pas de personnes
				prenom = ""
				nom = ""

				#Test d'un auteur de type personne
				if not determiner:
					# on separe tous les elements composant le champ nom
					for val in row.get('user_name').split(' '):

						# on verifie si un prenom existe dans le champ user_name
						if val.lower() in prenoms:
							typeAuteur = "PERSON"
							prenom = val.lower()
							nom = row.get('user_name').replace(val, "")
							nom = nom.strip()

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
											typeAuteur, prenom, nom
											))

		finally:
			file.close()
			file2.close()

	def getSomeoneTweets(self, nom, prenom, pertinent):
		someoneTweets = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (nom.lower() in tweet.user_name.lower())& (prenom.lower() in tweet.user_name.lower()):
				someoneTweets.append(tweet)
		return someoneTweets

	def getIndeterminatedTweets(self, pertinent):
		indeterminer = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuthor == "INDETERMINED"):
				indeterminer.append(tweet)
		return indeterminer

	def getPeopleTweets(self, pertinent):
		people = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuthor == "PERSON"):
				people.append(tweet)
		return people

	def getCompagnieTweets(self, pertinent):
		compagnie = []
		for tweet in self.tweets:
			if (tweet.pertinent==pertinent) & (tweet.typeAuthor == "COMPANY"):
				compagnie.append(tweet)
		return compagnie


# test de la class TweetCSVReader
if __name__ == '__main__':

	fname = "res/iteration_500.csv"
	reader = Reader(fname)
	reader.read()
	#tweets = reader.getIndeterminatedTweets(True)
	tweets = reader.getCompagnieTweets(True)
	tweets.extend(reader.getCompagnieTweets(False))
	tweets = list(set(tweets))
	for t in tweets:
		print(t.user_name)
	print(len(tweets))