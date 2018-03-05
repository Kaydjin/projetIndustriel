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

	def affiche(self):
		print("nom:%s" % self.nom)
		print("url:%s" % self.url)
		print("position:%s" % self.position)
		print("domaineEntreprise:%s" % self.domaineEntreprise)
		print("nomComplet:%s" % self.nomComplet)


