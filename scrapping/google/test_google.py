import re
import sys
try:
    from google import search
except ImportError: 
    print("No module named 'google' found")
 
# to search
if len(sys.argv) > 3:
    complementaire = sys.argv[3]
else:
    complementaire = ""
if len(sys.argv) > 2:
    prenom = sys.argv[1]
    nom = sys.argv[2]

query = prenom + nom + complementaire
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

#facebook
print("lien Facebook")
for i in search(queryFacebook, tld="com", num=10, stop=1, pause=2):
    if re.match(".*facebook\.com/" + re.escape(prenom)+ ".*" + re.escape(nom) + ".*", i):
        print(i)
    else:
        if re.match(".*facebook\.com/" + prenom.lower() + ".*" + nom.lower() + ".*", i):
           print(i)
#re.escape marche pas ils ne prends que la syntaxe exacte du string
        
print("\n")

#linkedin
print("lien LinkedIn")
for j in search(queryLinkedIn, tld="com", num=10, stop=1, pause=2):
    if re.match(".*linkedin.*"+ re.escape(prenom) + ".*" + re.escape(nom) + ".*", j):
        print(j)
    else:
        if re.match(".*linkedin.*"+ prenom.lower() + ".*" + nom.lower() + ".*", j):
           print(j)
