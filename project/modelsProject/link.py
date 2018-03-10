#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Link:

	"""(link, compte, value)"""
	def __init__(self, link, value=0):
		""" url"""
		self.link = link
		""" value if the search of the link had an influence on the value of it """
		self.value = value

	def synthese(self):
		return "L:"+self.link + "V:"+value