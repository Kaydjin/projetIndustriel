import csv
import nltk

#CSV ouvrir les 500 pertinents pour analyser les champs de noms

fname = "resultats_pertinent.csv"
file = open(fname, "rt")

#fname3 = "resultats_pertinent.csv"
#file3 = open(fname3, "rt")

try:
    reader = csv.DictReader(file, delimiter=',')
    #reader3 = csv.DictReader(file3, delimiter=',')

    person_furl=0
    person_lurl=0
    person_curl=0
    company_furl=0
    company_lurl=0
    company_curl=0
    listvu = []
    parcours = 0
    nbpersons = 0
    nbpersons2 = 0
    nbcompany = 0
    nbcompany2 = 0
    for row in reader:
        parcours = parcours +1
        idd = row.get('user_id')
        if idd not in listvu:
            if "PERSON" in row.get('type_author'):
                nbpersons2 = nbpersons2 + 1
            if "COMPANY" in row.get('type_author'):
                nbcompany2 = nbcompany2 + 1
            listvu.append(idd)

        if "PERSON" in row.get('type_author'):
            if row.get('url_facebook')!="":
                person_furl = person_furl + 1
            if row.get('url_linkedin')!="":
                person_lurl = person_lurl + 1
            if row.get('company_url')!="":
                person_curl = person_curl + 1
            nbpersons = nbpersons + 1

        if "COMPANY" in row.get('type_author'):
            if row.get('url_facebook')!="":
                company_furl = company_furl + 1
            if row.get('url_linkedin')!="":
                company_lurl = company_lurl + 1
            if row.get('company_url')!="":
                company_curl = company_curl + 1
            nbcompany = nbcompany + 1

    print(str(person_furl) + " resultat person facebook")
    print(str(person_lurl) + " resultat person linkedin")
    print(str(person_curl) + " resultat person compangnie")
    print(str(company_furl) + " resultat compagnie facebook")
    print(str(company_lurl) + " resultat compagnie linkedin")
    print(str(company_curl) + " resultat compagnie url")

    print(str(len(listvu)) + " nombres de resultats d'id user differents")
    print(str(parcours) + " nombres de resultats")

    print(str(nbpersons) + " resultats personnes")
    print(str(nbcompany) + " resultats compagnies")
    print(str(nbpersons2) + " personnes differentes")
    print(str(nbcompany2) + " compagnies differentes")
finally:
    file.close()
