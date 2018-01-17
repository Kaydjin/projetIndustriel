import csv
import nltk

#CSV ouvrir les 500 pertinents pour analyser les champs de noms

fname = "prenoms2.csv"
file = open(fname, "rt")

fname2 = "prenoms.csv"
file2 = open(fname2, "rt")

fname3 = "prenoms3.csv"
file3 = open(fname3, "wb")

try:
    reader = csv.DictReader(file, delimiter=',')
    reader2 = csv.DictReader(file2, delimiter=',')
    writer = csv.writer(file3)

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
    
    liste = []
    for row in reader:
        liste.append(row.get('prenom').lower())

    for row in reader2:
        if not row.get('prenom').lower() in liste:
            liste.append(row.get('prenom').lower())

    writer.writerow(reader.fieldnames[0])
    for val in liste:
        writer.writerow(val)

finally:
    file.close()
    file2.close()
    file3.close()
