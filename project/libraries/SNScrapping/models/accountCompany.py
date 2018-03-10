#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

class AccountCompany:

	def __init__(self,nom, url):
		self.nom=nom
		self.url=url
		self.position = ""
		self.domaine = ""
		self.nomComplet= ""
		self.description = ""

	def toString(self):
		return self.nom + " " + self.url + " " + self.position + " " + self.domaine + " " + self.nomComplet + " " + self.description

	def synthese(self):
		print("nom:%s" % self.nom)
		print("url:%s" % self.url)
		print("position:%s" % self.position)
		print("domaineEntreprise:%s" % self.domaineEntreprise)
		print("nomComplet:%s" % self.nomComplet)

	def toJson(self):
		return ("\t\t[account]{\n\t\t\tnom:"+self.nom +
				"\n\t\t\tposition:"+self.position +
				"\n\t\t\tdomaine:"+self.domaine +
				"\n\t\t\tnomComplet:"+self.nomComplet +
				"\n\t\t\tdescription:"+self.description+"\n\t\t}")


