#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import re
import sys
import time
from tweetCsvReader import *
from testgoogle import *
from textanalyser import *
from sfacebook import *

#from linkedIn_Recherche import *

if __name__ == '__main__':

	#Recuperation des tweets lier a la personne choisit
	fname = "iteration_500.csv"
	reader = Reader(fname)
	reader.read()
	tweets = reader.getPeopleTweets(True)

	for val in tweets:
		print(val.userNom +"/"+val.userPrenom + "/"+val.userLocation+"/"+val.userDescription)

		#recherche du premier resultat facebook obtenu
		result = []
		if not val.userDescription=="":
			result = search_google(val.userPrenom  + " " + val.userNom, val.userLocation)
			print(result[0])
			compte = findFacebook(val.userNom, val.userPrenom, result[0])

			#Initialisation de variables pour le parcours des homonymes
			"""urls = compte.homonymes
			doneUrl = []
			comptes = []

			#Limite temporel
			start_time = time.time()
			time_limit = 20

			#Tant que la liste urls n'est pas vide et que la limite temporel n'est pas atteinte,
			#on continue a recuperer les homonymes
			while (len(urls) > 0) & (time.time()-start_time<time_limit):

				#on parcourt les homonymes dans la liste urls
				for url in urls:
					print(url)
					#on se limite a une requete toutes les deux secondes
					time.sleep(2)

					#on ajoute les comptes trouves
					c = findFacebook(nom, prenom, url)
					comptes.append(c)

					#on met en memoire les adresse deja faite
					doneUrl.append(url)

				#on vide urls
				urls = []

				#on parcourt les comptes obtenus (les anciens aussi mais on l'ignore)
				for c in comptes:

					#on verifie si il y a de nouveaux homonymes a tester
					for u in c.homonymes:
						if (u not in doneUrl) & (u not in urls):
							urls.append(u)"""

			#Analyse avec le premier compte facebook obtenu
			analyser = TextAnalyser()
			r = analyser.getMatchingNouns(tweets[0].userDescription, compte.synthese())
			strRes = ""
			for values in r:
				strRes = strRes+values
			print(strRes)

			#Analyse avec les autres comptes
			"""for c in comptes:
				r = analyser.getMatchingNouns(tweets[0].userDescription, c.synthese())
				strRes = ""
				for values in r:
					strRes = strRes+values
				print(strRes)"""