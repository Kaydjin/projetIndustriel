#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" fonction used to give the parameter to used for a sort """
def getKey(item):
	return item[1]

""" class used to incorporate a class account from the SNS library and add other informations """
class Account:
	
	def __init__(self, link, account, linkF="", valueF=0, valueT=0):
		""" url account """
		self.link = link
		""" url account linked, used for linkedin account """
		self.linkF = linkF
		""" can be a company account or a person account """
		self.account = account
		""" used to specify matching between facebook and linkedin account """
		self.valueF = valueF
		""" used to specify matching between the account and the tweet """
		self.valueT = valueT

	def toString(self):
		return self.link + " " + self.linkF + " " + self.account.synthese() + " " + self.valueF + " " + self.valueT

	def toJson(self):
		return ("\t\tlink:"+self.link+"\n\t\tlinkF:"+self.linkF+"\n\t\t[Account]{"+
			self.account.toJson()+"\n\t\t}\n\t\tvalueF:"+self.valueF+"\n\t\tvalueF:"+self.valueT)

""" class used to add a value to the importance of a link """
class Link:

	"""(link, compte, value)"""
	def __init__(self, link, value=0):
		""" url"""
		self.link = link
		""" value if the search of the link had an influence on the value of it """
		self.value = value

	def synthese(self):
		return "L:"+self.link + "V:"+value

""" class used to instanciate the result of a search for one specified tweet """
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

	""" add links fonctions """

	def addLinkedinPersonLink(self, link, value=0):
		self.linkLinkedinPerson.append(Link(link, value))

	def addFacebookPersonLink(self, link, value=0):
		self.linkFacebookPerson.append(Link(link, value))

	def addFacebookCompanyLink(self, link, value=0):
		self.linkFacebookCompany.append(Link(link, value))

	def addLinkedinCompanyLink(self, link, value=0):
		self.linkLinkedinCompany.append(Link(link, value))

	""" get links fonctions """

	def getValueLinkedinPersonLink(self, link):
		return self.getValue(self.linkLinkedinPerson, link)

	def getValueFacebookPersonLink(self, link):
		return self.getValue(self.linkFacebookPerson, link)

	def getValueFacebookCompanyLink(self, link):
		return self.getValue(self.linkFacebookCompany, link)

	def getValueLinkedinCompanyLink(self, link):
		return self.getValue(self.linkLinkedinCompany, link)

	""" exists links fonctions """

	def existLinkedinPersonLink(self, link):
		return self.existLink(self.linkLinkedinPerson, link)

	def existFacebookPersonLink(self, link):
		return self.existLink(self.linkFacebookPerson, link)

	def existFacebookCompanyLink(self, link):
		return self.existLink(self.linkFacebookCompany, link)

	def existLinkedinCompanyLink(self, link):
		return self.existLink(self.linkLinkedinCompany, link)

	""" class links fonctions """

	def getValue(self, list_link, link):
		for val in list_link:
			if val.link ==link:
				return val.value
		return None
	def existLink(self, list_link, url):
		for val in list_link:
			if val.link==url:
				return True
		return False

	""" add accounts fonctions """

	def addAccountLinkedinPerson(self, link, account, linkF="", valueF=0, valueT=0):
		self.accountLinkedinPerson.append(Account(link, account, linkF, valueF, valueT))

	def addAccountFacebookPerson(self, link, account, linkF="", valueF=0, valueT=0):
		self.accountFacebookPerson.append(Account(link, account, linkF, valueF, valueT))

	def addAccountFacebookCompany(self, link, account, linkF="", valueF=0, valueT=0):
		self.accountFacebookCompany.append(Account(link, account, linkF, valueF, valueT))

	def addAccountLinkedinCompany(self, link, account, linkF="", valueF=0, valueT=0):
		self.accountLinkedinCompany.append(Account(link, account, linkF, valueF, valueT))
	
	""" get accounts fonctions """

	def getValuesAccountFacebookPerson(self, link):
		return self.getValuesAccount(self.accountFacebookPerson, link)

	""" class accounts fonctions """

	# return the two value of an accounts with a matching link given in parameter
	def getValuesAccount(self, list_accounts, link):
		for val in list_accounts:
			if val.link ==link:
				return (val.valueF, val.valueT)
		return None

	""" show fonctions """

	def printLinks(self):
		for val in self.linkFacebookPerson:
			print("FPerson:"+val.link)
		for val in self.linkFacebookCompany:
			print("FCompany:"+val.link)
		for val in self.linkLinkedinPerson:
			print("LPerson:"+val.link)
		for val in self.linkLinkedinCompany:
			print("LCompany:"+val.link)
	def printAccounts(self):

		for val in self.accountFacebookPerson:
			print(val.toString())
		for val in self.accountFacebookCompany:
			print(val.toString())
		for val in self.accountLinkedinPerson:
			print(val.toString())
		for val in self.accountLinkedinCompany:
			print(val.toString())

	""" useful fonctions """

	#keep only the five best facebook account according to the matchings values
	def keepFiveBestAccountsFacebook(self):

		# if there is not more than 5 accounts, no need to sort
		if len(self.accountFacebookPerson)<6:

			liste = []
			#first time we create a tuple account/value
			for val in self.accountFacebookPerson:
				star_start = self.getValueFacebookPersonLink(val.link)
				liste.append((val, star_start + val.valueT))

			#Sort the list by the second argument, in reverse order
			bests = sorted(liste, reverse=True, key=getKey)[:5]

			#second time we keep only five best accounts
			self.accountFacebookPerson = []
			for val in bests:
				self.accountFacebookPerson.append(val[0])