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
    nbr_vrai = 0
    nbr_loc_null_pre = 0
    nbr_loc_null_ent = 0
    nbr_desc_null_pre = 0
    nbr_desc_null_ent = 0
    nbr_loc_desc_null_pre = 0
    nbr_loc_desc_null_ent = 0

    nbrs_entreprises = 0
    entreprises = []
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
                complet = True
                if row.get('user_location') == "null":
                    nbr_loc_null_ent = nbr_loc_null_ent + 1
                if row.get('user_description') == "null":
                    nbr_desc_null_ent = nbr_desc_null_ent + 1
                if (row.get('user_description') == "null") & (row.get('user_location') == "null"):
                    nbr_loc_desc_null_ent = nbr_loc_desc_null_ent + 1
                entreprises.append(row.get('user_name'))
                nbrs_entreprises = nbrs_entreprises + 1
            else:
                if row.get('user_location') == "null":
                    nbr_loc_null_pre = nbr_loc_null_pre + 1
                if row.get('user_description') == "null":
                    nbr_desc_null_pre = nbr_desc_null_pre + 1
                if (row.get('user_description') == "null") & (row.get('user_location') == "null"):
                    nbr_loc_desc_null_pre = nbr_loc_desc_null_pre + 1

    for val in entreprises:
        print val

    print nbr_vrai
    print "entreprises", nbrs_entreprises, "soit:", float(float(nbrs_entreprises)/float(nbr_vrai))

    nbr_loc_null_ent = nbr_loc_null_ent - nbr_loc_desc_null_ent
    nbr_desc_null_ent = nbr_desc_null_ent - nbr_loc_desc_null_ent

    print "complet:", nbrs_entreprises-nbr_loc_null_ent-nbr_desc_null_ent-nbr_loc_desc_null_ent, " soit:", float(float(nbrs_entreprises-nbr_loc_null_ent-nbr_desc_null_ent-nbr_loc_desc_null_ent)/float(nbrs_entreprises))
    val = float(float(nbr_loc_null_ent)/float(nbrs_entreprises))
    print "location null:", nbr_loc_null_ent, " soit:", val
    print "avec location:", nbrs_entreprises-nbr_loc_null_ent, " soit:", 1-val
    val = float(float(nbr_desc_null_ent)/float(nbrs_entreprises))
    print "description null:", nbr_desc_null_ent, " soit:", val
    print "avec description:", nbrs_entreprises-nbr_desc_null_ent, " soit:", 1-val
    val = float(float(nbr_loc_desc_null_ent)/float(nbrs_entreprises))
    print "loc&desc null:", nbr_loc_desc_null_ent, " soit:", val
    print "avec un des 2:", nbrs_entreprises-nbr_loc_desc_null_ent, " soit:", 1-val
    print "personnes", nbr_vrai - nbrs_entreprises, "soit:", float(float(nbr_vrai - nbrs_entreprises)/float(nbr_vrai))

    nbr_loc_null_pre = nbr_loc_null_pre - nbr_loc_desc_null_pre
    nbr_desc_null_pre = nbr_desc_null_pre - nbr_loc_desc_null_pre

    print "complet:", (nbr_vrai-nbrs_entreprises)-nbr_loc_null_pre-nbr_desc_null_pre-nbr_loc_desc_null_pre, " soit:", float(float((nbr_vrai-nbrs_entreprises)-nbr_loc_null_pre-nbr_desc_null_pre-nbr_loc_desc_null_pre)/float(nbr_vrai-nbrs_entreprises))
    val = float(float(nbr_loc_null_pre)/float(nbr_vrai - nbrs_entreprises))
    print "location null:", nbr_loc_null_pre, " soit:", val
    print "avec location", nbrs_entreprises-nbr_loc_null_pre, " soit:", 1-val
    val = float(float(nbr_desc_null_pre)/float(nbr_vrai - nbrs_entreprises))
    print "description null:", nbr_desc_null_pre, " soit:", val
    print "avec description:", nbrs_entreprises-nbr_desc_null_pre, " soit:", 1-val
    val = float(float(nbr_loc_desc_null_pre)/float(nbr_vrai - nbrs_entreprises))
    print "loc&desc null:", nbr_loc_desc_null_pre, " soit:", val
    print "avec un des 2:", nbrs_entreprises-nbr_loc_desc_null_pre, " soit:", 1-val
finally:
    file.close()
    file3.close()
