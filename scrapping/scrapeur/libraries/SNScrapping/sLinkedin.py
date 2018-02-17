#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import absolute_import
from models.accountLinkedin import *
from utils.utils import *
from seleniumClass.mSelenium import SeleniumManager
from seleniumClass.seleniumClientLinkedin import ClientLinkedin
from settings.settingsLinkedin import *
from datetime import datetime
import sys
import argparse
import time
import os
import bs4
import platform

class SearcherLinkedin:

    def __init__(self, manager):
        self.manager = manager

        """ pause time 0 car on doit initialiser liclient avant d'attendre """
        self.manager.get("https://www.linkedin.com/uas/login", 0)

        # initialize LinkedIn web client
        liclient = ClientLinkedin(manager.driver, **search_keys)
        liclient.login()
        time.sleep(3)

    def findLinkedinsScrapping(self):

        #Chargement de la page /!\ 
        time.sleep(2)
        
        #On scroll histoire que la page soit charger pour le scrapping (sinon rique de manquer des éléments)
        manager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(1)
        manager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        html=manager.driver.page_source
        soup=bs4.BeautifulSoup(html, "html.parser")

        same=soup.find_all('a', class_='search-result__result-link')

        liste = []
        a=0
        for elem in same:
            liste.append('https://www.linkedin.com'+elem.get('href'))

        next_page = soup.find_all('ol', class_='results-paginator')
        for elem in next_page:
            suivant=elem.find_all('button', class_='next')
            if (len(suivant)==1):
                #dans le cas ou il croit avoir trouvé un button ... ouais ça arrive si la connexion est trop lente
                try:
                    manager.driver.find_element_by_css_selector('button.next').click()
                    liste = liste + self.findLinkedinsScrapping()
                except:
                    break
        return set(liste)


    def findLinkedinsKeyWord(self, keywords):
        """ fait une recherche avec les mots clefs, replace les espaces par un %20 pour qu'ils fonctionnent dans l'url
        """
        key="keywords="
        keywords=keywords.strip()
        profile_link="https://www.linkedin.com/search/results/people/?%s%s" % (key, keywords.replace(' ','%20'))

        manager.get(profile_link, 3)
        return self.findLinkedinsScrapping()

    def findLinkedins(self, nom, prenom, ecole=None, entreprise=None):
        """
            Usage :
            ecole="str", entreprise="str" qui sont des paramètres optionnel
        """
        recherche_nom= "lastName="
        recherche_prenom = "firstName="
        profile_link="https://www.linkedin.com/search/results/people/?"+recherche_nom+nom+"&"+recherche_prenom+prenom

        if ecole is not None:
            recherche_ecole="school=%s" % ecole
            profile_link+= "&"+recherche_ecole
        if entreprise is not None:
            recherche_entreprise="company=%s" % entreprise
            profile_link+= "&"+recherche_entreprise


        manager.get(profile_link, 3)

        return self.findLinkedinsScrapping()

    def findLinkedin(self, nom, prenom, url, file_tmp):

        compte = CompteLinkedin(nom, prenom, url)

        """ pause 0 car on doit defiler vers le bas avant de faire la pause"""
        manager.get(url, 3)
        
        #on charge le haut de la page
        time.sleep(3)
        #on scrolle vers le bas pour faire un chargement des centres d'interet
        manager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # on charge le bas de la page
        time.sleep(3)

        html=manager.driver.page_source

        soup=bs4.BeautifulSoup(html, "html.parser") #specify parser or it will auto-select for you

        #Education
        valeurs = soup.find_all('section', class_='education-section')
        file_tmp.write("-------------------------Education/Etude-------------------------\n")
        if(len(valeurs)==0):
            file_tmp.write('Empty\n')
        else:
            res=""
            for elem in valeurs:
                elem_valeurs = elem.find_all('li')
                for e in elem_valeurs:
                    if(e.get_text() != '') :
                        tmp = formater(e.get_text())
                        compte.addEtude(tmp)
                        res = res + '\n\n' + tmp
            ecriturePython2_Python3(file_tmp, res)
            file_tmp.write('\n\n')

        #Favoris
        file_tmp.write("\n-------------------------Favoris-------------------------\n")
        valeurs = soup.find_all('li', class_='pv-interest-entity')
        for elem in valeurs:
            if(elem.get_text()!= ''):
                tmp = formater(elem.get_text())
                compte.addFavori(tmp)
                ecriturePython2_Python3(file_tmp, tmp)
                file_tmp.write('\n\n')

        # Recuperation en dur des experiences
        experiences = []
        valeurs = soup.find_all('section', class_='experience-section')

        file_tmp.write("\n-------------------------Experiences-------------------------\n")
        if(len(valeurs)==0):
            file_tmp.write('Empty\n')
        else:
            """depuis un tableau de type soup, On récupère la liste de tag li qu'on formatte pour l'affichage 
            Cette fonction est utilisé pour la partie education et expérience"""
            res=""
            for elem in valeurs:
                elem_valeurs = elem.find_all('li')
                for e in elem_valeurs:
                    if(e.get_text() != '') :
                        tmp = formater(e.get_text())
                        experiences.append(tmp)
                        res = res + '\n\n' + tmp
            ecriturePython2_Python3(file_tmp, res)
            file_tmp.write('\n\n')

        #Recuperation des logos d'entreprises et des urls d'entreprises correspondantes
        urlsExperiences = []
        soupImageEntreprise = soup.select('.pv-profile-section.experience-section.ember-view a')
        for elem in soupImageEntreprise:
            if elem.get_text() != '':

                #By default address url empty
                if "company" in elem.get('href'):
                    urlsExperiences.append("https://www.linkedin.com"+elem.get('href'))
                else:
                    urlsExperiences.append("")

        #Parcourt des experiences en dur et des urls d'entreprises lier
        numExp = 0
        for experience in experiences:

            #Default variable
            nom = ""
            nomE = ""
            date = ""
            location = ""
            description = ""
            actif = True
            domaine = ""
            descriptionE = ""

            str_tab=experience.split("\n")
            ligne = 0
            for strExp in str_tab :

                #lower all
                if sys.version_info >= (3, 0):
                    strExpEncode = strExp
                else:
                    strExpEncode = strExp.encode('utf8')
                strExpLow = strExpEncode.lower()
                strExpLow_tab=strExpLow.split(" ")

                #Instanciation of the experience job: (first ligne not empty)
                if ligne == 0:
                    nom = strExpEncode

                #Instanciation of the date
                if "dates" == strExpLow_tab[0]:
                    date = strExpEncode[16:]
                    actif = False
                    for var in ["aujourd", "present", "now"]:
                        if var in strExpLow:
                            actif = True
    
                #Instanciation of the name of the entreprise
                if "nom" == strExpLow_tab[0]:
                    nomE = strExpEncode[22:]

                #Instanciation of the geolocalisation
                if "lieu" == strExpLow_tab[0]:
                    location = strExpEncode.replace("Lieu ", "")

                #Instanciation of the description
                if (ligne>0) & (not strExpLow_tab[0] in ['duree', 'dates', 'nom', 'lieu']):
                    description = strExpEncode
                
                # ++ si la ligne n'est pas vide
                if not strExp=="":
                    ligne = ligne + 1

            #Si un logo entreprise existe.
            if not urlsExperiences[numExp] == "":
                # wait for page load=3
                manager.get(urlsExperiences[numExp], 3)
                html=manager.driver.page_source
                soup=bs4.BeautifulSoup(html, "html.parser") #specify parser or it will auto-select for you
                divnom = soup.select('.org-top-card-module__name')
                divdomaine = soup.select('.company-industries.org-top-card-module__dot-separated-list')
                divlocation = soup.select('.org-top-card-module__location')
                divdescription = soup.select('.org-about-us-organization-description p')

                #On preferera le nom et la localisation donner sur la page de l'entreprise si elle existe.
                for elem in divnom:
                    nomsE = elem.get_text().strip("\n \r")
                for elem in divlocation:
                    location = elem.get_text().strip("\n \r")
                for elem in divdomaine:
                    domaine = elem.get_text().strip("\n \r")
                for elem in divdescription:
                    descriptionE =elem.get_text().strip("\n \r")

            compte.addExperience(nom, date, location, description, actif, urlsExperiences[numExp], nomE, descriptionE, domaine)

            #++
            numExp = numExp + 1

        return compte

