import csv
import nltk

#CSV ouvrir les 500 pertinents pour analyser les champs de noms

fname = "iteration_500.csv"
file = open(fname, "rt")

fname3 = "prenoms.csv"
file3 = open(fname3, "rt")

fname2 = "analyse.csv"
file2 = open(fname2, "wb")

try:
    reader = csv.DictReader(file, delimiter=',')
    reader3 = csv.DictReader(file3, delimiter=',')
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
    
    liste = []
    for row in reader3:
        liste.append(row.get('prenom').lower())

    corpus_compagnie = ['news', 'consulting', 'inc', 'investing', 'corp', 'talk', 'energy', 'communications']
    nbr_vrai = 0
    nbrs_noms = 0

    writer.writerow(reader.fieldnames[10])
    for row in reader:
        if 'VRAI' in row.get('Pertinent'):
            nbr_vrai = nbr_vrai + 1
            continu = True
            for stopword in corpus_compagnie:
                if stopword in row.get('user_name').lower():
                    continu = False
            if continu:
                for val in row.get('user_name').split(' '):
                    if val.lower() in liste:
                        nbrs_noms = nbrs_noms + 1
                        print row.get('user_name')
                        writer.writerow(row.get('user_name'))

    print nbr_vrai
    print nbrs_noms
finally:
    file.close()
    file2.close()
    file3.close()
