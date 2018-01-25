import requests, bs4

res = requests.get('https://www.facebook.com/frank.candido.5')
#
#try:
#    res.raise_for_status()
#except Exception as exc:
#    print('There was a problem: %s' % (exc))

res.status_code == requests.codes.ok
if res.status_code == 200:
	print("CONNECTION OK")
	print("")
else:
	print("CONNECTION FAIL")

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
		a=a+1
else:
	print('Pas de personnes de meme prenoms et noms')

print("")

descriptioncitation = soup.select('#pagelet_timeline_medley_about ._c24')

if len(descriptioncitation)>0:
	print('PROFIL TEXT:')
	for elem in descriptioncitation:
		print(elem.getText())
else:
	print('Pas de description ou citation')

print("")

metiersecoles = soup.select('#pagelet_timeline_medley_about .fbEditProfileViewExperience div ._6a a')

if len(metiersecoles)>0:
	print('DONNEES METIERS ET ECOLES:')
	for elem in metiersecoles:
		print(elem.getText()+"	:	"+elem.get('href'))
else:
	print('Pas de donnees scolaires ou metiers')

print("")

hometown = soup.select('#pagelet_timeline_medley_about #pagelet_hometown .fbProfileEditExperiences a')
if len(hometown)>0:
	print('DONNEES GEOGRAPHIQUES:')
	for elem in hometown:
		print(elem.getText()+"	:	"+elem.get('href'))
else:
	print('Pas de donnees geographiques')

print("")
favorites = soup.select('#favorites a')
if len(favorites)>0:
	print('Favoris:')
	for elem in favorites:
		print(elem.getText()+"	:	"+elem.get('href'))
else:
	print('Pas de favoris')
