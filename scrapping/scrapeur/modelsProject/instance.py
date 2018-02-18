#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Instance:

	def __init__(self, tweet):
		self.tweet = tweet
		self.linkLinkedinPerson = []
		self.linkFacebookPerson = []
		self.linkLinkedinCompany = []
		self.linkFacebookCompany= []
		self.accountLinkedinPerson = []
		self.accountFacebookPerson = []
		self.accountLinkedinCompany = []
		self.accountFacebookCompany = []
		self.entreprises = []

	def addLinkedinPersonLink(self, x):
		self.linkLinkedinPerson.append(x)

	def addFacebookPersonLink(self, x):
		self.linkFacebookPerson.append(x)

	def addFacebookCompanyLink(self, x):
		self.linkFacebookCompany.append(x)

	def addLinkedinCompanyLink(self, x):
		self.linkLinkedinCompany.append(x)

	def existLinkedinPersonLink(self, link, liste_etoiles):
		return self.existLink(self.linkLinkedinPerson, link, liste_etoiles)

	def existFacebookPersonLink(self, link, liste_etoiles):
		return self.existLink(self.linkLinkedinPerson, link, liste_etoiles)

	def existFacebookCompanyLink(self, link, liste_etoiles):
		return self.existLink(self.linkFacebookCompany, link, liste_etoiles)

	def existLinkedinCompanyLink(self, link, liste_etoiles):
		return self.existLink(self.linkLinkedinCompany, link, liste_etoiles)

	def existLink(self, list_link, link, liste_etoiles):
		for val in liste_etoiles:
			if (link, val) in self.linkLinkedinPerson:
				return True
		return False

	def printLinks(self):
		for link,nbEtoiles in self.linkFacebookPerson:
			print("FPerson:"+link)
		for link,nbEtoiles in self.linkFacebookCompany:
			print("FCompany:"+link)
		for link,nbEtoiles in self.linkLinkedinPerson:
			print("LPerson:"+link)
		for link,nbEtoiles in self.linkLinkedinCompany:
			print("LCompany:"+link)

	def addAccountLinkedinPerson(self, x):
		self.accountLinkedinPerson.append(x)

	def addAccountFacebookPerson(self, x):
		self.accountFacebookPerson.append(x)

	def addAccountFacebookCompany(self, x):
		self.accountFacebookCompany.append(x)

	def addAccountLinkedinCompnay(self, x):
		self.accountLinkedinCompany.append(x)

	def addEntreprise(self, x):
		self.entreprises.append(x)
