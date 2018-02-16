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

def recherche():


    search_keys = { 
        "username"         :  "testgeodatas@laposte.net",
        "password"         :  "testgeodatas",
        "keywords"         :  ["Data Scientist", "Data Analyst"],
        "locations"        :  ["San Francisco Bay Area", "Greater New York City Area"],

        "search_radius"    :  "50",
        "page_number"      :  1,
        "date_range"       :  "All",
        "sort_by"          :  "Date Posted",
        "salary_range"     :  "All",
        "filename"         :  "output.txt",
        "results_page"     :  ""
    }

    # initialize selenium webdriver - pass latest chromedriver path to webdriver.Chrome()

    #On gere ici si l'os qui lance l'appli est windows ou Linux
    #TODO Mac si besoin, il faudra par contre telecharger le driver de mac
    os_driver = "error"
    if platform.system() == "Windows":
        os_driver = "/geckodriver_windows64.exe"
    elif platform.system() == "Linux":
        os_driver = "/geckodriver_linux"
    else :
        print("OS non supporté")
        os_driver = "error"

    if os_driver != "error" :
        driver = webdriver.Firefox(executable_path=os.getcwd()+os_driver)
        driver.get("https://www.linkedin.com/uas/login")

        # initialize LinkedIn web client
        liclient = LIClient(driver, **search_keys)

        liclient.login()

        # wait for page load
        time.sleep(3)

        #Pour l'instant en dur, on pourra imaginer les différents arg de la recherche en parametre de la fonction
        nom = "candido"
        prenom = "frank"
        #
        
        recherche_nom= "lastName="
        recherche_prenom = "firstName="
        profile_link="https://www.linkedin.com/search/results/people/?"+recherche_nom+nom+"&"+recherche_prenom+prenom

        driver.get(profile_link)

        # wait for page load
        time.sleep(3)

        file=open('scrapping_Recherche.log','w+')

        html=driver.page_source
        soup=bs4.BeautifulSoup(html, "html.parser")

        same=soup.find_all('a', class_='search-result__result-link')
        try:
            # le nbr de résultat est doublé car, pour une personne nous avons deux lien pour rejoindre son profil (sur son image de profil + nom)
            a=0
            for elem in same:
                a=a+1
                if a%2==0:
                    #le lien est coupé, on rajoute donc ceci au début de chaque ligne
                    file.write('https://www.linkedin.com')
                    file.write(elem.get('href'))
                    file.write('\n')
        except Exception as e:
            print(e)
        file.close()
        liclient.driver_quit()

if __name__ == '__main__':
    recherche()