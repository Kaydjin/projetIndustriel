#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Account:
	
	def __init__(self, link, linkF="", account, valueF=0, valueT=0):
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
		return "\t\tlink:"+self.link+"\n\t\tlinkF:"+self.linkF+"\n\t\t[Account]{"+
			self.account.toJson()+"\n\t\t}\n\t\tvalueF:"+self.valueF+"\n\t\tvalueF:"+self.valueT