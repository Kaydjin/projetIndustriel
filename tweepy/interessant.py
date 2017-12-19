TRAITEMENT NLTK :
import nltk

from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('gutenberg')
words = nltk.corpus.gutenberg.words('carroll-alice.txt') : récupération des mots de base

datas = datas + status.text
liste = [(word, datas.count(word)) for word in words]	: traitement d un texte (datas)

stopwords = nltk.corpus.stopwords.words('english') 
content = [w for w in text if w.lower() not in stopwords] : suppression des stopwords