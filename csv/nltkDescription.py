import csv
import nltk
import string

#from nameparser.parser import HumanName
nltk.download('maxent_ne_chunker')

nltk.download('averaged_perceptron_tagger')

nltk.download('words')
def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return (person_list)

def findtags(tag_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
                                  if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].most_common(20)) for tag in cfd.conditions())

def normalisation(text):
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



fname = "iteration_500.csv"
file = open(fname, "rt")

fname3 = "prenoms.csv"
file3 = open(fname3, "rt")

try:
    reader = csv.DictReader(file, delimiter=',')
    reader3 = csv.DictReader(file3, delimiter=',')
    print "Titres ", reader.fieldnames 

    #200000_tweets_simplifier:
    #tweet_id                   -> 0
    #tweet_created_at           -> 1
    #tweet_text                 -> 2
    #hashtags                   -> 3
    #tweet_quoted_status_id     -> 4
    #tweet_mtion                -> 5
    #pertinents                 -> 6
    #proba_pertinence           -> 7

    #user_id                    -> 8
    #user_screenname            -> 9

    #user_name                  -> 10
    #user_location              -> 11
    #user_description           -> 12
    
    liste = []
    for row in reader3:
        liste.append(row.get('prenom').lower())

    corpus_compagnie = ['news', 'consulting', 'inc', 'investing', 'corp', 'talk', 'energy', 'communications']
    nbr_vrai = 0
    nbrs_noms = 0

    for row in reader:
        if 'VRAI' in row.get('Pertinent'):
            nbr_vrai = nbr_vrai + 1
            continu = True
            for stopword in corpus_compagnie:
                if stopword in row.get('user_name').lower():
                    continu = False
            if continu:
                for val in row.get('user_name').split(' '):
                    if val.lower() in liste:
                        nbrs_noms = nbrs_noms + 1
                        #print row.get('user_name'), row.get('user_description')

                        if not "null" == row.get('user_description'):
                            sentence = row.get('user_description')
                            tokens = nltk.word_tokenize(normalisation(sentence))
                            tagged = nltk.pos_tag(tokens)
                            print(tokens)
                            print(tagged)
                            (tag, word) for (word, tag) in tagged_text
                                  if tag.startswith(tag_prefix)
                            tagdict = findtags('NNP', tagged)
                            for tag in sorted(tagdict):
                                print(tag, tagdict[tag])
                            for name in get_human_names(sentence):
                                print(name)
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print nbr_vrai
    print nbrs_noms
    
finally:
    file.close()
    file3.close()
