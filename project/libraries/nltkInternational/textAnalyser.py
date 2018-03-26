#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import nltk
import string
import re
import sys
from nltk.corpus import stopwords        
from nltk.tag import pos_tag

"""
nltk.download('maxent_ne_chunker')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('gutenberg')
nltk.download('words')"""

def e(myStr):
    if sys.version_info >= (3,0):
       return myStr
    else:
       return myStr.encode('utf8')

class TextAnalyser:

	def __init__(self):
		self.listeStopwords = self.madeStopwords()
		self.corpus = self.madeCorpus()

	""" Retourne les noms communs d'un texte """
	def findtags(self, tag_prefix, tagged_text):
		cfd = []
		for (word, tag) in tagged_text:
			if tag.startswith(tag_prefix):
				cfd.append(word)

		return cfd

	""" A partir d'une base de stopwords en anglais, cree une base avec capitalisation en plus """
	def madeStopwords(self):
		stop = stopwords.words('english')

		#rajout des stopwords avec la premiere lettre capitalize
		liste = []
		liste.extend(stop)
		for w in stop:
			liste.append(w)
			liste.append(w.capitalize())

		stop = stopwords.words('french')
		liste.extend(stop)

		#rajout des stopwords avec la premiere lettre capitalize
		for w in stop:
			liste.append(w)
			liste.append(w.capitalize())

		return set(liste)

	""" Renvoi les noms communs les plus frequents d'une liste de texte """
	def mostCommunsNounsFromTextes(self, liste, nombres):
		liste = self.getNomsCommunsBySentence(liste)
		bigliste = []
		for data in liste:
			bigliste.extend(data)

		frequences = nltk.FreqDist(bigliste)

		return frequences.most_common(nombres)

	""" Renvoi les verbes les plus frequents d'une liste de texte """
	def mostCommunsVerbsFromTextes(self, liste, nombres):
		liste = self.getVerbes(liste)
		bigliste = []
		for data in liste:
			bigliste.extend(data)

		frequences = nltk.FreqDist(bigliste)

		return frequences.most_common(nombres)

		""" Creer un corpus multi-linguale """
	def madeCorpus(self):
		liste = []
		with open("res/frenchwords.txt") as f:
			for line in f:
				if line.strip() != "":
					liste.append(line.strip())

		liste.extend([w for w in nltk.corpus.words.words('en') if w.islower()])
		
		return set(liste)

	""" Analyse et ne renvoit que les noms propres d'un texte ou enonce """
	def getPropersNouns(self, text, doublon=False):
		tagged_sent = pos_tag(text.split())
		propernouns = [word for word,pos in tagged_sent if pos == 'NN']
		propernouns = self.filtrer(propernouns, self.listeStopwords)
		propernouns = self.filtrer(propernouns, self.corpus)

		if doublon==True:
			return propernouns

		return set(propernouns)

	""" Analyse et ne renvoit que les noms propres d'une liste de texte ou enonce"""
	def getPropersNounsFromList(self, liste, doublon=False):
		res = []
		for texte in liste:
			res.extend(self.getPropersNouns(texte.lower()))

		if doublon==True:
			return res

		return set(res)

	""" Separe les mots composes d'elements speciaux d'un texte et supprime la ponctuaction """
	def separeMotCompose(self, text):

		#TODO REMPLACER PAR STRIP
		
		#Remplacement par un espace

		s = text.replace(e(",")," ")
		s = s.replace(e("&")," ")
		s = s.replace(e(".")," ")
		s = s.replace(e("-")," ")
		s = s.replace(e("//")," ")
		s = s.replace(e("/")," ")
		s = s.replace(e("/")," ")
		s = s.replace(e("!")," ")
		s = s.replace(e("?")," ")
		s = s.replace(e("#")," ")
		s = s.replace(e("|")," ")
		s = s.replace(e("@")," ")
		s = s.replace(e("+")," ")
		s = s.replace(e("_")," ")
		s = s.replace(e(":")," ")
		s = s.replace(e(";")," ")

		#Pour tout le reste on supprime simplement la ponctuaction
		if sys.version_info >= (3,0):
			translator = str.maketrans('', '', string.punctuation)
			s = s.translate(translator)
		else:
			for val in string.punctuation:
				s = s.replace(e(val), " ")

		return s


	""" Retourne une liste contenant les elements initiaux donne en arguments, plus chaque
		mot se trouvant dans les mots-composes separe par des lettres en capital """
	def decomposeMotCompose(self, liste):
		res = []
		for word in liste:
			res.append(word)

			#rajout des sous mots contenu dans un mot et separe par une capitalisation
			sublist = re.findall('[A-Z][a-z]*', word)
			if len(sublist)>1:
				for val in sublist:
					if len(val)>2:
						res.append(val)

			#rajout des sous mots(+3 lettres) represente par des capitals (on ne prend pas en compte la derniere capital)
			sublist = re.findall('[A-Z]{4,}', word)
			for val in sublist:
				res.append(val[:-1])

		return res


	""" Retourne une liste de mots de 'liste' n'appartenant pas a la liste 'stop' """
	def filtrer(self, liste, stop):
		res = []

		for w in liste:
			if w not in stop:
				res.append(w)

		return res

	""" Retourne une liste contenant les sets de mots de type tag pour chaque texte donne en parametre """
	def getByTag(self, liste_texte, tag, doublon=False):
		res = []
		for texte in liste_texte:
			tokens = nltk.word_tokenize(self.separeMotCompose(texte))

			#on cree une sous liste contenant que les noms communs
			tagged = nltk.pos_tag(tokens)
			tagdict = self.findtags(tag, tagged)

			#on filtre les stopwords passe au travers des filtres precedents
			textNoms = self.filtrer(tagdict, self.listeStopwords)

			#on ajoute a notre liste les sous mots compris dans les mots composes
			textNoms = self.decomposeMotCompose(textNoms)

			#on met tout en lower case et on vérifie la taille des mots
			inter = []
			for val in textNoms:
				if len(val)>2:
					inter.append(val.lower())
		
			if doublon==False:
				res.append(set(inter))
			else:
				res.append(inter)
				
		return res

	""" Retourne une liste contenant les noms-communs present dans les deux textes donne en parametre """
	def getMatchingNouns(self, texte1, texte2):

		#on ne prend que des listes contenant des noms communs
		liste1 = self.getNomsCommunsBySentence([texte1])[0]
		liste2 = self.getNomsCommunsBySentence([texte2])[0]
		
		return self.getMatchingWords(liste1, liste2)

	""" Retourne une liste contenant les mots present dans les deux listes donne en parametre """
	def getMatchingWords(self, liste1, liste2):
		return [w for w in liste1 if w in liste2]

	def getNomsCommunsBySentence(self, liste_texte, doublon=False):
		if doublon==True:
			return self.getByTag(liste_texte, "NN")

		return self.getByTag(liste_texte, "NN", doublon=doublon)

	def getNomsCommuns(self, texte, doublon=False):
		return list(self.getByTag([texte], "NN", doublon=doublon)[0])

	""" Retourne une liste contenant les sets de noms-communs pour chaque texte donne en parametre """
	def getVerbes(self, liste_texte, doublon=False):
		if doublon==True:
			return self.getByTag(liste_texte, "VB")
		return self.getByTag(liste_texte, "VB", doublon=doublon)