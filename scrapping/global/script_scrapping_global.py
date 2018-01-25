import csv
import os
import re
import sys
from test_google import *

fname = "../../csv/iteration_500.csv"
file = open(fname, "rt", encoding="utf-8")

try:
    reader = csv.DictReader(file, delimiter=',')
    print ("Titres ", reader.fieldnames)

    #200000_tweets_simplifier:
    #tweet_id                   -> 0
    #tweet_created_at           -> 1
    #tweet_text                 -> 2
    #hashtags                   -> 3
    #tweet_quoted_status_id     -> 4
    #tweet_mtion                -> 5
    #pertinents                 -> 6
    #proba_pertinence           -> 7

    #user_id                    -> 8
    #user_screenname            -> 9

    #user_name                  -> 10
    #user_location              -> 11
    #user_description           -> 12
    
    for row in reader:
        row.get('user_name')
        if re.match(row.get('user_name'), "Frank Candido"):
            #if not(re.match(row.get('user_location'), "null")):
             #   result = search_google(row.get('user_name'), row.get('user_location'))
            #else:
            result = search_google(row.get('user_name'), "")
            
            for lien in result:
                print(" ", lien, " ")

    #result = search_google("Frank Candido", "")
    

finally:
    file.close()
