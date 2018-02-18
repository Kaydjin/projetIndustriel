#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .models import accountFacebook
import requests, bs4
import argparse
import time
import os
import bs4
import platform

def standardUrl(url):
	tab = url.split("facebook.com")
	if not "www" in tab[0]:
		return "https://www.facebook.com"+tab[1]
	return url

""" Verifiy if the page is a personnality page and not a personnal page """
def certifiatePagePersonnality(url):

	#modify the url to go on a page available only in the case of a personnality
	tab = url.split("facebook.com")
	url_modifier = tab[0]+"facebook.com/pg"+tab[1]
	print(url_modifier)

	#request et verification
	res = requests.get(url_modifier)
	res.status_code == requests.codes.ok

	""" Status code at 404 when the page is """
	if res.status_code == 404:
		return False
	else:
		return True



""" Retourne l'objet facebook correspondant a la recherche depuis une url donne """
def findFacebook(nom, prenom, url):
	compte = accountFacebook.CompteFacebook(nom, prenom, url)

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

	print(compte.synthese())

