#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os
#chemin vers le module
os.chdir("D:\M2S1\Projet_Indu\projetIndustriel\scrapping\global\Google-Search-API-master\google")
from google import google

"""
-nom_complet correspond au nom de la personne ou entreprise que l'on recherche
-complementaire contient une chaine de mots séparés par des espaces. Ceux-ci précise par exemple la localisation de l'entité recherchée.
-reseausocial correspond au réseau social sur lequel l'on recherche la personne
-entreprise est un boolean précisant si l'on recherche une entreprise (True) ou une personne (False)
"""
def search_google(nom_complet, complementaire, reseausocial, entreprise):
    result = []
    num_page = 1
    #cas où nous recherchons une personne
    if(not entreprise):
        #nous séparons le nom_complet en prénom et nom
        prenom = ""
        nom = ""
        fin_prenom = False
        for c in nom_complet:
            if(not fin_prenom):
                if(c == " "):
                    fin_prenom = True
                else:
                    prenom += c
            else:
                nom += c
        #formation de la chaine de caractère qui sera utilisée dans le moteur de recherche
        query = prenom + " " + nom + " " + complementaire + " " + reseausocial
        #appel de la méthode de la libraire permettant d'obtenir les résultats de la recherche
        listurls = google.search(query, num_page)
        #la suppression des accents facilite la vérification de la pertinance des résultat
        nom = supprime_accent(nom)
        prenom = supprime_accent(prenom)
        for i in listurls:
            i_sans_accent = supprime_accent(i.link)
            #comme nous recherchons une personne il nous suffit de trouver un lien correspondant puis de chercher dans les homonymes
            if(reseausocial == "facebook" and len(result) < 1 and
                re.match(".*FACEBOOK\.COM/" + prenom.upper() + ".*" + nom.upper() + ".*", i_sans_accent.upper())):
                    result.append(i.link)
            elif(reseausocial == "linkedin" and 
                re.match(".*LINKEDIN.*"+ prenom.upper() + ".*" + nom.upper() + ".*", i_sans_accent.upper())):
                    result.append(i.link)
    #cas d'une recherche d'entreprise
    else:
        query = nom_complet + " " + complementaire + " " + reseausocial
        listurls = google.search(query, num_page)
        nom = supprime_accent(nom_complet)
        nom_sans_espace = ""
        for c in nom:
            if c != " ":
                nom_sans_espace += c
            else:
                nom_sans_espace += ".*"
        for i in listurls:
            i_sans_accent = supprime_accent(i.link)
            if (reseausocial == "facebook" and 
            re.match(".*FACEBOOK.*" + nom_sans_espace.upper() + ".*", i_sans_accent.upper())):
                    result.append((i.link,i.description))
            elif (reseausocial == "linkedin" and 
                re.match(".*LINKEDIN.*" + nom_sans_espace.upper() + ".*", i_sans_accent.upper())):
                    result.append((i.link,i.description))
            else:
                if re.match(".*" + nom_sans_espace.upper() + ".*", i_sans_accent.upper()):
                    result.append((i.link,i.description))
    return result

"""
def search_google_facebook(nom, prenom, queryFacebook):
    result = []
    num_page = 1
    listurls = google.search(queryFacebook, num_page)
    #listurls = search(queryFacebook, tld="com", num=10, stop=1, pause=2)
    for i in listurls:
        #ne recupere que le premier resultat
        if (len(result) < 1):
            #supprimer les accents sert a généraliser la recherche
            i_sans_accent = supprime_accent(i.link)
            if re.match(".*FACEBOOK\.COM/" + prenom.upper() + ".*" + nom.upper() + ".*", i_sans_accent.upper()):
                result.append(i.link)
    return result

def search_google_linkedin(nom, prenom, queryLinkedIn):
    result = []
    num_page = 1
    listurls = google.search(queryLinkedIn, num_page)
    #listurls = search(queryLinkedIn, tld="com", num=10, stop=1, pause=2)
    for j in listurls:
        if (len(result) < 1):
            j_sans_accent = supprime_accent(j.link)
            if re.match(".*LINKEDIN.*"+ prenom.upper() + ".*" + nom.upper() + ".*", j_sans_accent.upper()):
                result.append(j.link)
                
    return result

def search_google_entreprise(nom, queryEntreprise):
    result = []
    num_page = 1
    listurls = google.search(queryEntreprise, num_page)
    #listurls = search(query, tld="com", num=10, stop=1, pause=2)
    for i in listurls:
        #supprimer les accents sert a généraliser la recherche
        i_sans_accent = supprime_accent(i.link)
        if re.match(".*" + nom.upper() + ".*", j_sans_accent.upper()):
            result.append((i.link,i.description))
    return result

def search_google_entreprise_linkedin(nom, queryEntrepriseLinkedin):
    result = []
    num_page = 1
    listurls = google.search(queryEntrepriseLinkedin, num_page)
    for i in listurls:
        i_sans_accent = supprime_accent(i.link)
        if re.match(".*LINKEDIN.*" + nom.upper() + ".*", i_sans_accent.upper()):
            result.append((i.link,i.description))
    return result

def search_google_entreprise_facebook(nom, queryEntrepriseFacebook):
    result = []
    num_page = 1
    listurls = google.search(queryEntrepriseFacebook, num_page)
    for i in listurls:
        i_sans_accent = supprime_accent(i.link)
        if re.match(".*FACEBOOK.*" + nom.upper() + ".*", i_sans_accent.upper()):
            result.append((i.link,i.description))
    return result
"""
def supprime_accent(ligne):
        """ supprime les accents du texte source """
        accents = { 'a': ['à', 'ã', 'á', 'â', 'ä', 'å'],
                    'ae': ['æ'],
                    'c': ['ç'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï', 'í', 'ì'],
                    'u': ['ù', 'ù', 'ü', 'û'],
                    'o': ['ô', 'ö', 'ó', 'ò', 'õ'],
                    'oe': ['œ'],
                    'n': ['ñ'],
                    'y': ['ý', 'ÿ'] }
        for (char, accented_chars) in accents.items():
            for accented_char in accented_chars:
                ligne = ligne.replace(accented_char, char)
        return ligne


if __name__ == '__main__':
    #liste_sites = search_google("Frank Candido", "", "linkedin", False)
    #print(liste_sites)
    liste_sites = search_google("BigMoneyTraders","","",True)
    for i,j in liste_sites:
        print(i," ==> ",j,"\n")
    