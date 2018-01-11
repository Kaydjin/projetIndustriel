import re
import sys
try:
    from google import search
except ImportError: 
    print("No module named 'google' found")
 
# to search
prenom = "Frank"
nom = "Candido"
#prenom = sys.argv[0]
#nom = sys.argv[1]
queryFacebook = prenom + nom + " facebook"
#regexFB = re.compile(
queryLinkedIn = prenom + nom + " linkedin"

#query : query string that we want to search for.
#tld : tld stands for top level domain which means we want to search our result on google.com or google.in or some other domain.
#lang : lang stands for language.
#num : Number of results we want.
#start : First result to retrieve.
#stop : Last result to retrieve. Use None to keep searching forever.
#pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant lapse will make your program slow but its safe and better option.
#Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.
#facebook
for i in search(queryFacebook, tld="com", num=10, stop=1, pause=2):
    if re.match(".*facebook\.com/" + re.escape(prenom)+".*" + re.escape(nom) + ".*", i):
        print(i)
#print(\n)
#linkedin
for j in search(queryLinkedIn, tld="com", num=10, stop=1, pause=2):
    if re.match(".*linkedin.*"+ re.escape(prenom) + ".*" + re.escape(nom) + ".*", j):
        print(j)

