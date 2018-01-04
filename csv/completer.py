import csv
 
#CSV ouvrir les 500 pertinents rajouter les elements manquants

fname = "Iteration_3_tri_500.csv"
file = open(fname, "rt")

fname2 = "iteration_500.csv"
file2 = open(fname2, "wb")

fname3 = "200000_tweets_simplifier.csv"
file3 = open(fname3, "rt")

try:
    reader = csv.DictReader(file, delimiter=';')
    reader2 = csv.DictReader(file3, delimiter=',')
    writer = csv.writer(file2)
    print "Titres ", reader2.fieldnames 
    for row2 in reader2:
        print(row2.get('tweet_id'))
    #iteration_500.csv
    #tweet_id	TweetB	Pertinent(2)	proba_pertinence(3)

    #200000_tweets_simplifier:
    #tweet_id                   -> 0
    #tweet_created_at           -> 1
    #tweet_text                 -> 2
    #hashtags                   -> 3
    #tweet_quoted_status_id     -> 4
    #tweet_mtion                -> 5
    #user_id                    -> 6
    #user_screenname            -> 7
    #user_name                  -> 8
    #user_location              -> 9
    #user_description           -> 10

    writer.writerow((reader2.fieldnames[0], reader2.fieldnames[1], reader2.fieldnames[2], reader2.fieldnames[3],
                     reader2.fieldnames[4], reader2.fieldnames[5], reader.fieldnames[2], reader.fieldnames[3],
                     reader2.fieldnames[6], reader2.fieldnames[7], reader2.fieldnames[8],reader2.fieldnames[9], 
                     reader2.fieldnames[10]))
    
    for row in reader:
        file3.seek(0)
        for row2 in reader2:
            if row2.get('tweet_id')==row.get('tweet_id'):
                writer.writerow( (row2.get('tweet_id'), row2.get('tweet_created_at'), row2.get('tweet_text'), row2.get('hashtags'),
                      row2.get('tweet_quoted_status_id'), row2.get('tweet_mtion'), 
                      row.get('Pertinent'), row.get('proba_pertinence'),
                      row2.get('user_id'), row2.get('user_screenname'),
                      row2.get('user_name'), row2.get('user_location'), row2.get('user_description')))
finally:
    file.close()
    file2.close()
    file3.close()
