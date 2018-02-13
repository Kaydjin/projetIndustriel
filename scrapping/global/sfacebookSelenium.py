from selenium import webdriver
from client import LIClientFacebook
from settings import search_keys
from datetime import datetime
import sys
import argparse
import time
import os
import bs4
import platform


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

class SearcherFacebook_Selenium:

    def __init__(self, manager):
        self.manager = manager

        """ pause time 0 car on doit initialiser liclient avant d'attendre """
        self.manager.get("https://www.facebook.com/login/", 0)

        # initialize LinkedIn web client
        liclient = LIClientFacebook(manager.driver, **search_keys)
        liclient.login()
        time.sleep(3)

    def findFacebookScrolling(self):
    	#Chargement de la page /!\ 
        time.sleep(2)

        html=manager.driver.page_source
        soup=bs4.BeautifulSoup(html, "html.parser")

        pattern = 'End of Results'

        end = soup.find('div', text=pattern)

        while end == None :
        	manager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        	time.sleep(1)
        	html=manager.driver.page_source
        	soup=bs4.BeautifulSoup(html, "html.parser")
        	end = soup.find('div', text=pattern)

        html=manager.driver.page_source
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
    	manager.get(profile_link, 3)
    	return self.findFacebookScrolling()



def ecriturePython2_Python3(file, myStr):
    if sys.version_info >= (3,0):
        file.write(myStr)
    else:
        file.write(myStr.encode('utf8'))

if __name__ == '__main__':
	manager = SeleniumManager(3)
	search = SearcherFacebook_Selenium(manager)
	liste = search.findFacebook('candido','frank')
	file = ""
	name_date_file = datetime.now().strftime('%H%M%d%m%Y')
	if sys.version_info >= (3, 0):
		file=open('log/sfacebookRecherche'+name_date_file+'.log', 'w+', encoding="utf8")
	else:
		file=open('log/sfacebookRecherche'+name_date_file+'.log', 'w+')
	for val in liste:
		print(val)
		ecriturePython2_Python3(file, val)
		file.write('\n')
	file.close()


	manager.driver_quit()
