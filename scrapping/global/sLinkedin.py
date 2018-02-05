#!/usr/bin/env python
#-*- coding: utf-8 -*-
from selenium import webdriver
from client import LIClient
from settings import search_keys
import argparse
import time
import os
import bs4
import platform

class Experience:

    def __init__(self, url, nom, date, geolocalisation, description, descriptionEntreprise):
        self.url = url
        self.nom = nom
        self.date = date
        self.geolocalisation = geolocalisation
        self.description = description
        self.descriptionEntreprise = descriptionEntreprise
        self.domaine = ""   

        def toString(self):
            return nom + " " + geolocalisation + " " + description

class CompteLinkedin:

    def __init__(self, nom, prenom, url):
        self.homonymes = []
        self.url = url
        self.favoris = []
        self.etudes = []
        self.experiences = []
        self.entreprise = ""
        self.complementaire = ""

    def addFavori(self, x):
        self.favoris.append(x)

    def addEtude(self, x):
        self.etudes.append(x)

    def addExperience(self, url, nom, date, geolocalisation, description, descriptionEntreprise):
        self.experiences.append(Experience(url, nom, date, geolocalisation, description, descriptionEntreprise))

    def addHomonyme(self, x):
        self.homonymes.append(x)

    def synthese(self):
        strFavoris = ""
        for s in self.favoris:
            strFavoris = strFavoris + s+" "
        strEtudes = ""
        for s in self.etudes:
            strEtudes = strEtudes + s+" "
        strExperiences = ""
        for s in self.experiences:
            strExperiences = strExperiences + s+" "

        return strEtudes + " " + strExperiences + " " + self.complementaire + " " + strFavoris

class SeleniumManager:

    def __init__(self, waiting_time):
        os_driver = "error"

        """ different drivers selon l'os"""
        if platform.system() == "Windows":
            os_driver = "/geckodriver_windows64.exe"
        elif platform.system() == "Linux":
            os_driver = "/geckodriver_linux"
        else :
            print("OS non supporté")
            os_driver = "error"

        if os_driver != "error" :
            self.driver = webdriver.Firefox(executable_path=os.getcwd()+os_driver)
        self.waiting_time = waiting_time
        self.last_time = time.time()

    """ Permet de gérer le temps entre les requêtes """
    def get(self, url, pause_time):

        """ Si le temps entre les deux dernieres requetes gérer par le manager 
            est inferieur au paramètre d'initialisation, on attend le temps restant"""
        if time.time()-self.last_time<self.waiting_time:
            time.sleep(self.waiting_time-(time.time()-self.last_time))

        """ on recupere l'url demande """
        self.driver.get(url)

        """ on attend le temps requisionne """
        time.sleep(pause_time)

        """ on garde en memoire le temps de la derniere utilisation """
        self.last_time = time.time()

    def driver_quit(self):
        self.driver.quit()


def formater(str_text):
    strt = str_text.replace('\n', ' ').strip()
    str_tab = str_text.split("  ")

    res = ""
    for s in str_tab:
        s = s.strip()
        if(s != ''):
            res = res + s

    return res.encode('utf-8')

