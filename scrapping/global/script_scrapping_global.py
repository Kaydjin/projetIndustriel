import csv
import os
import re
import sys
from test_google import *
from linkedin_Recherche import *

fname = "../../csv/iteration_500.csv"
file = open(fname, "rt", encoding="utf-8")

try:
    reader = csv.DictReader(file, delimiter=',')
    print ("Titres ", reader.fieldnames)
   
    for row in reader:
        row.get('user_name')
        if re.match(row.get('user_name'), "Frank Candido"):
            if not(re.match(row.get('user_location'), "null")):
                result = search_google(row.get('user_name'), row.get('user_location'))
            else:
                result = search_google(row.get('user_name'), "")
        
        if(len(result) != 0):
            for lien in result:
                print(" ", lien, " ")
            print("\n")


    #result = search_google("Frank Candido", "")
    

finally:
    file.close()
