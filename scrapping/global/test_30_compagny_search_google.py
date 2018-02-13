from test_google import search_google
from tweetCsvReader import Reader
from textanalyser import TextAnalyser

fname2 = "test_30_Compagny.log"
file = open(fname2,"w+",encoding = "utf8")
fname = "iteration_500.csv"
reader = Reader(fname)
reader.read()
tweets = reader.getCompagnieTweets(True)
tweets.extend(reader.getCompagnieTweets(False))
tweets = list(set(tweets))
cpt = 30
liste_descriptions = []
for t in tweets:
	if(cpt > 0):
		file.write(t.userName + "\n\n")
		#print(t.userName)
		liste_sites = search_google(t.userName, "", "", True)
		for i,j in liste_sites:
			liste_descriptions.append(j)
			file.write(i + "\n" + j + "\n\n")
			#print(i," ==>\n",j,"\n")
		file.write("----------------\n")
		#cpt -= 1
#print(liste_descriptions)
analyser = TextAnalyser()
resultat2 = analyser.mostCommunsNounsFromTextes(liste_descriptions, 20)
resultat3 = analyser.mostCommunsVerbsFromTextes(liste_descriptions, 20)

for res in resultat2:                
	print(res)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

for res in resultat3:                
	print(res)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


file.close()