import requests, bs4



class CompteFacebook:

    def __init__(self, nom, prenom, url):
    	self
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

	res = requests.get(url)

	res.status_code == requests.codes.ok
	if not res.status_code == 200:
		return None

	soup = bs4.BeautifulSoup(res.text)
	sames = soup.select('#pagelet_people_same_name a')

	a=0
	if len(sames)>0:
		print('PERSONNES MEME PRENOMS/NOMS:')
		for elem in sames:
			if "/public/" in elem.get('href'):
				break
			if a%2==1:
				print(elem.getText()+"	:	"+elem.get('href'))
				compte.addHomonyme(elem.get('href'))
			a=a+1
	else:
		print('Pas de personnes de meme prenoms et noms')

	print("")

	descriptioncitation = soup.select('#pagelet_timeline_medley_about ._c24')

	if len(descriptioncitation)>0:
		print('PROFIL TEXT:')
		desc = ""
		for elem in descriptioncitation:
			desc = desc + elem.getText()
			print(elem.getText())
		
		compte.description = desc
	else:
		print('Pas de description ou citation')

	print("")

	metiersecoles = soup.select('#pagelet_timeline_medley_about .fbEditProfileViewExperience div ._6a a')

	if len(metiersecoles)>0:
		print('DONNEES METIERS ET ECOLES:')
		for elem in metiersecoles:
			print(elem.getText()+"	:	"+elem.get('href'))
			compte.addExperience(elem.getText())
	else:
		print('Pas de donnees scolaires ou metiers')

	print("")

	hometown = soup.select('#pagelet_timeline_medley_about #pagelet_hometown .fbProfileEditExperiences a')
	if len(hometown)>0:
		print('DONNEES GEOGRAPHIQUES:')
		geodonnees = ""
		for elem in hometown:
			geodonnees = geodonnees + elem.getText()
			print(elem.getText()+"	:	"+elem.get('href'))
		compte.complementaire = geodonnees
	else:
		print('Pas de donnees geographiques')

	print("")
	favorites = soup.select('#favorites a')
	if len(favorites)>0:
		print('Favoris:')
		for elem in favorites:
			print(elem.getText()+"	:	"+elem.get('href'))
			compte.addFavori(elem.getText())
	else:
		print('Pas de favoris')
