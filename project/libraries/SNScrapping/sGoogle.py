#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import sys
import os


if __name__ == '__main__':
    from google import google
    from utils.utils import *
else:
    from .google import google
    from .utils.utils import *
    



"""
-complete_name is the full name of the company or individual you wanted to search.
-complementary is a string which contain informations like the localisation.
-social_media is the social media within we search for.
-entreprise est un boolean précisant si l'on recherche une entreprise (True) ou une personne (False)
"""
def search_google(complete_name, complementary, social_media, entreprise):
    result = []
    if(not entreprise):
        result.extend(search_people(complete_name, complementary, social_media))
    else:
        result.extend(search_firm(complete_name, complementary, social_media))

    return result
"""
    
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
        #la suppression des accents facilite la vérification de la pertinance des résultat
        nom = supprime_accent(nom)
        prenom = supprime_accent(prenom)

        listurls = google.search(query, num_page)
        for i in listurls:
            i_sans_accent = supprime_accent(i.link)
            #comme nous recherchons une personne il nous suffit de trouver un lien correspondant puis de chercher dans les homonymes
            if(reseausocial == "facebook"):
                if(re.match(".*FACEBOOK\.COM/" + prenom.upper() + ".*" + nom.upper() + ".*", i_sans_accent.upper()) and
                 not re.match(".*/PUBLIC/.*",i_sans_accent.upper())):
                    result.append(i.link)
            elif(reseausocial == "linkedin"): 
                if(re.match(".*LINKEDIN.*"+ prenom.upper() + ".*" + nom.upper() + ".*", i_sans_accent.upper()) and
                   not (re.match(".*/PUB/DIR.*", i_sans_accent.upper()) or
                   re.match(".*/PULSE/.*", i_sans_accent.upper()))):
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
            if (reseausocial == "facebook"):
                if(re.match(".*\.FACEBOOK\.COM/" + nom_sans_espace.upper() + ".*", i_sans_accent.upper()) and 
                    not (re.match(".*/PUBLIC/.*", i_sans_accent.upper()) or 
                        re.match(".*/ABOUT.*", i_sans_accent.upper()) or
                        re.match(".*/POST.*", i_sans_accent.upper()))):
                    ajout = True
                    for val in ["is on Facebook", "est sur Facebook", "esta en Facebook",
                    d("è su Facebook"), "ist bei Facebook", d("está no Facebook") ]:
                        if(val in i.description):
                            ajout = False
                    if(ajout):    
                        result.append((i.link,i.description))

            elif (reseausocial == "linkedin"): 
                if(re.match(".*LINKEDIN/COMPANY/.*" + nom_sans_espace.upper() + ".*", i_sans_accent.upper()) and
                   not (re.match(".*/PUB/DIR.*", i_sans_accent.upper()) or
                   re.match(".*/PULSE/.*", i_sans_accent.upper()))):
                    result.append((i.link,i.description))
            else:
                if re.match(".*" + nom_sans_espace.upper() + ".*", i_sans_accent.upper()):
                    result.append((i.link,i.description))
    return result

"""

"""
method who search link for a social media with google
"""
def search_people(complete_name, complementary, social_media):
    result = []
    #separating firstname and lastname for better result with google search engine
    firstname = ""
    lastname = ""
    end_firstname = False
    for c in complete_name:
        if(not end_firstname):
            if(c == " "):
                end_firstname = True
            else:
                firstname += c
        else:
            lastname += c

    #formation de la chaine de caractère qui sera utilisée dans le moteur de recherche
    query = firstname + " " + lastname + " " + complementary + " " + social_media
    if(social_media == "facebook" ):
        result.extend(search_people_facebook(query, firstname, lastname))

    elif(social_media == "linkedin"):
        result.extend(search_people_linkedin(query, firstname, lastname))
    return result


