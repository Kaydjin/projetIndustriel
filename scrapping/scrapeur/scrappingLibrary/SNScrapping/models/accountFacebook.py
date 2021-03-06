#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

class CompteFacebook:

	def __init__(self, nom, prenom, url):
		self.homonymes = []
		self.description = ""
		self.url = url
		self.favoris = []

		self.experiences = []

		self.nomsEtudes = []
		self.detailsEtudes = []

		self.geodonnees = []
		self.complementaire = ""

	def addFavori(self, x):
		self.favoris.append(x)

	def addGeoDonnee(self, x):
		self.geodonnees.append(x)

	def addExperience(self, exp, detail):
		self.experiences.append(Experience(exp, detail))

	def getNamesExperiences(self):
		liste = []
		for s in self.experiences:
			liste.append(s.nameExperience)
		return liste

	def addEtude(self, etud, detail):
		self.nomsEtudes.append(etud)
		self.detailsEtudes.append(detail)

	def addHomonyme(self, x):
		self.homonymes.append(x)

	def synthese(self):
		strFavoris = ""
		for s in self.favoris:
			strFavoris = strFavoris + s+ " "

		strExperiences = ""
		for s in self.experiences:
			strExperiences = strExperiences + s.syntheseExperienceP() + " "

		strEtudes = ""
		num=0
		for s in self.nomsEtudes:
			strEtudes = strEtudes+ s + " " + self.detailsEtudes[num] + " "
			num = num + 1


		strGeoDonnee = ""
		for s in self.geodonnees:
			strGeoDonnee = strGeoDonnee + s+ " "

		return self.description + " " + strEtudes + " " + strExperiences + " " + self.complementaire + " " + strGeoDonnee + " " + strFavoris

class Experience:

	def __init__(self, name, details):
		#Necessary datas
		self.nameExperience = name
		self.detailsExperience = details
		#Is the experience of actuality? : by default true for facebook
		self.active = True

		""" Company's specification """
		self.nameCompany = ""
		self.urlCompany = ""
		self.descriptionCompany = ""
		self.domainCompany = ""
		self.geolocalizationCompany = ""

	def specifyCompany(self, nameCompany, urlCompany, descriptionCompany, domainCompany, geolocalizationCompany):
		self.nameCompany = nameCompany
		self.urlCompany = urlCompany
		self.descriptionCompany = descriptionCompany
		self.domainCompany = domainCompany
		self.geolocalizationCompany = geolocalizationCompany	

	def syntheseExperienceP(self):
		return (self.nameExperience + " "+self.detailsExperience + " " + self.geolocalizationCompany + " " 
					+self.descriptionCompany + " "+self.nameCompany + " " + self.domainCompany)

	def syntheseExperienceC(self):
		return (self.nameCompany + " " + self.urlCompany +" "+ self.descriptionCompany +" "+ self.domainCompany + " " + self.geolocalizationCompany)

class CompteEntrepriseFacebook:

	def __init__(self,nom, url):
		self.nom=nom
		self.url=url
		self.geolocalisation = ""
		self.domaineEntreprise = ""
		self.nomComplet= ""

	def affiche(self):
		print("nom:%s" % self.nom)
		print("url:%s" % self.url)
		print("geolocalisation:%s" % self.geolocalisation)
		print("domaineEntreprise:%s" % self.domaineEntreprise)
		print("nomComplet:%s" % self.nomComplet)


