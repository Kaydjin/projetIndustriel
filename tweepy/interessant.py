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


--------------------------------------------------------------------------------------

>>> import nltk
>>> sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good."""
>>> tokens = nltk.word_tokenize(sentence)
>>> tokens
['At', 'eight', "o'clock", 'on', 'Thursday', 'morning',
'Arthur', 'did', "n't", 'feel', 'very', 'good', '.']
>>> tagged = nltk.pos_tag(tokens)
>>> tagged[0:6]
[('At', 'IN'), ('eight', 'CD'), ("o'clock", 'JJ'), ('on', 'IN'),
('Thursday', 'NNP'), ('morning', 'NN')]

Identify named entities:

>>> entities = nltk.chunk.ne_chunk(tagged)
>>> entities
Tree('S', [('At', 'IN'), ('eight', 'CD'), ("o'clock", 'JJ'),
           ('on', 'IN'), ('Thursday', 'NNP'), ('morning', 'NN'),
       Tree('PERSON', [('Arthur', 'NNP')]),
           ('did', 'VBD'), ("n't", 'RB'), ('feel', 'VB'),
           ('very', 'RB'), ('good', 'JJ'), ('.', '.')])

Display a parse tree:

>>> from nltk.corpus import treebank
>>> t = treebank.parsed_sents('wsj_0001.mrg')[0]
>>> t.draw()

-------------
référence trouver un nom via nltk
https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk
-------------


--------------------------------------------------------------------------------------------
In work with nltk, please put this link in ref:
Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
