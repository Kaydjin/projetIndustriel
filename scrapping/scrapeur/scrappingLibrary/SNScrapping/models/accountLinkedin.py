#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

class Experience:

    def __init__(self, nom, date, geolocalisation, description, actif, urlEntreprise, nomEntreprise, descriptionEntreprise, domaineE):
        self.nomExperience = nom
        self.date = date
        self.geolocalisation = geolocalisation
        self.description = description
        self.actif = actif

        self.urlEntreprise = urlEntreprise
        self.descriptionEntreprise = descriptionEntreprise
        self.domaineEntreprise = domaineE
        self.nomEntreprise = nomEntreprise

        def synthesePerson(self):
            return self.nomExperience + self.date + self.geolocalisation + self.description + self.nomEntreprise + self.domaineEntreprise

        def syntheseCompany(self):
            return self.nomEntreprise + self.geolocalisation + self.domaineEntreprise + self.descriptionEntreprise
            
class CompteLinkedin:

    def __init__(self, nom, prenom, url):
        self.homonymes = []
        self.url = url
        self.favoris = []
        self.etudes = []
        self.experiences = []
        self.complementaire = ""

    def addFavori(self, x):
        self.favoris.append(x)

    def addEtude(self, x):
        self.etudes.append(x)

    def addExperience(self, nom, date, geolocalisation, description, actif, urlEntreprise, nomE, descriptionE, domaineE):
        self.experiences.append(Experience(nom, date, geolocalisation, description, actif, urlEntreprise, nomE, descriptionE, domaineE))

    def addHomonyme(self, x):
        self.homonymes.append(x)

    def allActiveEntreprise(self):
        liste = []
        for s in self.experiences:
            if s.actif == True:
                liste.append(s)

        return liste

    def syntheseCompany(self, active):
        strRes = ""
        for s in self.experiences:
            if s.actif==active:
                strRes = strRes + s.syntheseCompany() + " "

        return strRes

    def synthesePerson(self):
        strFavoris = ""
        for s in self.favoris:
            strFavoris = strFavoris + s+" "
        strEtudes = ""
        for s in self.etudes:
            strEtudes = strEtudes + s+" "
        strExperiences = ""
        for s in self.experiences:
            strExperiences = strExperiences + s.synthesePerson() +" "

        return strEtudes + " " + strExperiences + " " + self.complementaire + " " + strFavoris