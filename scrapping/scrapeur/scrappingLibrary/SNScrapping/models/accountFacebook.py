#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

class CompteFacebook:

	def __init__(self, nom, prenom, url):
		self.homonymes = []
		self.description = ""
		self.url = url
		self.favoris = []
		self.nomsExperiences = []
		self.detailsExperiences = []
		self.nomsEtudes = []
		self.detailsEtudes = []
		self.geodonnees = []
		self.complementaire = ""

	def addFavori(self, x):
		self.favoris.append(x)

	def addGeoDonnee(self, x):
		self.geodonnees.append(x)

	def addExperience(self, exp, detail):
		self.nomsExperiences.append(exp)
		self.detailsExperiences.append(detail)

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
		num=0
		for s in self.nomsExperiences:
			strExperiences = strExperiences + s+ " " + self.detailsExperiences[num] + " "
			num = num + 1

		strEtudes = ""
		num=0
		for s in self.nomsEtudes:
			strEtudes = strEtudes+ s + " " + self.detailsEtudes[num] + " "
			num = num + 1


		strGeoDonnee = ""
		for s in self.geodonnees:
			strGeoDonnee = strGeoDonnee + s+ " "

		return self.description + " " + strEtudes + " " + strExperiences + " " + self.complementaire + " " + strGeoDonnee + " " + strFavoris