class SearcherLinkedin:

    def __init__(self, manager):
        self.manager = manager

        """ pause time 0 car on doit initialiser liclient avant d'attendre """
        self.manager.get("https://www.linkedin.com/uas/login", 0)

        # initialize LinkedIn web client
        liclient = LIClient(manager.driver, **search_keys)
        liclient.login()
        time.sleep(3)

    def findLinkedins(self, nom, prenom):
        recherche_nom= "lastName="
        recherche_prenom = "firstName="
        profile_link="https://www.linkedin.com/search/results/people/?"+recherche_nom+nom+"&"+recherche_prenom+prenom

        manager.get(profile_link, 3)

        html=manager.driver.page_source
        soup=bs4.BeautifulSoup(html, "html.parser")

        same=soup.find_all('a', class_='search-result__result-link')

        liste = []
        a=0
        for elem in same:
            a=a+1

            """ Le nombre de résultat est double car, pour une personne nous avons deux lien
                pour rejoindre son profil (sur son image de profil + nom)"""
            if a%2==0:
                liste.append('https://www.linkedin.com'+elem.get('href'))

        return liste

    def findLinkedin(self, nom, prenom, url):

        compte = CompteLinkedin(nom, prenom, url)

        """ pause 0 car on doit defiler vers le bas avant de faire la pause"""
        manager.get(url, 3)
        print("ici")
        #on scrolle vers le bas pour faire un chargement des centres d'interet
        manager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # wait for page load
        time.sleep(6)

        html=manager.driver.page_source

        soup=bs4.BeautifulSoup(html, "html.parser") #specify parser or it will auto-select for you

        #Education
        valeurs = soup.find_all('li', class_='pv-education-entity')
        for elem in valeurs:
            if(elem.get_text()!= ''):
                compte.addEtude(elem.get_text().strip("\n \r"))
                print(formater(elem.get_text()))

        #Favoris
        valeurs = soup.find_all('li', class_='pv-interest-entity')
        for elem in valeurs:
            if(elem.get_text()!= ''):
                compte.addFavori(elem.get_text().strip("\n \r"))
                print(formater(elem.get_text()))

        # Experiences
        soup=bs4.BeautifulSoup(html, "html.parser") #specify parser or it will auto-select for you
        valeurs = soup.find_all('li', class_='pv-position-entity')
        date = []
        description = []
        for elem in valeurs:
            date.append(elem.get_text().strip("\n \r"))
            description.append(elem.get_text().strip("\n \r"))
            print(formater(elem.get_text()))

        experience = soup.select('.pv-profile-section.experience-section.ember-view a')
        urlsExperiences = []

        pos = 0
        index = []
        for elem in experience:
            if (elem.get_text() != '') & ("company" in elem.get('href')):
                urlsExperiences.append("https://www.linkedin.com"+elem.get('href'))
            if "company" in elem.get('href'):
                index.append(pos)
            else:
                val = elem.get('href').replace("/search/results/index/?keywords=", "")
                val = val.encode('utf-8')
                print(val)

            pos = pos + 1

        nomsE = []
        domaineE = []
        locationE = []
        descriptionE = []
        for url in urlsExperiences:
            # wait for page load=3
            manager.get(url, 3)
            html=manager.driver.page_source
            soup=bs4.BeautifulSoup(html, "html.parser") #specify parser or it will auto-select for you
            divnom = soup.select('.org-top-card-module__name')
            divdomaine = soup.select('.company-industries.org-top-card-module__dot-separated-list')
            divlocation = soup.select('.org-top-card-module__location')
            divdescription = soup.select('.org-about-us-organization-description p')
            for elem in divnom:
                nomsE.append(elem.get_text().strip("\n \r"))
            for elem in divdomaine:
                domaineE.append(elem.get_text().strip("\n \r"))
            for elem in divlocation:
                locationE.append(elem.get_text().strip("\n \r"))
            for elem in divdescription:
                descriptionE.append(elem.get_text().strip("\n \r"))

        print(len(urlsExperiences))
        print(len(nomsE))
        print(len(date))
        print(len(locationE))
        print(len(description))
        print(len(descriptionE))
        for k in range(0,len(urlsExperiences)):
            compte.addExperience(urlsExperiences[k], nomsE[k], "", locationE[k], "", descriptionE[k])

        return compte

if __name__ == '__main__':
    manager = SeleniumManager(3)
    search = SearcherLinkedin(manager)
    liste = search.findLinkedins("candido", "frank")
    for val in liste:
        print(val)

    compte = search.findLinkedin("candido", "frank", liste[0])
    for experience in compte.experiences:
        #print(experience.url)
        print(experience.nom)
        #print(experience.geolocalisation)
        #print(experience.descriptionEntreprise)

    manager.driver_quit()