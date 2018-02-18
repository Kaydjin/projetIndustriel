#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Instance:

    def __init__(tweet):
        self.tweet = tweet
        self.accountLinkedinPerson = []
        self.accountFacebookPerson = []
        self.accountLinkedinCompany = []
        self.accountFacebookCompany = []
        self.entreprises = []

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
