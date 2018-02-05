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
from linkedIn_Recherche import *

def inforPersonne():

    # initialize selenium webdriver - pass latest chromedriver path to webdriver.Chrome()
    #On gere ici si l'os qui lance l'appli est windows ou Linux
    #TODO Mac si besoin, il faudra par contre telecharger le driver de mac
    os_driver = "error"
    if platform.system().find("Windows") != -1 :
        os_driver = "/geckodriver_windows64.exe"
    elif platform.system().find("Linux") != -1 :
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

        profile_link="https://www.linkedin.com/in/marcbenioff/fr"
        driver.get(profile_link)

        # wait for page load
        time.sleep(3)

        html=driver.page_source

        #pv-profile-section experience-section
        #pv-profile-section experience-section ember-view

        soup=bs4.BeautifulSoup(html, "html.parser") #specify parser or it will auto-select for you


        compte = CompteLinkedin("benioff", "marc", profile_link)

        experience = soup.select('.pv-profile-section.experience-section.ember-view a')
        #valeurs = soup.find_all('section', class_='experience-section')
        urlsExperiences = []
        for elem in experience:
            if(elem.get_text() != ''):
                urlsExperiences.append("https://www.linkedin.com"+elem.get('href'))

        for url in urlsExperiences:

            driver.get(url)
            # wait for page load
            time.sleep(3)
            html=driver.page_source
            soup=bs4.BeautifulSoup(html, "html.parser") #specify parser or it will auto-select for you
            divnom = soup.select('.org-top-card-module__name')
            divdomaine = soup.select('.company-industries.org-top-card-module__dot-separated-list')
            divlocation = soup.select('.org-top-card-module__location')
            divdescription = soup.select('.org-about-us-organization-description p')
            for elem in divnom:
                print(elem.get_text().strip("\n \r"))
            for elem in divdomaine:
                print(elem.get_text().strip("\n \r"))
            for elem in divlocation:
                print(elem.get_text().strip("\n \r"))
            for elem in divdescription:
                print(elem.get_text())

        liclient.driver_quit()
        
if __name__ == '__main__':
    inforPersonne()  
