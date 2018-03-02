#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import re
import sys
import time
from normalizeDatas import *
#from test_google import *
from scrappingLibrary import sGoogle
from textanalyser import *
from scrappingLibrary import sFacebook

#from linkedIn_Recherche import *

if __name__ == '__main__':

	#Recuperation des tweets lier a la personne choisit
	fname = "res/iteration_500.csv"
	reader = Datas()
	reader.readFromCsv(fname)
	tweets = reader.getPeopleTweets(True)

	nbrResByTweets = []
	nbrResByTweetsExpEtud = []
	nbrResByTweetsExp = []
	nbrResByTweetsEtud = []
	nbrResByTweetsGeo = []
	nbrResNouns = []
	nbrResPropernounsLExp = []
	nbrResPropernounsLEtud = []
	nbresultats = len(tweets)

	print(nbresultats)
	for val in tweets:
		result = sGoogle.search_google(val.userFirstname  + " " + val.userSurname, "", "facebook", False)

		if len(result) > 0:
			compte = sFacebook.findFacebook(val.userSurname, val.userFirstname, result[0])

			#Initialisation de variables pour le parcours des homonymes
			urls = compte.homonymes
			doneUrl = []
			comptes = []
			comptes.append(compte)

			#Limite temporel
			start_time = time.time()
			time_limit = 30

			#Tant que la liste urls n'est pas vide et que la limite temporel n'est pas atteinte,
			#on continue a recuperer les homonymes
			while (len(urls) > 0) & (time.time()-start_time < time_limit):
				#on parcourt les homonymes dans la liste urls
				for url in urls:
					print(url)
					#on se limite a une requete toutes les deux secondes
					time.sleep(2)

					#on ajoute les comptes trouves
					c = sFacebook.findFacebook(val.userSurname , val.userFirstname , url)
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

				if (len(c.geodonnees)) > 0:
					geo = geo + 1

				propernounsLExp.append(len(propernounsExp))
				propernounsLEtud.append(len(propernounsEtud))

				if not val.user_description=="":
					r = analyser.getMatchingNouns(val.tweet_text + " " + val.hashtags +" " + val.user_description + " " + val.user_location, c.synthese())
					nounsL.append(len(r))
					print("[" + val.userSurname + " " + val.userFirstname + ": (" + str(len(r)) + ",matchingnouns) ("
							  + str(len(c.nomsExperiences)) + ",exp) (" + str(len(c.nomsEtudes)) + ",etudes)("
							  + str(len(propernounsExp)) + ",matchingexp)(" + str(len(propernounsEtud)) + ",machingetud)]")				
				else:
					nounsL.append(0)
					print("[" + val.userSurname + " " + val.userFirstname + "("
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
		else:
			print("no_result_google")
			nbresultats = nbresultats - 1 

	print nbresultats

	for k in range(0,nbresultats-1):
		print (str(nbrResByTweets[k]) + ",nbPeople "+str(nbrResByTweetsExpEtud[k]) + ",Exp&Etud "
			+str(nbrResByTweetsExp[k]) + ",Exp "+str(nbrResByTweetsEtud[k]) + " ,Etud "
			+str(nbrResByTweetsGeo[k]) + ", geodatas")

	for k in range(0, nbresultats-1):
		for v in range(1, len(nbrResNouns[k])):
			print(str(nbrResNouns[k][v])+ ",nouns " + str(nbrResPropernounsLExp[k][v]) 
				+ ",ExpNouns " + str(nbrResPropernounsLEtud[k][v]) + ",EtudNouns")
		print("- - - - -")
	print("o o o o o")


					

