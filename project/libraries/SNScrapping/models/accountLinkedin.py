#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

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
		self.experiences.append(Experience(nom, date, geolocalisation, 
			description, actif, urlEntreprise, nomE, descriptionE, domaineE))

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
				 strRes = strRes + s.syntheseExperienceC() + " " 
		return strRes

	def synthese(self):
		return self.synthesePerson()

	""" return only simple information """
	def toJson(self):
		if len(self.experiences)>0:
			return ("\t\t[account]{\t\t\tlastExp:"+self.experiences[0].nomExperience+","+self.experiences[0].domaineEntreprise+"\n\t\t}")
		return "\t\t[account]{\n\t\t\t[]\n\t\t}"

	def synthesePerson(self):
		strFavoris = ""
		for s in self.favoris:
			strFavoris = strFavoris + s+" "
		strEtudes = ""
		for s in self.etudes:
			strEtudes = strEtudes + s+" "
		strExperiences = ""
		for s in self.experiences:
			strExperiences = (strExperiences + s.nomExperience + " "+s.date + " " + s.geolocalisation + " " 
						+s.description + " "+s.nomEntreprise + " " + s.domaineEntreprise + " ")

		return strEtudes + " " + strExperiences + " " + self.complementaire + " " + strFavoris


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

	def specifyCompany(self, nomEntreprise, urlEntreprise , descriptionEntreprise, domaineEntreprise):
		self.nomEntreprise = nomEntreprise
		self.urlEntreprise  = urlEntreprise 
		self.descriptionEntreprise = descriptionEntreprise
		self.domaineEntreprise = domaineEntreprise

	def syntheseExperienceP(self):
		return (self.nomExperience + " "+self.date + " " + self.geolocalisation + " " 
					+self.description + " "+self.nomEntreprise + " " + self.domaineEntreprise)

	def syntheseExperienceC(self):
		return self.nomEntreprise + " " + self.geolocalisation +" "+ self.domaineEntreprise +" "+ self.descriptionEntreprise

	""" return simple information in json format """
	def toJson(self):
		return ("\t\t[account]{\n\t\t\tnomEntreprise :"+self.nomEntreprise  +
				"\n\t\t\tgeolocalisation:"+self.geolocalisation +
				"\n\t\t\tdomaineEntreprise:"+self.domaineEntreprise+"\n\t\t}")