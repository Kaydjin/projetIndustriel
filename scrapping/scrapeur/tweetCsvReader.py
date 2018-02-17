#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import nltk
import string
import re
from nltk.corpus import stopwords        

class TweetCSV:
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

    def __init__(self, idd, date, text, tags, quotedId, mention, pertinent, p, 
        userId, userScreenname, userName, userLocation, userDescription, typeAuteur, prenom, nom):
        self.id = idd
        self.date = date
        self.text = text
        self.tags = tags
        self.quotedId = quotedId
        self.mention = mention
        self.pertinent = pertinent
        self.proba = p
        self.userId = userId
        self.userScreenname = userScreenname
        self.userName = userName
        self.userNom = nom
        self.userPrenom = prenom
        self.userLocation = userLocation
        self.userDescription = userDescription
        self.typeAuteur = typeAuteur


class Reader:

    def __init__(self, fileNameCsv):
        self.fileNameCsv = fileNameCsv
        self.tweets = []

    def read(self):

        #instanciation de fichier csv
        if(sys.version_info > (3,0)):
            file = open(self.fileNameCsv, "rt",encoding = "utf8")
        else:
            file = open(self.fileNameCsv, "rt")
            
        fname = "res/prenoms.csv"
        file2 = open(fname, "rt")

        try:
            #connection aux fichiers csv.
            reader = csv.DictReader(file, delimiter=',')
            reader2 = csv.DictReader(file2, delimiter=',')

            #on transforme les prenoms en une liste sans capital
            liste = []
            for row in reader2:
                liste.append(row.get('prenom').lower())

            #on cree une liste de mots souvent present dans une compagnie
            corpus_compagnie = ['news', 'consulting', 'inc', 'investing', 'corp', 'talk','stocks','stock', 'resources',
            'energy', 'communications','digital','news', 'report', 'talk', 'media','publishing',
                                'mine','mining', 'live', 'investors', 'international', 'office', 'partners', 'environment','group',
                                'radio', 'network','wire','wired','financial', 'economic', 'traders', 'trade', 'information',
                                'networks','limited','electronics', 'corporation', 'company', 'entertainment', 'productions', 'tech','sciences',
                                'research','production', 'solutions', 'sports', 'systems', 'records', 'journal', 'exploration','exploror']

            #instanciation de la liste des descriptions a analyser
            descriptions = []

            #pour tous les elements trouves dans le csv
            for row in reader:

                pertinent = False
                #si l'element est pertinent
                if 'VRAI' in row.get('Pertinent'):
                    pertinent = True


                #on ne continue pas si l'element est une compagnie ou une organisation
                typeAuteur = "Indeterminer"
                determiner = False
                for companyWord in corpus_compagnie:
                    if companyWord in row.get('user_name').lower():
                        typeAuteur = "Compagnie"
                        determiner = True

                #Instanciation à vide pour les tweets ne provenant pas de personnes
                prenom = ""
                nom = ""

                #Test d'un auteur de type personne
                if not determiner:
                    # on separe tous les elements composant le champ nom
                    for val in row.get('user_name').split(' '):

                        # on verifie si un prenom existe dans le champ user_name
                        if val.lower() in liste:
                            typeAuteur = "Personne"
                            prenom = val.lower()
                            nom = row.get('user_name').replace(val, "")
                            nom = nom.strip()

                self.tweets.append(TweetCSV(row.get('tweet_id'),
                                            row.get('tweet_created_at'),
                                            row.get('tweet_text'),
                                            row.get('hashtags'),
                                            row.get('tweet_quoted_status_id'),
                                            row.get('tweet_mtion'),
                                            pertinent,
                                            row.get('proba_pertinence'),
                                            row.get('user_id'),
                                            row.get('user_screenname'),
                                            row.get('user_name'),
                                            row.get('user_location'),
                                            row.get('user_description'),
                                            typeAuteur, prenom, nom
                                            ))

        finally:
            file.close()
            file2.close()

    def getSomeoneTweets(self, nom, prenom, pertinent):
        someoneTweets = []
        for tweet in self.tweets:
            if (tweet.pertinent==pertinent) & (nom.lower() in tweet.userName.lower())& (prenom.lower() in tweet.userName.lower()):
                someoneTweets.append(tweet)
        return someoneTweets

    def getIndeterminatedTweets(self, pertinent):
        indeterminer = []
        for tweet in self.tweets:
            if (tweet.pertinent==pertinent) & (tweet.typeAuteur == "Indeterminer"):
                indeterminer.append(tweet)
        return indeterminer

    def getPeopleTweets(self, pertinent):
        people = []
        for tweet in self.tweets:
            if (tweet.pertinent==pertinent) & (tweet.typeAuteur == "Personne"):
                people.append(tweet)
        return people

    def getCompagnieTweets(self, pertinent):
        compagnie = []
        for tweet in self.tweets:
            if (tweet.pertinent==pertinent) & (tweet.typeAuteur == "Compagnie"):
                compagnie.append(tweet)
        return compagnie


# test de la class TweetCSVReader
if __name__ == '__main__':

    fname = "iteration_500.csv"
    reader = Reader(fname)
    reader.read()
    #tweets = reader.getIndeterminatedTweets(True)
    tweets = reader.getCompagnieTweets(True)
    tweets.extend(reader.getCompagnieTweets(False))
    tweets = list(set(tweets))
    for t in tweets:
        print(t.userName)