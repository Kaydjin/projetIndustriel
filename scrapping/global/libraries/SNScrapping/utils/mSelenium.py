from selenium import webdriver
import os
import platform
import time

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