#!/usr/bin/env python
# -*- coding: utf-8 -*-

from textanalyser import *
import requests, bs4
import argparse
import time
import os
import bs4
import platform

class CompteFacebook:

	def __init__(self, nom, prenom, url):
		self.homonymes = []
		self.description = ""
		self.url = url
		self.favoris = []
		self.nomsExperiences = []
		self.detailsExperiences = []
		self.nomsEtudes = []
		self.detailsEtudes = []
		self.geodonnees = []
		self.complementaire = ""

	def addFavori(self, x):
		self.favoris.append(x)

	def addGeoDonnee(self, x):
		self.geodonnees.append(x)

	def addExperience(self, exp, detail):
		self.nomsExperiences.append(exp)
		self.detailsExperiences.append(detail)

	def addEtude(self, etud, detail):
		self.nomsEtudes.append(etud)
		self.detailsEtudes.append(detail)

	def addHomonyme(self, x):
		self.homonymes.append(x)

	def synthese(self):
		strFavoris = ""
		for s in self.favoris:
			strFavoris = strFavoris + s+ " "

		strExperiences = ""
		num=0
		for s in self.nomsExperiences:
			strExperiences = strExperiences + s+ " " + self.detailsExperiences[num] + " "
			num = num + 1

		strEtudes = ""
		num=0
		for s in self.nomsEtudes:
			strEtudes = strEtudes+ s + " " + self.detailsEtudes[num] + " "
			num = num + 1


		strGeoDonnee = ""
		for s in self.geodonnees:
			strGeoDonnee = strGeoDonnee + s+ " "

		return self.description + " " + strEtudes + " " + strExperiences + " " + self.complementaire + " " + strGeoDonnee + " " + strFavoris

""" Retourne l'objet facebook correspondant a la recherche depuis une url donne """
def findFacebook(nom, prenom, url):
	compte = CompteFacebook(nom, prenom, url)

	#request et verification
	res = requests.get(url)
	res.status_code == requests.codes.ok
	if not res.status_code == 200:
		return None

	soup = bs4.BeautifulSoup(res.text)
	sames = soup.select('#pagelet_people_same_name a')

	#'PERSONNES MEME PRENOMS/NOMS:')
	a=0
	if len(sames)>0:
		#on ne prend pas les liens de types public de facebook et on ne prend qu'un lien sur deux (doublons sinon)
		for elem in sames:
			if "/public/" in elem.get('href'):
				break
			if a%2==1:
				if (nom.lower() in elem.getText().lower()) & (prenom.lower() in elem.getText().lower()):
					compte.addHomonyme(elem.get('href'))
			a=a+1

	#'PROFIL TEXT:')
	descriptioncitation = soup.select('#pagelet_timeline_medley_about ._c24')
	if len(descriptioncitation)>0:
		desc = ""
		for elem in descriptioncitation:
			desc = desc + elem.getText()
		compte.description = desc
	else:
		compte.description = "null"

	#'DONNEES METIERS ET ECOLES:')
	metiersecoles = soup.find_all('div', class_='_4qm1')
	if len(metiersecoles)>0:
		for elem in metiersecoles:
			if (elem.get('data-pnref') == "work") or (elem.get('data-pnref') == "edu"):
				liste = elem.find_all('li')
				for val in liste:
					liste2 = val.find_all('a')
					for val2 in liste2:
						if val2.getText()!="":
							inter = val.getText()
							if elem.get('data-pnref') == "work":
								compte.addExperience(val2.getText(), inter.replace(val2.getText(), ""))
							if elem.get('data-pnref') == "edu":
								compte.addEtude(val2.getText(), inter.replace(val2.getText(), ""))

	#'DONNEES GEOGRAPHIQUES:')
	hometown = soup.select('#pagelet_timeline_medley_about #pagelet_hometown .fbProfileEditExperiences a')
	if len(hometown)>0:
		for elem in hometown:
			compte.addGeoDonnee((elem.getText()))

	#'Favoris:')
	favorites = soup.select('#favorites a')
	if len(favorites)>0:
		for elem in favorites:
			compte.addFavori(elem.getText())

	return compte

# test de la classe et des methodes
if __name__ == '__main__':
	compte = findFacebook('frank','candido','https://www.facebook.com/frank.candido.5')
	print('Homonymes:')
	for val in compte.homonymes:
		print(val)

	print('Experiences:')
	for val in compte.nomsExperiences:
		print(val)
	print('Etudes:')
	for val in compte.nomsEtudes:
		print(val)
	print('Favoris:')
	for val in compte.favoris:
		print(val)
	print compte.synthese()

	analyser = TextAnalyser()
	liste = analyser.getPropersNounsFromList(compte.nomsExperiences)
	for v in liste:
		print(v)
	liste = analyser.getPropersNounsFromList(compte.nomsEtudes)
	for v in liste:
		print(v)

