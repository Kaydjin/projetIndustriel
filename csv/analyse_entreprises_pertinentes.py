import csv
import nltk

#CSV ouvrir les 500 pertinents pour analyser les champs de noms

fname = "iteration_500.csv"
file = open(fname, "rt")

fname3 = "prenoms.csv"
file3 = open(fname3, "rt")

try:
    reader = csv.DictReader(file, delimiter=',')
    reader3 = csv.DictReader(file3, delimiter=',')

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
    for row in reader3:
        liste.append(row.get('prenom').lower())

    corpus_compagnie = ['news', 'consulting', 'inc', 'investing', 'corp', 'talk', 'energy', 'communications']
    corpus_news = ['news', 'report', 'talk', 'media']
    nbr_vrai = 0
    nbrs_entreprises = 0
    entreprises = []
    boolea = True
    for row in reader:
        if 'VRAI' in row.get('Pertinent'):
            nbr_vrai = nbr_vrai + 1
            compagnie = True
            for val in row.get('user_name').split(' '):
                if val.lower() in liste:
                    compagnie = False
            for val in corpus_compagnie:
                if val in row.get('user_name').lower():
                    compagnie = True
            if compagnie:
                boolea = True
                for val in corpus_news :
                    if val in row.get('user_location').lower():
                        boolea = False
                    if val in row.get('user_description').lower():
                        boolea = False
                    if val in row.get('user_name').lower():
                        boolea = False
                if boolea:
                    if not "company" in row.get('user_description').lower():
                        entreprises.append(row.get('user_name'))
                        nbrs_entreprises = nbrs_entreprises + 1
                        print row.get('user_name'), row.get('user_description')

    print nbr_vrai
    print nbrs_entreprises
finally:
    file.close()
    file3.close()
