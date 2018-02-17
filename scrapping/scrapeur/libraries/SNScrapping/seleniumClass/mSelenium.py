#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import platform
import time

class SeleniumManager:

    def __init__(self, waiting_time):
        os_driver = "error"

        """ different drivers selon l'os"""
        if platform.system() == "Windows":
            os_driver = "/libraries/SNScrapping/seleniumClass/geckodriver_windows64.exe"
        elif platform.system() == "Linux":
            os_driver = "geckodriver_linux"
        else :
            print("OS non supporte")
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