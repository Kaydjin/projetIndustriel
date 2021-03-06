import requests, bs4

class CompteFacebook:

    def __init__(self, nom, prenom, url):
        self.homonymes = []
        self.description = ""
        self.url = url
        self.favoris = []
        self.experiences = []
        self.complementaire = ""

    def addFavori(self, x):
        self.favoris.append(x)

    def addExperience(self, x):
        self.experiences.append(x)

    def addHomonyme(self, x):
		self.homonymes.append(x)

""" Retourne l'objet facebook correspondant a la recherche depuis une url donne """
def findFacebook(nom, prenom, url):
	compte = CompteFacebook(nom, prenom, url)

	#request et verification
	res = requests.get(url)
	res.status_code == requests.codes.ok
	if not res.status_code == 200:
		return None

	soup = bs4.BeautifulSoup(res.text)
	sames = soup.select('#pagelet_people_same_name a')

	#'PERSONNES MEME PRENOMS/NOMS:')
	a=0
	if len(sames)>0:
		#on ne prend pas les liens de types public de facebook et on ne prend qu'un lien sur deux (doublons sinon)
		for elem in sames:
			if "/public/" in elem.get('href'):
				break
			if a%2==1:
				compte.addHomonyme(elem.get('href'))
			a=a+1
	#'PROFIL TEXT:')
	descriptioncitation = soup.select('#pagelet_timeline_medley_about ._c24')
	if len(descriptioncitation)>0:
		desc = ""
		for elem in descriptioncitation:
			desc = desc + elem.getText()
		compte.description = desc
	else:
		compte.description = "null"
	#'DONNEES METIERS ET ECOLES:')
	metiersecoles = soup.select('#pagelet_timeline_medley_about .fbEditProfileViewExperience div ._6a a')
	if len(metiersecoles)>0:
		for elem in metiersecoles:
			compte.addExperience(elem.getText())
	#'DONNEES GEOGRAPHIQUES:')
	hometown = soup.select('#pagelet_timeline_medley_about #pagelet_hometown .fbProfileEditExperiences a')
	if len(hometown)>0:
		geodonnees = ""
		for elem in hometown:
			geodonnees = geodonnees + elem.getText()
		compte.complementaire = geodonnees
	else:
		compte.complementaire = "null"
	#'Favoris:')
	favorites = soup.select('#favorites a')
	if len(favorites)>0:
		for elem in favorites:
			compte.addFavori(elem.getText())

	return compte

compte = findFacebook('paul','jean','https://www.facebook.com/people/Jean-Paul/674795292')
print('Homonymes:')
for val in compte.homonymes:
	print(val)

print('Experiences:')
for val in compte.experiences:
	print(val)

print('Favoris:')
for val in compte.favoris:
	print(val)


