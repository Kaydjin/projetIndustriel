#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import re
import sys
import time
from tweetCsvReader import *
#from test_google import *
from libraries import sGoogle
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
		result = search_google(val.userPrenom  + " " + val.userNom, "", "facebook", False)
		nbrResByTweets = []
		nbrResByTweetsExpEtud = []
		nbrResByTweetsExp = []
		nbrResByTweetsEtud = []
		nbrResByTweetsGeo = []
		nbrResNouns = []
		nbrResPropernounsLExp = []
		nbrResPropernounsLEtud = []

		if len(result) > 0:
			compte = findFacebook(val.userNom, val.userPrenom, result[0])

			#Initialisation de variables pour le parcours des homonymes
			urls = compte.homonymes
			doneUrl = []
			comptes = []
			comptes.append(compte)

			#Limite temporel
			start_time = time.time()
			time_limit = 20

			#Tant que la liste urls n'est pas vide et que la limite temporel n'est pas atteinte,
			#on continue a recuperer les homonymes
			while (len(urls) > 0) & (time.time()-start_time < time_limit):
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

			nbrResByTweets.append(len(comptes))
			expAndEtud = 0
			exp = 0
			etud = 0
			geo = 0
			nounsL = []
			propernounsLExp = []
			propernounsLEtud = []
			for c in comptes:

				nomExp = ""
				nomEtud =""

				analyser = TextAnalyser()

				propernounsExp = list(analyser.getPropersNounsFromList(c.nomsExperiences))
				propernounsEtud = list(analyser.getPropersNounsFromList(c.nomsEtudes))

				if (len(c.nomsExperiences)) > 0 and (len(c.nomsEtudes)>0):
					expAndEtud = expAndEtud + 1

				if (len(c.nomsExperiences)) > 0:
					exp = exp + 1

				if (len(c.nomsEtudes)) > 0:
					etud = etud + 1

				if (len(c.geoDonnees)) > 0:
					geo = geo + 1

				propernounsLExp.append(len(propernounsExp))
				propernounsLEtud.append(len(propernounsEtud))

				if not val.userDescription=="":
					r = analyser.getMatchingNouns(val.text + " " + val.tags +" " + val.userDescription + " " + val.userLocation, c.synthese())
					nounsL.append(len(r))
					print("[" + val.userNom + " " + val.userPrenom + ": (" + str(len(r)) + ",matchingnouns) ("
							  + str(len(c.nomsExperiences)) + ",exp) (" + str(len(c.nomsEtudes)) + ",etudes)("
							  + str(len(propernounsExp)) + ",matchingexp)(" + str(len(propernounsEtud)) + ",machingetud)]")				
				else:
					nounsL.append(0)
					print("[" + val.userNom + " " + val.userPrenom + "("
					  + str(len(c.nomsExperiences)) + ",exp) (" + str(len(c.nomsEtudes)) + ",etudes)("
					  + str(len(propernounsExp)) + ",matchingexp)(" + str(len(propernounsEtud)) + ",machingetud)]")	

				if len(propernounsExp)>0:
					print(propernounsExp[0])
				if len(propernounsEtud)>0:
					print(propernounsEtud[0])
				print("-------------------------------------------------------------------------------------")

			nbrResByTweetsExpEtud.append(expAndEtud)
			nbrResByTweetsExp.append(exp)
			nbrResByTweetsEtud.append(etud)
			nbrResByTweetsGeo.append(geo)
			nbrResNouns.append(nounsL)
			nbrResPropernounsLExp.append(propernounsLExp)
			nbrResPropernounsLEtud.append(propernounsLEtud)


					