def search_people_facebook(query, firstname, lastname):
    result = []
    num_page = 1
    #appel de la méthode de la libraire permettant d'obtenir les résultats de la recherche
    listurls = google.search(query, num_page)
    #la suppression des accents facilite la vérification de la pertinance des résultat
    lastname = delete_accent(lastname)
    firstname = delete_accent(firstname)
    listurls = google.search(query, num_page)
    for i in listurls:
        i_sans_accent = delete_accent(i.link)
        #comme nous recherchons une personne il nous suffit de trouver un lien correspondant puis de chercher dans les homonymes          
        if(re.match(".*FACEBOOK\.COM/" + firstname.upper() + ".*" + lastname.upper() + ".*", i_sans_accent.upper()) 
            and not (re.match(".*/PUBLIC/.*", i_sans_accent.upper()) or 
                    re.match(".*/ABOUT.*", i_sans_accent.upper()) or
                    re.match(".*/POST.*", i_sans_accent.upper()))):
            result.append(i.link)
    return result


def search_people_linkedin(query, firstname, lastname):
    result = []
    num_page = 1
    #appel de la méthode de la libraire permettant d'obtenir les résultats de la recherche
    listurls = google.search(query, num_page)
    #la suppression des accents facilite la vérification de la pertinance des résultat
    lastname = delete_accent(lastname)
    firstname = delete_accent(firstname)
    listurls = google.search(query, num_page)
    for i in listurls:
        i_sans_accent = delete_accent(i.link)
        #comme nous recherchons une personne il nous suffit de trouver un lien correspondant puis de chercher dans les homonymes          
        if(re.match(".*LINKEDIN.*" + firstname.upper() + ".*" + lastname.upper() + ".*", i_sans_accent.upper()) 
            and not (re.match(".*/PUB/DIR.*", i_sans_accent.upper()) or re.match(".*/PULSE/.*", i_sans_accent.upper()))):
                result.append(i.link)
    return result
                
def search_firm(complete_name, complementary, social_media):
    result = []
    query = complete_name + " " + complementary + " " + social_media
    name_whitout_space = ""
    for c in complete_name:
        if c != " ":
            name_whitout_space += c
        else:
            name_whitout_space += ".*"
    if(social_media == "facebook"):
        result.extend(search_firm_facebook(query, name_whitout_space))
    if(social_media == "linkedin"):
        result.extend(search_firm_linkedin(query, name_whitout_space))
    return result

def search_firm_facebook(query, name_whitout_space):
    result = []
    num_page = 1
    listurls = google.search(query, num_page)
    for i in listurls:
        i_sans_accent = delete_accent(i.link)
        if(re.match(".*\.FACEBOOK\.COM/" + name_whitout_space.upper() + ".*", i_sans_accent.upper()) 
            and not (re.match(".*/PUBLIC/.*", i_sans_accent.upper()) or 
                    re.match(".*/ABOUT.*", i_sans_accent.upper()) or
                    re.match(".*/POST.*", i_sans_accent.upper()))):
            add = True
            for val in ["is on Facebook", "est sur Facebook", "esta en Facebook",
            d("è su Facebook"), "ist bei Facebook", d("está no Facebook") ]:
                if(val in i.description):
                    add = False
            if(add):    
                result.append((i.link,i.description))
    return result

def search_firm_linkedin(query, name_whitout_space):
    result = []
    num_page = 1
    listurls = google.search(query, num_page)
    for i in listurls:
        i_sans_accent = delete_accent(i.link)
        #print("je suis au bon endroit")
        #print(".*LINKEDIN\.COM/COMPANY/.*", name_whitout_space.upper(), ".*", " =? ", i_sans_accent)
        if(re.match(".*LINKEDIN\.COM/COMPANY/.*" + name_whitout_space.upper() + ".*", i_sans_accent.upper()) 
            and not (re.match(".*/PUB/DIR.*", i_sans_accent.upper()) or
                       re.match(".*/PULSE/.*", i_sans_accent.upper()))):
            result.append((i.link,i.description))

    return result



""" delete accent from ligne """
def delete_accent(ligne):
    if sys.version_info < (3, 0):
        ligne = ligne.encode('utf8')
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
    #resultFacebook = search_google("Frank" + " " + "Candido", "", "facebook", False)
    liste_sites = search_google("amur minerals","","linkedin",True)
    print("\n\n\n")
    for i,j in liste_sites:
        print(i," ==> ",j,"\n")