import csv
import nltk

#CSV ouvrir les 500 pertinents pour analyser les champs de noms

fname = "iteration_500.csv"
file = open(fname, "rt")

fname2 = "analyse.csv"
file2 = open(fname2, "wb")

try:
    reader = csv.DictReader(file, delimiter=',')
    writer = csv.writer(file2)
    print "Titres ", reader.fieldnames 

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
        
finally:
    file.close()
    file2.close()
