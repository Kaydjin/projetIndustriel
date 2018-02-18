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
