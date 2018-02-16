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
    prenom = [["Frank Candido", "Montreal, Canada"],
["James Dean" ,"World Wide"],
["Steve Thomas",] ,
["michael dehn" ,"United Kingdom"],
["John Pentony ", "Canada"],
["Marijke van der Lee" ,"null"],
["FRANCIS K S LIM ","Thailand Malaysia Indonesia "],
["Brandon Macdonald", "Vancouver, BC"], 
["John Pentony ", "United States"],
["Gilbert Rono ", "Bomet, Kenya"],
["Mable Twegumye Zake", "Kampala, Uganda"],
["Ronald Ssekandi ", ""],
["Africa Report", "Africa"],
["Paul Jones","Canada "],
["Amara Pope","Vancouver, British Columbia"],
["Elizabeth Block","London"],
["Peter Bell",""],
["Louis Jadwong","Uganda"],
["Paul Jones","Canada"],
["Randy hilzinger",""],
["Douglas British","Columbia, Canada"],
["Julius Businge","Kampala"],
["Edwin Muhumuza","Kampala"]]
    result = []
    #lecture ligne par ligne du fichier csv
    """
    for row in reader:
        print(row.get('user_name'))
        if re.match( "Frank Candido",row.get('user_name')):
            
            #si le champ localisation est remplis, on l'utilise.
            if not(re.match(row.get('user_location'), "null")):
                result = search_google(row.get('user_name'), row.get('user_location'))
            else:
            
            result_intermediare = search_google(row.get('user_name'), "")
            print(result_intermediare)
            result.append(result_intermediare)
            """
    for nom,lieu in prenom:
        result_intermediare = search_google(nom, lieu)
        print(result_intermediare)
        result.append(result_intermediare)
    
    for lien in result:
        print(" ", lien, " ")
    print("\n")


    #result = search_google("Frank Candido", "")
    

finally:
    file.close()
