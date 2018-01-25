import re
import sys
try:
    from google import search
except ImportError: 
    print("No module named 'google' found")

def search_google(nom_complet, complementaire):
    # séparation du nom_complet en nom et prénom, utile pour les regex
    prenom = ""
    nom = ""
    fin_prenom = False
    for c in nom_complet:
        if(not fin_prenom):
            if(c == " "):
                fin_prenom = True
            else:
                prenom += c
        else:
            nom += c

    #construction des strings servant aux requetes sur le moteur de recherche google
    query = prenom + " " + nom + " " + complementaire
    queryFacebook = query + " facebook"
    queryLinkedIn = query + " linkedin"

#query : query string that we want to search for.
#tld : tld stands for top level domain which means we want to search our result on google.com or google.in or some other domain.
#lang : lang stands for language.
#num : Number of results we want.
#start : First result to retrieve.
#stop : Last result to retrieve. Use None to keep searching forever.
#pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant lapse will make your program slow but its safe and better option.
#Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.
    result = []
    #supprimer les accents sert a généraliser la recherche
    prenom = supprime_accent(prenom)
    nom = supprime_accent(nom)
    #execution d'une requete, le resultat est recupere dans "i"
    for i in search(queryFacebook, tld="com", num=10, stop=1, pause=2):
        #ne recupere que le premier resultat
        if (len(result) < 1):
            #supprimer les accents sert a généraliser la recherche
            i_sans_accent = supprime_accent(i)
            if re.match(".*FACEBOOK\.COM/" + prenom.upper() + ".*" + nom.upper() + ".*", i_sans_accent.upper()):
                result.append(i)

    for j in search(queryLinkedIn, tld="com", num=10, stop=1, pause=2):
        if (len(result) < 2):
            j_sans_accent = supprime_accent(j)
            if re.match(".*LINKEDIN.*"+ prenom.upper() + ".*" + nom.upper() + ".*", j_sans_accent.upper()):
                result.append(j)
                
    return result

def supprime_accent(ligne):
        """ supprime les accents du texte source """
        accents = { 'a': ['à', 'ã', 'á', 'â'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û'],
                    'o': ['ô', 'ö'] }
        for (char, accented_chars) in accents.items():
            for accented_char in accented_chars:
                ligne = ligne.replace(accented_char, char)
        return ligne


liste_sites = search_google("Frank Candido", "")
print(liste_sites)
