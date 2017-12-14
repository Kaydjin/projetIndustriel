import csv
 
#CSV ouvrir les 500 pertinents rajouter les elements manquants

fname = "100_premiers_tweets.csv"
file = open(fname, "rb")
 
fname2 = "out.csv"
file2 = open(fname2, "wb")
try:
    reader = csv.DictReader(file)
    writer = csv.writer(file2)
    print "Titres ", reader.fieldnames 
    boolean = True
    writer.writerow((reader.fieldnames[0], reader.fieldnames[1]))
    while boolean:
    	row = reader.next()
    	if row is None:
    		boolean = False
    	else:
    		writer.writerow( (row.get('tweet_id'), row.get('tweet_created_at')))
finally:
    file.close()