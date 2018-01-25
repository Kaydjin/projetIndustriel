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

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="""
        parse LinkedIn search parameters
        """)
    parser.add_argument('--username', type=str, required=True, 
        help="""
        enter LI username
        """)
    parser.add_argument('--password', type=str, required=True, 
        help="""
        enter LI password
        """)
    parser.add_argument('--keyword', default=search_keys['keywords'], nargs='*', 
        help="""
        enter search keys separated by a single space. If the keyword is more
        than one word, wrap the keyword in double quotes.
        """)
    parser.add_argument('--location', default=search_keys['locations'], nargs='*',
        help="""
        enter search locations separated by a single space. If the location 
        search is more than one word, wrap the location in double quotes.
        """)
    parser.add_argument('--search_radius', type=int, default=search_keys['search_radius'], nargs='?', 
        help="""
        enter a search radius (in miles). Possible values are: 10, 25, 35, 
        50, 75, 100. Defaults to 50.
        """)
    parser.add_argument('--results_page', type=int, default=search_keys['page_number'], nargs='?', 
        help="""
        enter a specific results page. If an unexpected error occurs, one can
        resume the previous search by entering the results page where they 
        left off. Defaults to first results page.
        """)
    parser.add_argument('--date_range', type=str, default=search_keys['date_range'], nargs='?', 
        help="""
        specify a specific date range. Possible values are: All, 1, 2-7, 8-14,
        15-30. Defaults to 'All'.
        """)
    parser.add_argument('--sort_by', type=str, default=search_keys['sort_by'], nargs='?', 
        help="""
        sort results by relevance or date posted. If the input string is not 
        equal to 'Relevance' (case insensitive), then results will be sorted 
        by date posted. Defaults to sorting by relevance.
        """)
    parser.add_argument('--salary_range', type=str, default=search_keys['salary_range'], nargs='?', 
        help="""
        set a minimum salary requirement. Possible input values are:
        All, 40+, 60+, 80+, 100+, 120+, 140+, 160+, 180+, 200+. Defaults
        to All.
        """)
    parser.add_argument('--filename', type=str, default=search_keys['filename'], nargs='?', 
        help="""
        specify a filename to which data will be written. Defaults to
        'output.txt'
        """)
    return vars(parser.parse_args())

if __name__ == "__main__":

    search_keys = parse_command_line_args()

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
    
    
