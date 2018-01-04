import csv
 
fname = "200000_tweets.csv"
file = open(fname, "rb")

fname2 = "200000_tweets_simplifier.csv"
file2 = open(fname2, "w")

try:
    reader = csv.DictReader(file, delimiter=';')
    writer = csv.writer(file2, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    print "Titres ", reader.fieldnames 
    boolean = True

    #iteration_500.csv
    #tweet_id	TweetB	Pertinent	proba_pertinence

    #200000_tweets:
    #tweet_id(0)    tweet_created_at(1)    user_id(2) user_screenname(3) tweet_text(4)  
    #tweet_coordinates(5)   tweet_coordinates_latitude(6)  tweet_coordinates_longitude(7) tweet_source(8)    tweet_lang(9)  
    #country_code(10)    country(11) place_name(12)  place_fullname(13)  place_bbox(14)  
    #hashtags(15)    place_bbox_polygon(16)  place_bbox_geom(17) place_bbox_geojson(18)  tweet_coordinates_geom(19)  
    #tweet_coordinates_geojson(20)   tweet_favorite_count(21)    tweet_quoted_status_id(22) tweet_retweet_count(23) 
    #tweet_current_user_retweet(24)  user_created_at(25) user_description(26)    user_followers_count(27)    user_friends_count(28)  
    #user_lang(29)   user_location(30)   user_name(31)   user_statuses_count (32)
    #user_time_zone(33)  user_favorites_count(34)    user_geo_enabled(35)    user_listed_counted(36) 
    #user_utc_offset(37) place_type(38)  tweet_mtion(39) id_filtre(40)

    #tweet_id               -> 0
    #tweet_created_at           -> 1
    #tweet_text             -> 4
    #hashtags               -> 15
    #tweet_quoted_status_id         -> 22
    #tweet_mtion                -> 39
    #user_id                -> 2
    #user_screenname            -> 3
    #user_name              -> 31
    #user_location              -> 30
    #user_description           -> 26

    writer.writerow((reader.fieldnames[0], reader.fieldnames[1], reader.fieldnames[4], reader.fieldnames[15],
                     reader.fieldnames[22], reader.fieldnames[39], reader.fieldnames[2], reader.fieldnames[3],
                     reader.fieldnames[31], reader.fieldnames[30], reader.fieldnames[26]))
    while boolean:
        boolean = boolean + 1
    	row = reader.next()
    	if row is None:
    		boolean = False
    	else:
    		writer.writerow( (row.get('tweet_id'), row.get('tweet_created_at'), row.get('tweet_text'), row.get('hashtags'),
                              row.get('tweet_quoted_status_id'), row.get('tweet_mtion'), row.get('user_id'), row.get('user_screenname'),
                              row.get('user_name'), row.get('user_location'), row.get('user_description')))
finally:
    file.close()

