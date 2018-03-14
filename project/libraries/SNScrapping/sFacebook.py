#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
if __name__ == "__main__":
	from models import accountFacebook
	from models import accountCompany
	from utils import utils
	from seleniumClass.managerSelenium import SeleniumManager
	from seleniumClass.seleniumClientFacebook import ClientFacebook
	from settings import settingsFacebook
else:
	from .models import accountFacebook
	from .models import accountCompany
	from .utils import utils
	from .seleniumClass.managerSelenium import SeleniumManager
	from .seleniumClass.seleniumClientFacebook import ClientFacebook
	from .settings import settingsFacebook
import requests, bs4
import argparse
import time
import os
import bs4
import platform
import sys
from datetime import datetime



#--------------------------Partie Selenium----------------------------
class SearcherFacebook_Selenium:

	def __init__(self, manager):
		self.manager = manager
		liclient = ClientFacebook(self.manager.driver, settingsFacebook.search_keys)
		self.manager.connection(liclient)


	""" fonction appeler par findFacebook, le manager doit etre initialisé avec une page de recherche de profil Facebook
	, scrappe la page puis scroll pour charger les informations, s'arrete quand on trove le message 'End of Results' """
	def findFacebookScrolling(self):
		#Chargement de la page /!\ 
		time.sleep(2)

		html=self.manager.driver.page_source
		soup=bs4.BeautifulSoup(html, "html.parser")
		#On cherche le texte en bas qui apparait quand nous n'avons plus de résultat pour arretez de scroll
		pattern = 'End of Results'

		end = soup.find('div', text=pattern)

		while end == None :
			self.manager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)
			html=self.manager.driver.page_source
			soup=bs4.BeautifulSoup(html, "html.parser")
			end = soup.find('div', text=pattern)

		html=self.manager.driver.page_source
		soup=bs4.BeautifulSoup(html, "html.parser")
		liste = []
		a=0
		results = soup.find('div',id='browse_result_area')
		if results != None:
			tab_results = results.find_all('a')
			for elem in tab_results:
				liste.append(elem.get('href'))
		else:
			print("pas de résultat")
		#On passe la liste sous un set pour retirer les doublons
		liste = set(liste)
		#la liste reçu peut donner en résultat des # on les retire
		liste.remove("#")
		return liste


	""" Effectue une recherche de profil sur facebook via selenium """
	def findFacebook(self,nom,prenom):
		profile_link ="https://www.facebook.com/search/str/%s+%s/keywords_users" % (nom,prenom)
		self.manager.get(profile_link, 3)
		return self.findFacebookScrolling()

	""" EXPERIMENTAL permet de scrapper un profil personne via selenium
	POUR L'INSTANT NE STOCKE AUCUNE INFORMATION """
	def scrappingProfil(self, nom, prenom, url):
		compte = accountFacebook.CompteFacebook(nom, prenom, url)
		self.manager.get(url,3)
		#on charge le haut de la page
		time.sleep(2)
		html=self.manager.driver.page_source
		soup=bs4.BeautifulSoup(html, "html.parser")

		nameClassFB_Info = "fbTimelineUnit"

		infoGenral = soup.find('li', class_=nameClassFB_Info)

		info = infoGenral.find_all('li')
		for elem in info:
			print(elem.getText())
		return compte


	def scrappingProfilEntreprise(self,nom, url):
		accountCompanyFacebook = accountCompany.AccountCompany(nom,url)
		self.manager.get(url,3)
		#chargement
		time.sleep(2)
		html=self.manager.driver.page_source
		soup=bs4.BeautifulSoup(html, "html.parser")

		lienPlusInfo = "/about/?ref=page_internal"
		classDomaineScrapping = "_1c03" #magnifique ?
		domaine = "Empty"
		nomComplet = nom
		#pour la partie nom complet entreprise c'est sur votre gauche

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
			domaine = scrapping_domaine.getText()
		else :
			print("nothing scrapping_domaine")
		accountCompanyFacebook.domaine = domaine
		accountCompanyFacebook.nomComplet = nomComplet
		return accountCompanyFacebook


def standardUrl(url):

	#if not a facebook url go to simple facebook url
	if (url==None) or (not "facebook.com" in url):
		return "https://www.facebook.com/"

	#certifiate others arguments
	tab = url.split("facebook.com")

	""" we ignore the "/ argument" after the name except if it's a number starting with one"""
	tab2 = tab[1].split("/")
	if len(tab2)>2:
		if (tab2[2]!="") and (tab2[2][0]=="1"):
			return "https://www.facebook.com/"+tab2[1]+"/"+tab2[2]

	return "https://www.facebook.com/"+tab2[1]

""" Verifiy if the url go to a facebook page and not a personnal profil """
def certifiatePage(url):
	if(url==None):
		return None

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

#--------------------------Partie Facebook sans l'utilisation de sélénium ----------------------------

""" Retourne l'objet facebook correspondant a la recherche depuis une url donne """
def findFacebook(nom, prenom, url):
	compte = accountFacebook.CompteFacebook(nom, prenom, url)

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


def testRecherche(search):

	liste = search.findFacebook('candido','frank')
	file = ""
	name_date_file = datetime.now().strftime('%H%M%d%m%Y')
	if sys.version_info >= (3, 0):
		file=open('libraries/SNScrapping/log/sfacebookRecherche'+name_date_file+'.log', 'w+', encoding="utf8")
	else:
		file=open('libraries/SNScrapping/log/sfacebookRecherche'+name_date_file+'.log', 'w+')
	for val in liste:
		print(val)
		ecriturePython2_Python3(file, val)
		file.write('\n')
	file.close()

def testScrappingPage(search):
	search.scrappingProfil('candido', 'frank', 'https://www.facebook.com/frank.candido.5')

def testScrappingPageEntreprise(search):
	nom = 'Sopra'
	url = 'https://www.facebook.com/soprasteria/'
	#url = 'https://www.facebook.com/Inra.France/'
	#nom='INRA'
	return search.scrappingProfilEntreprise(nom, url)

#-----------------------Test pour la partie if __name__ == '__main__': -----------------------------
def testSeleniumFB():
	manager = SeleniumManager(3)
	search = SearcherFacebook_Selenium(manager)
	name_date_file = datetime.now().strftime('%H%M%d%m%Y')
	file=open('libraries/SNScrapping/log/sfacebookSelenium_py_recherche'+name_date_file+'.log', 'w+', encoding="utf8")
	res = testScrappingPageEntreprise(search)
	file.write(res.nom+'\n')
	file.write(res.url+'\n')
	file.write(res.position+'\n')
	file.write(res.domaineEntreprise+'\n')
	file.write(res.nomComplet+'\n')
	file.close()
	manager.driver_quit()

def testFB():
	compte = findFacebook('frank','candido','https://www.facebook.com/frank.candido.5')
	print('Homonymes:')
	for val in compte.homonymes:
		print(val)

	print('Experiences:')

	list_len = len(compte.nomsExperiences)
	for i in range(0, list_len):
		print(compte.nomsExperiences[i])
		print(compte.detailsExperiences[i])
	print('Etudes:')
	for val in compte.nomsEtudes:
		print(val)
	print('Favoris:')
	for val in compte.favoris:
		print(val)




# test de la classe et des methodes
if __name__ == '__main__':
	testSeleniumFB()
	

	"""compte = findFacebookPageEntreprise('INRA', 'https://www.facebook.com/Inra.France/')
	compte.affiche()"""