if __name__ == '__main__':
    manager = SeleniumManager(3)
    search = SearcherLinkedin(manager)
    liste = search.findLinkedinsKeyWord("frank candido president")
    liste = list(liste)
    #liste = search.findLinkedins("candido", "frank", entreprise="nuran")
    #test pour cas plusieurs page = nbr résultat = 13
    #liste = search.findLinkedins("Legros", "camille")

    file_tmp = ""
    name_date_file = datetime.now().strftime('%H%M%d%m%Y')
    if sys.version_info >= (3, 0):
        file_tmp=open('log/sLinkedin_py_recherche'+name_date_file+'.log', 'w+', encoding="utf8")
    else:
        file_tmp=open('log/sLinkedin_py_recherche'+name_date_file+'.log', 'w+')
    for val in liste:
        print(val)
        ecriturePython2_Python3(file_tmp, val)
        file_tmp.write('\n')
    file_tmp.close()

    file_tmp = ""
    if sys.version_info >= (3, 0):
        file_tmp=open('log/sLinkedin_py_info'+name_date_file+'.log', 'w+', encoding="utf8")
    else:
        #cas ou c'est en python2, il faudra dire que l'encodage sera fait en utf8 lors de l'écriture dans le fichier via str.encode(utf8) (qui fonctionne pas en python3 sinon c'est pas drole)
        file_tmp=open('log/sLinkedin_py_info'+name_date_file+'.log', 'w+')

    if len(liste) > 0 :
        compte = search.findLinkedin("candido", "frank", liste[0], file_tmp)
        compte.homonymes = liste[1:]
        for experience in compte.experiences:
            if platform.system() == "Windows":
                file_tmp.write('\n\n')
                ecriturePython2_Python3(file_tmp,"date:"+experience.date+'\n')
                ecriturePython2_Python3(file_tmp,"description:"+experience.description+'\n')
                ecriturePython2_Python3(file_tmp,"urlEntreprise:"+experience.urlEntreprise+'\n')
                ecriturePython2_Python3(file_tmp,"nomExperience:"+experience.nomExperience+'\n')
                ecriturePython2_Python3(file_tmp,"nomEntreprise:"+experience.nomEntreprise+'\n')
                ecriturePython2_Python3(file_tmp,"geolocalisation:"+experience.geolocalisation+'\n')
                ecriturePython2_Python3(file_tmp,"descriptionE:"+experience.descriptionEntreprise+'\n')
                ecriturePython2_Python3(file_tmp,"domaine:"+experience.domaineEntreprise+'\n')
                ecriturePython2_Python3(file_tmp,"expActif? %s \n" % experience.actif)

            else:
                print("date:",experience.date)
                print("description", experience.description)
                print("urlEntreprise", experience.urlEntreprise)
                print("nomExperience", experience.nomExperience)
                print("nomEntreprise", experience.nomEntreprise)
                print("geolocalisation", experience.geolocalisation)
                print("descriptionE", experience.descriptionEntreprise)
                print("domaine", experience.domaineEntreprise)
                print("expActif?", experience.actif)
    file_tmp.close()
    manager.driver_quit()
