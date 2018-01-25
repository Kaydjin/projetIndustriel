import csv
import os
import re
import sys
from test_google import *
#from linkedIn_Recherche import *

#fichier contenant les tweets
fname = "../../csv/iteration_500.csv"
file = open(fname, "rt", encoding="utf-8")

try:
    reader = csv.DictReader(file, delimiter=',')
    print ("Titres ", reader.fieldnames)

    result = []
    #lecture ligne par ligne du fichier csv
    for row in reader:
        if re.match(row.get('user_name'), "Frank Candido"):
            """
            #si le champ localisation est remplis, on l'utilise.
            if not(re.match(row.get('user_location'), "null")):
                result = search_google(row.get('user_name'), row.get('user_location'))
            else:
            """
            result_intermediare = search_google(row.get('user_name'), "")
            print(result_intermediare)
            result.append(result_intermediare)
              
    
    for lien in result:
        print(" ", lien, " ")
    print("\n")


    #result = search_google("Frank Candido", "")
    

finally:
    file.close()
