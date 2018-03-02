#!/usr/bin/env python
# -*- coding: utf-8 -*-


def getKey(item):
	return item[2]

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

	def getValueLinkedinPersonLink(self, link):
		return self.getValue(self.linkLinkedinPerson, link)

	def addFacebookPersonLink(self, x):
		self.linkFacebookPerson.append(x)

	def getValueFacebookPersonLink(self, link):
		return self.getValue(self.linkFacebookPerson, link)

	def addFacebookCompanyLink(self, x):
		self.linkFacebookCompany.append(x)

	def getValueFacebookCompanyLink(self, link):
		return self.getValue(self.linkFacebookCompany, link)

	def addLinkedinCompanyLink(self, x):
		self.linkLinkedinCompany.append(x)

	def getValueLinkedinCompanyLink(self, link):
		return self.getValue(self.linkLinkedinCompany, link)

	def existLinkedinPersonLink(self, link):
		return self.existLink(self.linkLinkedinPerson, link)

	def existFacebookPersonLink(self, link):
		return self.existLink(self.linkFacebookPerson, link)

	def existFacebookCompanyLink(self, link):
		return self.existLink(self.linkFacebookCompany, link)

	def existLinkedinCompanyLink(self, link):
		return self.existLink(self.linkLinkedinCompany, link)

	def getValue(self, list_link, link):
		for val in list_link:
			if val[0]==link:
				return val[1]
		return None

	def existLink(self, list_link, url):
		for val in list_link:
			if val[0]==url:
				return True
		return False

	def getElem(self, list_link, link, pos):
		for val in list_link:
			if val[pos]==link:
				return val
		return None

	def printLinks(self):
		for val in self.linkFacebookPerson:
			print("FPerson:"+val[0])
		for val in self.linkFacebookCompany:
			print("FCompany:"+val[0])
		for val in self.linkLinkedinPerson:
			print("LPerson:"+val[0])
		for val in self.linkLinkedinCompany:
			print("LCompany:"+val[0])

	def addAccountLinkedinPerson(self, x):
		self.accountLinkedinPerson.append(x)

	def getValueAccountFacebookPerson(self, linkF):
		return self.getElem(self.accountFacebookPerson, linkF, 0)

	def addAccountFacebookPerson(self, x):
		self.accountFacebookPerson.append(x)

	def addAccountFacebookCompany(self, x):
		self.accountFacebookCompany.append(x)

	def addAccountLinkedinCompany(self, x):
		self.accountLinkedinCompany.append(x)

	def printAccounts(self):
		"""(link, compte, value)"""
		for link,compte, value in self.accountFacebookPerson:
			print("FPerson:")
			print("[link]"+link+" [star]"+str(value))
		for link,compte in self.accountFacebookCompany:
			print("FCompany:"+link+" " +compte.synthese())
		"""(link, linkF, compte, valueF, valueT)"""
		for link,linkF,compte,valueF,valueT in self.accountLinkedinPerson:
			print("LPerson: ")
			print("[link]"+link+" [linkF]"+linkF+" [starF]"+str(valueF)+" [starT]"+str(valueT))
		for link,compte,value in self.accountLinkedinCompany:
			print("LCompany:"+link+" " +compte.syntheseCompany()+" "+value)

	def getFiveBestAccountsFacebook(self):
		if len(self.accountFacebookPerson)<5:
			return self.accountFacebookPerson

		liste = []
		for link, compte, stars in self.accountFacebookPerson:
			star_start = self.getValueFacebookPersonLink(link)
			liste.append((link, compte,star_start + stars))

		return sorted(liste, reverse=True, key=getKey)[:5]

	def addEntreprise(self, x):
		self.entreprises.append(x)
