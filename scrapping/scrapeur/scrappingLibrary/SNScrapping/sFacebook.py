#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
if __name__ == "__main__":
	from models.accountFacebook import *
else:
	from .models.accountFacebook import *
import requests, bs4
import argparse
import time
import os
import bs4
import platform
import sys

def standardUrl(url):
	tab = url.split("facebook.com")

	""" we ignore the string after the name except if it's a number starting with one"""
	tab2 = tab[1].split("/")
	if len(tab2)>2:
		if (tab2[2]!="") and (tab2[2][0]=="1"):
			return "https://www.facebook.com/"+tab2[1]+"/"+tab[2]

	return "https://www.facebook.com/"+tab2[1]

""" Verifiy if the url go to a facebook page and not a personnal profil """
def certifiatePage(url):

	#modify the url to go on a page available only in the case of a personnality or company page
	tab = url.split("facebook.com")
	url_modifier = tab[0]+"facebook.com/pg"+tab[1]

	#limit access
	time.sleep(1)

	#request et verification
	res = requests.get(url_modifier)
	res.status_code == requests.codes.ok

	""" Status code at 404 when the page is not available """
	if res.status_code == 404:
		return False
	else:
		#limit access
		time.sleep(1)
		return True



""" Retourne l'objet facebook correspondant a la recherche depuis une url donne """
def findFacebook(nom, prenom, url):
	compte = CompteFacebook(nom, prenom, url)

	#request et verification
	res = requests.get(url)
	res.status_code == requests.codes.ok
	if not res.status_code == 200:
		return None

	if sys.version_info >= (3,0):
		soup = bs4.BeautifulSoup(res.text,"html.parser")
	else:
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

""" Retourne l'objet pageEnetrepriseFB d'une page entreprise correspondant a la recherche depuis une url donne """
def findFacebookPageEntreprise(nom, url):

	compteEntrepriseFacebook = accountFacebook.CompteEntrepriseFacebook(nom,url)

	lienPlusInfo = "/about/?ref=page_internal"
	classDomaineScrapping = "_4-u8" #magnifique ?
	domaine = "Empty"
	nomComplet = nom
	#pour la partie nom complet entreprise c'est sur votre gauche

	#request et verification
	res = requests.get(url)
	res.status_code == requests.codes.ok
	if not res.status_code == 200:
		return None

	soup = bs4.BeautifulSoup(res.text, "html.parser")
	"""Partie ou on récupère le nom complet """
	sidebar_left = soup.find("div", id="entity_sidebar")
	if sidebar_left == None :
		print("nothing sidebar_left")
	scrapping_nomComplet = sidebar_left.find("div", id="u_0_0")
	if scrapping_nomComplet != None :
		nomComplet = scrapping_nomComplet.getText()
	else :
		print("nothing scrapping_nomComplet")
	"""---------------------------------"""

	"""Maintenant on passe sur la récupération à droite, du domaine d'activité de l'entreprise"""
	scrapping_domaine=soup.find("div", class_=classDomaineScrapping)
	if scrapping_domaine != None :
		print(scrapping_domaine.getText())
		domaine = scrapping_domaine.getText()
	else :
		print("nothing scrapping_domaine")
	compteEntrepriseFacebook.domaineEntreprise = domaine
	compteEntrepriseFacebook.nomComplet = nomComplet
	return compteEntrepriseFacebook





# test de la classe et des methodes
if __name__ == '__main__':
	"""
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
	"""

	compte = findFacebookPageEntreprise('INRA', 'https://www.facebook.com/Inra.France/')
	compte.affiche()

