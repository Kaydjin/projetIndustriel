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
		if not val.userDescription=="":
			result = search_google(val.userPrenom  + " " + val.userNom, "", "facebook")
			
			if len(result) > 0:
				compte = findFacebook(val.userNom, val.userPrenom, result[0])

				#Analyse avec le premier compte facebook obtenu
				analyser = TextAnalyser()
				print("##################################################################################################")
				print("iiiiii>" + val.text)
				print("ooooooo" + val.userPrenom + " " + val.userNom + "" + result[0])
				print("*******" + val.userDescription + " " + val.userLocation)
				print("------>" + compte.synthese())
				r = analyser.getMatchingNouns(val.text + " " + val.tags +  " " + val.userDescription + " " + val.userLocation, compte.synthese())
				strRes = ""
				for values in r:
					strRes = strRes+values
				print("~~~~~~~~~~~~~~~~[" + strRes + "]")
				print("##################################################################################################")

				#Initialisation de variables pour le parcours des homonymes
				urls = compte.homonymes
				doneUrl = []
				comptes = []

				#Limite temporel
				start_time = time.time()
				time_limit = 20

				#Tant que la liste urls n'est pas vide et que la limite temporel n'est pas atteinte,
				#on continue a recuperer les homonymes
				while (len(urls) > 0) & ( ):
					#on parcourt les homonymes dans la liste urls
					for url in urls:
						print(url)
						#on se limite a une requete toutes les deux secondes
						time.sleep(2)

						#on ajoute les comptes trouves
						c = findFacebook(val.userNom , val.userPrenom , url)
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
								urls.append(u)

				for c in comptes:
					r = analyser.getMatchingNouns(val.text + " " + val.tags +" " + val.userDescription + " " + val.userLocation, c.synthese())
					strRes = ""
					for values in r:
						strRes = strRes+values
					print("~~~~~~~~~~~~~~~~[" + strRes + "]")
				print("-------------------------------------------------------------------------------------")

