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

        file=open('scrapping_InfoPerson.log', 'w+')

        soup=bs4.BeautifulSoup(html, "html.parser") #specify parser or it will auto-select for you


        valeurs = soup.find_all('section', class_='experience-section')
        if len(valeurs)>0:
            file.write('Données:\n')
            for elem in valeurs:
                if(elem.get_text() != ''):
                    file.write(elem.get_text())
                    file.write('\n')
        else:
            file.write('- no data -\n')
        
        """valeurs = soup.select('.background-details .pv-profile-section__card-item .pv-entity__summary-info')
        if len(valeurs)>0:
            print('Valeurs:')
            for elem in valeurs:
                print(elem)
        else:
            print('- no data -')"""

        """a=0
        valeurs = soup.select('.background-details .pv-profile-section .experience-section .pv-profile-section__card-item .pv-entity__summary-info span')
        if len(valeurs)>0:
            file.write('Experience:\n')
            for elem in valeurs:
                a=a+1
                if a%2==0:
                    file.write(elem.getText())
                    file.write('\n')
        else:
            file.write('- no data -\n')
        file.write('--------------------------------------------------\n')

        valeurs = soup.select('.background-details .pv-profile-section .experience-section .pv-profile-section__card-item .pv-entity__summary-info h3')
        if len(valeurs)>0:
            file.write('Experience:\n')
            for elem in valeurs:
                file.write(elem.getText())
                file.write('\n')
        else:
            file.write('- no data -\n')
        file.write('--------------------------------------------------\n')

        a=0
        valeurs = soup.select('.background-details .pv-profile-section .education-section .pv-profile-section__card-item .pv-entity__summary-info span')
        if len(valeurs)>0:
            file.write('Formation:\n')
            for elem in valeurs:
                a=a+1
                if a%2==0:
                    file.write(elem.getText())
                    file.write('\n')
        else:
            file.write('- no data -\n')
        file.write('--------------------------------------------------\n')

        valeurs = soup.select('.background-details .pv-profile-section .education-section .pv-profile-section__card-item .pv-entity__summary-info h3')
        if len(valeurs)>0:
            file.write('Formation:\n')
            for elem in valeurs:
                file.write(elem.getText())
                file.write('\n')
        else:
            file.write('- no data -\n')"""
        file.write('--------------------------------------------------\n')
        file.close()
        liclient.driver_quit()
        
inforPersonne()  
