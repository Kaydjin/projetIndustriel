import csv
import nltk
import string
import re
from nltk.corpus import stopwords

nltk.download('maxent_ne_chunker')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('words')

class TextAnalyser:

    def __init__(self):
        self.listeStopwords = self.madeStopwords()

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
        for w in stop:
            liste.append(w)
            liste.append(w.capitalize())

        return liste


    """ Separe les mots composes d'elements speciaux d'un texte et supprime la ponctuaction """
    def separeMotCompose(self, text):
        s = text.replace(",","")
        s = s.replace("&"," ")
        s = s.replace("."," ")
        s = s.replace("-"," ")
        s = s.replace("//"," ")
        s = s.replace("/"," ")
        s = s.replace("!"," ")
        s = s.replace("?"," ")
        s = s.replace("#"," ")
        s = s.replace("|"," ")
        s = s.replace("@"," ")
        s = s.translate(None, string.punctuation)
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

    """ Retourne une liste contenant les sets de noms communs pour chaque texte donne en parametre """
    def getNomsCommuns(self, liste_texte):
        res = []
        for texte in liste_texte:
            tokens = nltk.word_tokenize(self.separeMotCompose(texte))

            #on cree une sous liste contenant que les noms communs
            tagged = nltk.pos_tag(tokens)
            tagdict = self.findtags('NN', tagged)

            #on filtre les stopwords passe au travers des filtres precedents
            textNoms = self.filtrer(tagdict, self.listeStopwords)

            #on ajoute a notre liste les sous mots compris dans les mots composes
            textNoms = self.decomposeMotCompose(textNoms)
            res.append(textNoms)
        return res           


#instanciation de fichier csv
fname = "iteration_500.csv"
file = open(fname, "rt")

fname3 = "prenoms.csv"
file3 = open(fname3, "rt")

try:
    #connection aux fichiers csv.
    reader = csv.DictReader(file, delimiter=',')
    reader3 = csv.DictReader(file3, delimiter=',')

    #on transforme les prenoms en une liste sans capital
    liste = []
    for row in reader3:
        liste.append(row.get('prenom').lower())

    #on cree une liste de mots souvent present dans une compagnie
    corpus_compagnie = ['news', 'consulting', 'inc', 'investing', 'corp', 'talk', 'energy', 'communications']

    #instanciation de la liste des descriptions a analyser
    descriptions = []

    #pour tous les elements trouves dans le csv
    for row in reader:

        #si l'element est pertinent
        if 'VRAI' in row.get('Pertinent'):

            #on ne continue pas si l'element est une compagnie ou une organisation
            continu = True
            for companyWord in corpus_compagnie:
                if companyWord in row.get('user_name').lower():
                    continu = False

            #on continue sinon
            if continu:

                # on separe tous les elements composant le champ nom
                for val in row.get('user_name').split(' '):

                    # si l'element est un prenom et donc une personne on continu
                    if val.lower() in liste:

                        # si la description est nulle, on ne peut pas continuer
                        if not "null" == row.get('user_description'):
                            descriptions.append(row.get('user_description'))

    #analyse des descriptions
    analyser = TextAnalyser()
    resultat = analyser.getNomsCommuns(descriptions)

    for res in resultat:
        for val in res:
            print(val)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
finally:
    file.close()
    file3.close()
