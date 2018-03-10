#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import models
if __name__ == "__main__":
    from models.accountFacebook import *
    from models.accountCompany import *
    from utils.utils import *
    from seleniumClass.managerSelenium import SeleniumManager
    from seleniumClass.seleniumClientFacebook import ClientFacebook
    from settings.settingsFacebook import *
else:
    from .models.accountFacebook import *
    from .models.accountCompany import *
    from .utils.utils import *
    from .seleniumClass.managerSelenium import SeleniumManager
    from .seleniumClass.seleniumClientFacebook import ClientFacebook
    from .settings.settingsFacebook import *
from datetime import datetime
import sys
import argparse
import time
import os
import bs4
import platform

class SearcherFacebook_Selenium:

    def __init__(self, manager):
        self.manager = manager
        liclient = ClientFacebook(self.manager.driver, search_keys)
        self.manager.connection(liclient)

    def findFacebookScrolling(self):
    	#Chargement de la page /!\ 
        time.sleep(2)

        html=self.manager.driver.page_source
        soup=bs4.BeautifulSoup(html, "html.parser")

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
        	print("pas de résultat :(")
        liste = set(liste)
        liste.remove("#")
        return liste


    def findFacebook(self,nom,prenom):
    	profile_link ="https://www.facebook.com/search/str/%s+%s/keywords_users" % (nom,prenom)
    	self.manager.get(profile_link, 3)
    	return self.findFacebookScrolling()

    def scrappingProfil(self, nom, prenom, url):
        compte = CompteFacebook(nom, prenom, url)
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
        accountCompanyFacebook = AccountCompany(nom,url)
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



def ecriturePython2_Python3(file, myStr):
    if sys.version_info >= (3,0):
        file.write(myStr)
    else:
        file.write(myStr.encode('utf8'))

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


if __name__ == '__main__':
    manager = SeleniumManager(3)
    search = SearcherFacebook_Selenium(manager)
    name_date_file = datetime.now().strftime('%H%M%d%m%Y')
    file=open('libraries/SNScrapping/log/sfacebookSelenium_py_recherche'+name_date_file+'.log', 'w+', encoding="utf8")
    res = testScrappingPageEntreprise(search)
    file.write(res.nom+'\n')
    file.write(res.url+'\n')
    file.write(res.geolocalisation+'\n')
    file.write(res.domaineEntreprise+'\n')
    file.write(res.nomComplet+'\n')
    file.close()
    manager.driver_quit()
