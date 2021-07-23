import requests
import json
import pprint
import pymysql
import time
import warnings
import datetime
import secretkeys


# GET from twitter API ---------------------------------------------------------

# use your own access keys for Twitter API
# the type is: {'Authorization': 'Bearer ...'}
headers = secretkeys.headers

# 1500/15min limit
# calls max 17 times: twitter API statuses/user_timeline
def getAllNewTweetsByScreenName(screen_name, since = None):
    
    # return type: [{}] (list of tweets)

    alltweets = []

    params = (
        ('screen_name', screen_name),
        ('count', '200'),
        ('since_id', since),
        ('tweet_mode', 'extended')
    )

    new_tweets = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json', headers=headers, params=params).json()

    alltweets.extend(new_tweets)

    if 'error' in new_tweets:
        return None

    if len(new_tweets) != 0:
        oldest = int(alltweets[-1]['id_str']) - 1

    
        while len(new_tweets) > 0:
            params2 = (
                ('screen_name', screen_name),
                ('count', '200'),
                ('since_id', since),
                ('max_id', oldest),
                ('tweet_mode', 'extended')
            )
            # print("getting tweets before %s" % oldest)
                
            new_tweets = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json', headers=headers, params=params2).json()

            alltweets.extend(new_tweets)
            
            oldest = int(alltweets[-1]['id_str']) - 1
            
            # print("...%s tweets downloaded so far" % (len(alltweets)))

  
    # print(json.dumps(alltweets, indent=4, sort_keys=True, ensure_ascii=False))

    tweets = []
    for tw in alltweets:
        tweets.append(json.dumps(tw, ensure_ascii=False))

    return tweets

# 75/15min limit
# calls max 11 times: twitter API favorites/list
def getAllNewFavsByScreenName(screen_name, fav_count_diff):
    
    # return type: [{}] (list of tweets)

    if fav_count_diff > 2000:
        fav_count_diff = 2000

    if fav_count_diff == 0:
        return []

    remaining = fav_count_diff

    alltweets = []

    if fav_count_diff < 200:
        params = (
            ('screen_name', screen_name),
            ('count', str(fav_count_diff)),
            ('tweet_mode', 'extended')
        )
        new_tweets = requests.get('https://api.twitter.com/1.1/favorites/list.json', headers=headers, params=params).json()

        if 'error' in new_tweets:
            return None

        alltweets.extend(new_tweets)
    else:
        params = (
            ('screen_name', screen_name),
            ('count', '200'),
            ('tweet_mode', 'extended')
        )

        new_tweets = requests.get('https://api.twitter.com/1.1/favorites/list.json', headers=headers, params=params).json()

        if 'error' in new_tweets:
            return None

        alltweets.extend(new_tweets)

        oldest = int(alltweets[-1]['id_str']) - 1

        remaining -= 200
    
        while remaining > 0:
            if remaining < 200:
                params2 = (
                    ('screen_name', screen_name),
                    ('count', str(remaining)),
                    ('max_id', oldest),
                    ('tweet_mode', 'extended')
                )
            else:
                params2 = (
                    ('screen_name', screen_name),
                    ('count', '200'),
                    ('max_id', oldest),
                    ('tweet_mode', 'extended')
                )
                
            # print("getting tweets before %s" % oldest)
                
            new_tweets = requests.get('https://api.twitter.com/1.1/favorites/list.json', headers=headers, params=params2).json()

            alltweets.extend(new_tweets)
            
            oldest = int(alltweets[-1]['id_str']) - 1
            
            # print("...%s tweets downloaded so far" % (len(alltweets)))

            remaining -= 200

  
    # print(json.dumps(alltweets, indent=4, sort_keys=True, ensure_ascii=False))

    tweets = []
    for tw in alltweets:
        tweets.append(json.dumps(tw, ensure_ascii=False))

    return tweets

# 15/15min limit
# calls max 1 time: twitter API followers/ids
def getAllNewFollowersByScreenName(screen_name):
    
    params = (
        ('screen_name', screen_name),
        ('count', '5000'),
    )
    
    followersIDs = requests.get('https://api.twitter.com/1.1/followers/ids.json', headers=headers, params=params).json()
    
    # print(json.dumps(followersIDs, indent=4, sort_keys=True, ensure_ascii=False))

    try:
        return followersIDs['ids']
    except:
        return None
    

# 15/15min limit
# calls max 1 time: twitter API friends/ids
def getAllNewFriendsByScreenName(screen_name):
    
    params = (
        ('screen_name', screen_name),
        ('count', '5000'),
    )
    
    friendsIDs = requests.get('https://api.twitter.com/1.1/friends/ids.json', headers=headers, params=params).json()
    
    # print(json.dumps(friendsIDs, indent=4, sort_keys=True, ensure_ascii=False))

    try:
        return friendsIDs['ids']
    except:
        return None

# 300/15min limit
# calls max 51 times: twitter API users/lookup
def convertToUserProfiles(ids):

    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
    # pprint.pprint(list(chunks(ids, 100)))
    chunkedIds = list(chunks(ids, 100))

    profiles = []

    for i in range(len(chunkedIds)):

        params = (
            ('user_id', chunkedIds[i]),
            ('tweet_mode', 'extended')
        )
        
        profiles.extend(requests.get('https://api.twitter.com/1.1/users/lookup.json', headers=headers, params=params).json())

    # print(json.dumps(profiles, indent=4, sort_keys=True, ensure_ascii=False))

    pros = []
    for pr in profiles:
        pros.append(json.dumps(pr, ensure_ascii=False))

    # pprint.pprint(pros)

    return pros






# access my twigrapher DB ---------------------------------------------------------


def insertToDB(hostname, uname, dbname, theCharset, table, cols, vals):
    
    # args types:
    #     hostname: str
    #     uname: str
    #     dbname: str
    #     theCharset: str
    #     table: str
    #     cols: [[str]]
    #     vals: [[str]]
    
    # return type: void
    
    conn = pymysql.connect(host=hostname,
                    user=uname,
                    db=dbname,
                    charset=theCharset,
                    cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            with warnings.catch_warnings():
                
                warnings.simplefilter("ignore")
                
                sql = 'SET sql_mode = ""'
                cursor.execute(sql)
                for i in range(len(cols)):
                    if len(cols[i]) == 1:
                        sql = "INSERT IGNORE INTO {} ({}) VALUES ('{}')".format(table, cols[i][0], vals[i][0])
                    elif len(cols[i]) > 1:
                        sql = "INSERT IGNORE INTO {} ({}".format(table, cols[i][0])
                        for j in range(len(cols[i])):
                            if j != 0:
                                sql += ", {}".format(cols[i][j])
                        if not(vals[i][0] is None or type(vals[i][0]) is int or type(vals[i][0]) is float or type(vals[i][j]) is list  or type(vals[i][j]) is dict  or type(vals[i][j]) is tuple):
                        # if type(vals[i][0]) is str:
                            sql += ") VALUES ('{}'".format(pymysql.escape_string(vals[i][0]))
                        else:
                            sql += ") VALUES ('{}'".format(vals[i][0])
                        for j in range(len(cols[i])):
                            if j != 0:
                                if not(vals[i][j] is None or type(vals[i][j]) is int or type(vals[i][j]) is float or type(vals[i][j]) is list or type(vals[i][j]) is dict or type(vals[i][j]) is tuple):
                                # if type(vals[i][j]) is str:
                                    sql += ", '{}'".format(pymysql.escape_string(vals[i][j]))
                                elif type(vals[i][j]) is list or type(vals[i][j]) is dict or type(vals[i][j]) is tuple:
                                    sql += ", 'error'"
                                else:
                                    sql += ", '{}'".format(vals[i][j])                            
                        sql += ")"
                    
                    # pprint.pprint(sql)

                    cursor.execute(sql)

        conn.commit()
    finally:
        conn.close()


def prepareRequestValsArray(cols, request_type, valsarr):
    
    newArr = []
    newCols = []
    for item in valsarr:
        newArr.append([request_type, item])
        newCols.append(cols)

    return [newCols, newArr]







def selectFromDB(hostname, uname, dbname, theCharset, table, cols, where):

    # args types:
    #     hostname: str
    #     uname: str
    #     dbname: str
    #     theCharset: str
    #     table: str
    #     cols: [str]
    #     where: str
    #       eg. "WHERE id REGEXP '.'"

    # return type: [{}]
    
    conn = pymysql.connect(host=hostname,
                    user=uname,
                    db=dbname,
                    charset=theCharset,
                    cursorclass=pymysql.cursors.DictCursor)

    result = None
    try:
        with conn.cursor() as cursor:
            if len(cols) == 1:
                sql = "SELECT {} FROM {} {}".format(cols[0], table, where)
            elif len(cols) > 1:
                sql = "SELECT {}".format(cols[0])
                for i in range(len(cols)):
                    if i != 0:
                        sql += ", {}".format(cols[i])
                sql += " FROM {} {}".format(table, where)
            
            cursor.execute(sql)
            result = cursor.fetchall()
    except:
        1 + 1
    finally:
        conn.close()

    return result


def getLatestTweetID(screen_name):
    
    latest = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'tweets', ['id_str'], "WHERE user_screen_name = '{}' ORDER BY id_str DESC LIMIT 1".format(screen_name))
    
    if type(latest) != tuple:
        obj = latest[0]
        return obj['id_str']
    else:
        return None

# calls 1 time: twitter API users/lookup
def getFavCountDiff(screen_name):

    previous_fav_count = 0

    try:
        previous_fav_count = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', ['fav_count'], "WHERE user_screen_name = '{}'".format(screen_name))[0]['fav_count']
    except:
        1 + 1
        
    params = (
        ('screen_name', screen_name),
    )

    user = requests.get('https://api.twitter.com/1.1/users/lookup.json', headers=headers, params=params).json()
    user_json = user[0] 
    user_str = json.dumps(user_json, ensure_ascii=False)

    addToUsers([user_str], screen_name)

    current_fav_count = user_json.get('favourites_count')

    # print(previous_fav_count)
    # print(current_fav_count)

    update_last_user_fetch_time(screen_name)

    return [current_fav_count - previous_fav_count, current_fav_count, previous_fav_count]


# calls 1 time: twitter API users/lookup.json
def addToFollowings(screen_name, ff_profiles, f_or_f):

    if f_or_f == 'getFriends':
        
        params = (
            ('screen_name', screen_name),
        )
        
        follower = requests.get('https://api.twitter.com/1.1/users/lookup.json', headers=headers, params=params).json()

        cols = []
        vals = []
        for i in range(len(ff_profiles)):
            cols.append(['follower_id', 'follower_screen_name', 'follower_name', 'followee_id', 'followee_screen_name', 'followee_name'])

        for i in range(len(ff_profiles)):
            ff_json = json.loads(ff_profiles[i])
            vals.append([int(follower[0].get('id_str')), screen_name, follower[0].get('name'), int(ff_json.get('id_str')), ff_json.get('screen_name'), ff_json.get('name')])

        insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'followings', cols, vals)
    elif f_or_f == 'getFollowers':
        
        params = (
            ('screen_name', screen_name),
        )
        
        followee = requests.get('https://api.twitter.com/1.1/users/lookup.json', headers=headers, params=params).json()

        cols = []
        vals = []
        for i in range(len(ff_profiles)):
            cols.append(['followee_id', 'followee_screen_name', 'followee_name', 'follower_id', 'follower_screen_name', 'follower_name'])

        for i in range(len(ff_profiles)):
            ff_json = json.loads(ff_profiles[i])
            vals.append([int(followee[0].get('id_str')), screen_name, followee[0].get('name'), int(ff_json.get('id_str')), ff_json.get('screen_name'), ff_json.get('name')])

        insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'followings', cols, vals)

def addToUsers(user, screen_name):

    request = prepareRequestValsArray(['request_type', 'json_col'],'getAllNewFriendsByScreenName', user)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', request[0], request[1])

    profiles = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', ['id', 'json_col', 'extracted'], "WHERE extracted = 0 AND request_type = 'getAllNewFriendsByScreenName'")
    req = formRequestArray(profiles, 'getAllNewFriendsByScreenName', screen_name)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', req[0], req[1])
    updateExtractedFlag('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', [['extracted']], [[1]], "WHERE extracted = 0  AND request_type = 'getAllNewFriendsByScreenName'")


def tweetExtract(tw):
    
    # args type: [{}] (array of full data of tweets returned from AllFromTwitterAPI DB using selectFromDB())
    # return type: [cols[],vals[]] (extracted parts of tweet data)
  
    jsonCol = tw["json_col"]
    jsoned = json.loads(jsonCol)

    cols = [\
        "id_str",\
        "full_text",\
        "created_at",\

        "source",\
        "in_reply_to_status_id_str",\
        "in_reply_to_user_id_str",\
        "in_reply_to_screen_name",\

        "is_quote_status",\
        "quoted_status_id_str",\
        "quoted_status",\

        "favorited",\
        "retweeted",\
        "retweet_count",\
        "favorite_count",\

        "possibly_sensitive",\
        "filter_level",\

        "lang",\




        "user_id_str",\
        "user_name",\
        "user_screen_name",\
        "user_location",\
        "user_url",\
        "user_description",\
        "user_protected",\
        "user_verified",\
        "user_followers_count",\
        "user_friends_count",\
        "user_listed_count",\
        "user_favourites_count",\
        "user_statuses_count",\
        "user_created_at",\
        "user_profile_banner_url",\
        "user_profile_image_url_https",\
        "user_withheld_in_countries",\





        "place_place_type",\
        "place_name",\
        "place_full_name",\
        "place_country_code",\
        "place_country",\
        "place_bounding_box_coordinates_1Long",\
        "place_bounding_box_coordinates_1Lat",\
        "place_bounding_box_coordinates_2Long",\
        "place_bounding_box_coordinates_2Lat",\
        "place_bounding_box_coordinates_3Long",\
        "place_bounding_box_coordinates_3Lat",\
        "place_bounding_box_coordinates_4Long",\
        "place_bounding_box_coordinates_4Lat",\
        "place_bounding_box_type",\

        "coordinates_type",\
        "coordinates_coordinates_Long",\
        "coordinates_coordinates_Lat",\






        "entities_hashtags0_indices_start",\
        "entities_hashtags0_indices_end",\
        "entities_hashtags0_text",\

        "entities_hashtags1_indices_start",\
        "entities_hashtags1_indices_end",\
        "entities_hashtags1_text",\

        "entities_hashtags2_indices_start",\
        "entities_hashtags2_indices_end",\
        "entities_hashtags2_text",\
            
        "entities_hashtags3_indices_start",\
        "entities_hashtags3_indices_end",\
        "entities_hashtags3_text",\

        "entities_hashtags4_indices_start",\
        "entities_hashtags4_indices_end",\
        "entities_hashtags4_text",\

        "entities_hashtags5_indices_start",\
        "entities_hashtags5_indices_end",\
        "entities_hashtags5_text",\

        "entities_hashtags6_indices_start",\
        "entities_hashtags6_indices_end",\
        "entities_hashtags6_text",\
            
        "entities_hashtags7_indices_start",\
        "entities_hashtags7_indices_end",\
        "entities_hashtags7_text",\


        "entities_media0_display_url",\
        "entities_media0_expanded_url",\
        "entities_media0_id_str",\
        "entities_media0_indices_start",\
        "entities_media0_indices_end",\
        "entities_media0_media_url",\
        "entities_media0_media_url_https",\
        "entities_media0_type",\
        "entities_media0_url",\

        "entities_media1_display_url",\
        "entities_media1_expanded_url",\
        "entities_media1_id_str",\
        "entities_media1_indices_start",\
        "entities_media1_indices_end",\
        "entities_media1_media_url",\
        "entities_media1_media_url_https",\
        "entities_media1_type",\
        "entities_media1_url",\

        "entities_media2_display_url",\
        "entities_media2_expanded_url",\
        "entities_media2_id_str",\
        "entities_media2_indices_start",\
        "entities_media2_indices_end",\
        "entities_media2_media_url",\
        "entities_media2_media_url_https",\
        "entities_media2_type",\
        "entities_media2_url",\

        "entities_media3_display_url",\
        "entities_media3_expanded_url",\
        "entities_media3_id_str",\
        "entities_media3_indices_start",\
        "entities_media3_indices_end",\
        "entities_media3_media_url",\
        "entities_media3_media_url_https",\
        "entities_media3_type",\
        "entities_media3_url",\


        "entities_urls0_indices_start",\
        "entities_urls0_indices_end",\
        "entities_urls0_url",\
        "entities_urls0_display_url",\
        "entities_urls0_expanded_url",\

        "entities_urls1_indices_start",\
        "entities_urls1_indices_end",\
        "entities_urls1_url",\
        "entities_urls1_display_url",\
        "entities_urls1_expanded_url",\

        "entities_urls2_indices_start",\
        "entities_urls2_indices_end",\
        "entities_urls2_url",\
        "entities_urls2_display_url",\
        "entities_urls2_expanded_url",\

        "entities_urls3_indices_start",\
        "entities_urls3_indices_end",\
        "entities_urls3_url",\
        "entities_urls3_display_url",\
        "entities_urls3_expanded_url",\



        "entities_user_mentions0_name",\
        "entities_user_mentions0_indices_start",\
        "entities_user_mentions0_indices_end",\
        "entities_user_mentions0_screen_name",\
        "entities_user_mentions0_id_str",\

        "entities_user_mentions1_name",\
        "entities_user_mentions1_indices_start",\
        "entities_user_mentions1_indices_end",\
        "entities_user_mentions1_screen_name",\
        "entities_user_mentions1_id_str",\

        "entities_user_mentions2_name",\
        "entities_user_mentions2_indices_start",\
        "entities_user_mentions2_indices_end",\
        "entities_user_mentions2_screen_name",\
        "entities_user_mentions2_id_str",\
            
        "entities_user_mentions3_name",\
        "entities_user_mentions3_indices_start",\
        "entities_user_mentions3_indices_end",\
        "entities_user_mentions3_screen_name",\
        "entities_user_mentions3_id_str",\

        "entities_user_mentions4_name",\
        "entities_user_mentions4_indices_start",\
        "entities_user_mentions4_indices_end",\
        "entities_user_mentions4_screen_name",\
        "entities_user_mentions4_id_str",\

        "entities_user_mentions5_name",\
        "entities_user_mentions5_indices_start",\
        "entities_user_mentions5_indices_end",\
        "entities_user_mentions5_screen_name",\
        "entities_user_mentions5_id_str",\

        "entities_user_mentions6_name",\
        "entities_user_mentions6_indices_start",\
        "entities_user_mentions6_indices_end",\
        "entities_user_mentions6_screen_name",\
        "entities_user_mentions6_id_str",\
            
        "entities_user_mentions7_name",\
        "entities_user_mentions7_indices_start",\
        "entities_user_mentions7_indices_end",\
        "entities_user_mentions7_screen_name",\
        "entities_user_mentions7_id_str",\


        "entities_symbols_indices_start",\
        "entities_symbols_indices_end",\
        "entities_symbols_text",\

        "entities_polls_option1_text",\
        "entities_polls_option2_text",\
        "entities_polls_option3_text",\
        "entities_polls_option4_text",\
        "entities_polls_end_datetime",\
        "entities_polls_duration_minutes",\

        "extended_entities_media0_media_url_https",\
        "extended_entities_media0_type",\
        "extended_entities_media1_media_url_https",\
        "extended_entities_media1_type",\
        "extended_entities_media2_media_url_https",\
        "extended_entities_media2_type",\
        "extended_entities_media3_media_url_https",\
        "extended_entities_media3_type"\
    ]

    vals = []

    vals.append(int(jsoned['id_str']))
    vals.append(jsoned['full_text'])
    vals.append(convertTime(jsoned['created_at']))

    try:
        vals.append(jsoned['source'])
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned['in_reply_to_status_id_str']))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned['in_reply_to_user_id_str']))
    except:
        vals.append(None)
    try:
        vals.append(jsoned['in_reply_to_screen_name'])
    except:
        vals.append(None)



    try:
        vals.append(convertToTinyInt(jsoned['is_quote_status']))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned['quoted_status_id_str']))
    except:
        vals.append(None)
    try:
        vals.append(json.dumps(jsoned['quoted_status'], ensure_ascii=False))
    except:
        vals.append(None)


    try:
        vals.append(convertToTinyInt(jsoned['favorited']))
    except:
        vals.append(None)
    try:
        vals.append(convertToTinyInt(jsoned['retweeted']))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned['retweet_count']))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned['favorite_count']))
    except:
        vals.append(None)


    try:
        vals.append(convertToTinyInt(jsoned['possibly_sensitive']))
    except:
        vals.append(None)
    try:
        vals.append(jsoned['filter_level'])
    except:
        vals.append(None)
    try:
        vals.append(jsoned['lang'])
    except:
        vals.append(None)






    try:
        vals.append(int(jsoned.get('user').get('id_str')))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('user').get('name'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('user').get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('user').get('location'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('user').get('url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('user').get('description'))
    except:
        vals.append(None)
    try:
        vals.append(convertToTinyInt(jsoned.get('user').get('user_protected')))
    except:
        vals.append(None)
    try:
        vals.append(convertToTinyInt(jsoned.get('user').get('user_verified')))
    except:
        vals.append(None)


    try:
        vals.append(int(jsoned.get('user').get('followers_count')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('user').get('friends_count')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('user').get('listed_count')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('user').get('favourites_count')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('user').get('statuses_count')))
    except:
        vals.append(None)

    try:
        vals.append(convertTime(jsoned.get('user').get('created_at')))
    except:
        vals.append(None)

    try:
        vals.append(jsoned.get('user').get('profile_banner_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('user').get('profile_image_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('user').get('withheld_in_countries'))
    except:
        vals.append(None)





    try:
        vals.append(jsoned.get('place').get('place_type'))
    except:
        vals.append(None)
    try: 
        vals.append(jsoned.get('place').get('name'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('place').get('full_name'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('place').get('country_code'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('place').get('country'))
    except:
        vals.append(None)


    try:
        vals.append(float(jsoned.get('place').get('bounding_box').get('coordinates')[0][0][0]))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('place').get('bounding_box').get('coordinates')[0][0][1]))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('place').get('bounding_box').get('coordinates')[0][1][0]))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('place').get('bounding_box').get('coordinates')[0][1][1]))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('place').get('bounding_box').get('coordinates')[0][2][0]))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('place').get('bounding_box').get('coordinates')[0][2][1]))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('place').get('bounding_box').get('coordinates')[0][3][0]))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('place').get('bounding_box').get('coordinates')[0][3][1]))
    except:
        vals.append(None)

    try:
        vals.append(jsoned.get('place').get('bounding_box').get('type'))
    except:
        vals.append(None)





    try:
        vals.append(jsoned.get('coordinates').get('type'))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('coordinates').get('coordinates')[0]))
    except:
        vals.append(None)
    try:
        vals.append(float(jsoned.get('coordinates').get('coordinates')[1]))
    except:
        vals.append(None)





    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[0].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[0].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('hashtags')[0].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[1].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[1].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('hashtags')[1].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[2].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[2].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('hashtags')[2].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[3].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[3].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('hashtags')[3].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[4].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[4].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('hashtags')[4].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[5].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[5].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('hashtags')[5].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[6].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[6].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('hashtags')[6].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[7].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('hashtags')[7].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('hashtags')[7].get('text'))
    except:
        vals.append(None)



    try:
        vals.append(jsoned.get('entities').get('media')[0].get('display_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[0].get('expanded_url'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[0].get('id_str')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[0].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[0].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[0].get('media_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[0].get('media_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[0].get('type'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[0].get('url'))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('media')[1].get('display_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[1].get('expanded_url'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[1].get('id_str')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[1].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[1].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[1].get('media_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[1].get('media_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[1].get('type'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[1].get('url'))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('media')[2].get('display_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[2].get('expanded_url'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[2].get('id_str')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[2].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[2].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[2].get('media_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[2].get('media_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[2].get('type'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[2].get('url'))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('media')[3].get('display_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[3].get('expanded_url'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[3].get('id_str')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[3].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('media')[3].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[3].get('media_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[3].get('media_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[3].get('type'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('media')[3].get('url'))
    except:
        vals.append(None)




    try:
        vals.append(int(jsoned.get('entities').get('urls')[0].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('urls')[0].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[0].get('url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[0].get('display_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[0].get('expanded_url'))
    except:
        vals.append(None)


    try:
        vals.append(int(jsoned.get('entities').get('urls')[1].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('urls')[1].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[1].get('url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[1].get('display_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[1].get('expanded_url'))
    except:
        vals.append(None)


    try:
        vals.append(int(jsoned.get('entities').get('urls')[2].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('urls')[2].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[2].get('url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[2].get('display_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[2].get('expanded_url'))
    except:
        vals.append(None)


    try:
        vals.append(int(jsoned.get('entities').get('urls')[3].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('urls')[3].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[3].get('url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[3].get('display_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('urls')[3].get('expanded_url'))
    except:
        vals.append(None)





    try:
        vals.append(jsoned.get('entities').get('user_mentions')[0].get('name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[0].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[0].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('user_mentions')[0].get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[0].get('id_str')))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('user_mentions')[1].get('name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[1].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[1].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('user_mentions')[1].get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[1].get('id_str')))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('user_mentions')[2].get('name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[2].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[2].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('user_mentions')[2].get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[2].get('id_str')))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('user_mentions')[3].get('name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[3].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[3].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('user_mentions')[3].get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[3].get('id_str')))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('user_mentions')[4].get('name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[4].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[4].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('user_mentions')[4].get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[4].get('id_str')))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('user_mentions')[5].get('name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[5].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[5].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('user_mentions')[5].get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[5].get('id_str')))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('user_mentions')[6].get('name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[6].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[6].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('user_mentions')[6].get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[6].get('id_str')))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('entities').get('user_mentions')[7].get('name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[7].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[7].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('user_mentions')[7].get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('user_mentions')[7].get('id_str')))
    except:
        vals.append(None)





    try:
        vals.append(int(jsoned.get('entities').get('symbols')[0].get('indices')[0]))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('symbols')[0].get('indices')[1]))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('symbols')[0].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(jsoned.get('entities').get('polls')[0].get('options')[0].get('text'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('polls')[0].get('options')[1].get('text'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('polls')[0].get('options')[2].get('text'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('entities').get('polls')[0].get('options')[3].get('text'))
    except:
        vals.append(None)

    try:
        vals.append(convertTime(jsoned.get('entities').get('polls')[0].get('end_datetime')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('entities').get('polls')[0].get('duration_minutes')))
    except:
        vals.append(None)


    try:
        vals.append(jsoned.get('extended_entities').get('media')[0].get('media_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('extended_entities').get('media')[0].get('type'))
    except:
        vals.append(None)

    try:
        vals.append(jsoned.get('extended_entities').get('media')[1].get('media_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('extended_entities').get('media')[1].get('type'))
    except:
        vals.append(None)

    try:
        vals.append(jsoned.get('extended_entities').get('media')[2].get('media_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('extended_entities').get('media')[2].get('type'))
    except:
        vals.append(None)

    try:
        vals.append(jsoned.get('extended_entities').get('media')[3].get('media_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('extended_entities').get('media')[3].get('type'))
    except:
        vals.append(None)


    return [cols, vals]

def userExtract(user):
    
    # args type: [{}] (array of full data of tweets returned from AllFromTwitterAPI DB using selectFromDB())
    # return type: [cols[],vals[]] (extracted parts of tweet data)
  
    jsonCol = user["json_col"]
    jsoned = json.loads(jsonCol)

    cols = [\
        "user_id_str",\
        "user_name",\
        "user_screen_name",\
        "user_location",\
        "user_url",\
        "user_description",\
        "user_protected",\
        "user_verified",\
        "user_followers_count",\
        "user_friends_count",\
        "user_listed_count",\
        "user_favourites_count",\
        "user_statuses_count",\
        "user_created_at",\
        "user_profile_banner_url",\
        "user_profile_image_url_https",\
        "user_withheld_in_countries",\
    ]

    vals = []

    try:
        vals.append(int(jsoned.get('id_str')))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('name'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('screen_name'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('location'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('description'))
    except:
        vals.append(None)
    try:
        vals.append(convertToTinyInt(jsoned.get('user_protected')))
    except:
        vals.append(None)
    try:
        vals.append(convertToTinyInt(jsoned.get('user_verified')))
    except:
        vals.append(None)


    try:
        vals.append(int(jsoned.get('followers_count')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('friends_count')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('listed_count')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('favourites_count')))
    except:
        vals.append(None)
    try:
        vals.append(int(jsoned.get('statuses_count')))
    except:
        vals.append(None)

    try:
        vals.append(convertTime(jsoned.get('created_at')))
    except:
        vals.append(None)

    try:
        vals.append(jsoned.get('profile_banner_url'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('profile_image_url_https'))
    except:
        vals.append(None)
    try:
        vals.append(jsoned.get('withheld_in_countries'))
    except:
        vals.append(None)
    

    return [cols, vals]


def convertTime(twTime):
    
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(twTime,'%a %b %d %H:%M:%S +0000 %Y'))
    return ts

def convertToTinyInt(boolval):
    
    if boolval == 'true':
        return 1
    else:
        return 0

def formRequestArray(tws, req, fav_by_screen_name = None):
    
    if req == 'getAllNewTweetsByScreenName':
        
        cols = []
        vals = []
        for i in range(len(tws)):
            extracted = tweetExtract(tws[i])
            cols.append(extracted[0])
            vals.append(extracted[1])
                
        # pprint.pprint(vals)

        return [cols, vals]
    elif req == 'getAllNewFriendsByScreenName' or req == 'getAllNewFollowersByScreenName':

        cols = []
        vals = []
        for i in range(len(tws)):
            extracted = userExtract(tws[i])
            cols.append(extracted[0])
            vals.append(extracted[1])
        
        return [cols, vals]
    elif req == 'getAllNewFavsByScreenName':
        
        cols = []
        vals = []

        for i in range(len(tws)):
            extracted = tweetExtract(tws[i])

            extracted[0].append('fav_by_screen_name')
            extracted[1].append("{}".format(fav_by_screen_name))
            cols.append(extracted[0])
            vals.append(extracted[1])
        
        # pprint.pprint(vals)

        return [cols, vals]



def tweetExtractTweetID(tw):
    
    # args type: {} (full data of tweet)
    # return type: str (tweet ID)
  
    tw0 = tw[0]
    jsonCol = tw0['json_col']
    jsoned = json.loads(jsonCol)

    id = jsoned['id_str']
   
    # print(id)

    return id

def updateDB(hostname, uname, dbname, theCharset, table, cols, vals, where):
   
    # args types:
    #     hostname: str
    #     uname: str
    #     dbname: str
    #     theCharset: str
    #     table: str
    #     cols: [[str]]
    #     vals: [[str]]
    #     where: str
    #       eg. "WHERE id REGEXP '.'"
    
    # return type: void
    
    conn = pymysql.connect(host=hostname,
                    user=uname,
                    db=dbname,
                    charset=theCharset,
                    cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            with warnings.catch_warnings():
                
                warnings.simplefilter("ignore")
                
                sql = 'SET sql_mode = ""'
                cursor.execute(sql)
                for i in range(len(cols)):
                    if len(cols[i]) == 1:
                        sql = "UPDATE IGNORE {} SET {} = {} {}".format(table, cols[i][0], vals[i][0], where)
                    elif len(cols[i]) > 1:
                        sql = "UPDATE IGNORE {} SET {} = {}".format(table, cols[i][0], vals[i][0])
                        for j in range(len(cols[i])):
                            if j != 0:
                                sql += ", {} = {}".format(cols[i][j], vals[i][j])
                        sql += " {}".format(where)
                    
                    # pprint.pprint(sql)

                    cursor.execute(sql)

        conn.commit()
    finally:
        conn.close()

def updateExtractedFlag(hostname, uname, dbname, theCharset, table, cols, vals, where):

        updateDB(hostname, uname, dbname, theCharset, table, cols, vals, where)

# also does update_last_fav_fetch_time
def updateFavCount(screen_name):

    current_fav_count = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', ['user_favourites_count'], "WHERE user_screen_name = '{}'".format(screen_name))

    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(str(datetime.datetime.now()),'%Y-%m-%d %H:%M:%S.%f'))

    updateDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', [['fav_count', 'last_fav_fetch_time']], [[current_fav_count[0]['user_favourites_count'], "'{}'".format(current_time)]], "WHERE user_screen_name = '{}'".format(screen_name))

# calls 1 time: twitter API users/lookup.json
# also makes sure the user is in the user list
def update_last_tweet_fetch_time(screen_name):

    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(str(datetime.datetime.now()),'%Y-%m-%d %H:%M:%S.%f'))

    last_tweet_fetch_time = current_time

    try:
        last_tweet_fetch_time = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', ['last_tweet_fetch_time'], "WHERE user_screen_name = '{}'".format(screen_name))[0]['last_tweet_fetch_time']
    except:
        1 + 1
        
    if last_tweet_fetch_time == current_time:

        params = (
            ('screen_name', screen_name),
        )

        user = requests.get('https://api.twitter.com/1.1/users/lookup.json', headers=headers, params=params).json()
        user_json = user[0] 
        user_str = json.dumps(user_json, ensure_ascii=False)

        addToUsers([user_str], screen_name)

    
    updateDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', [['last_tweet_fetch_time']], [["'{}'".format(current_time)]], "WHERE user_screen_name = '{}'".format(screen_name))

    update_last_user_fetch_time(screen_name)

def update_last_user_fetch_time(screen_name):

    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(str(datetime.datetime.now()),'%Y-%m-%d %H:%M:%S.%f'))
    
    updateDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', [['last_user_fetch_time']], [["'{}'".format(current_time)]], "WHERE user_screen_name = '{}'".format(screen_name))

# calls 1 time: twitter API users/lookup.json
# also makes sure the user is in the user list, and update_last_user_fetch_time.
def update_last_followers_fetch_time(screen_name):

    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(str(datetime.datetime.now()),'%Y-%m-%d %H:%M:%S.%f'))

    last_followers_fetch_time = current_time

    try:
        last_followers_fetch_time = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', ['last_followers_fetch_time'], "WHERE user_screen_name = '{}'".format(screen_name))[0]['last_followers_fetch_time']
    except:
        1 + 1
        
    if last_followers_fetch_time == current_time:

        params = (
            ('screen_name', screen_name),
        )

        user = requests.get('https://api.twitter.com/1.1/users/lookup.json', headers=headers, params=params).json()
        user_json = user[0] 
        user_str = json.dumps(user_json, ensure_ascii=False)

        addToUsers([user_str], screen_name)

    
    updateDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', [['last_followers_fetch_time']], [["'{}'".format(current_time)]], "WHERE user_screen_name = '{}'".format(screen_name))
    update_last_user_fetch_time(screen_name)

# calls 1 time: twitter API users/lookup.json
# also makes sure the user is in the user list
def update_last_friends_fetch_time(screen_name):

    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(str(datetime.datetime.now()),'%Y-%m-%d %H:%M:%S.%f'))

    last_friends_fetch_time = current_time

    try:
        last_friends_fetch_time = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', ['last_friends_fetch_time'], "WHERE user_screen_name = '{}'".format(screen_name))[0]['last_friends_fetch_time']
    except:
        1 + 1
        
    if last_friends_fetch_time == current_time:

        params = (
            ('screen_name', screen_name),
        )

        user = requests.get('https://api.twitter.com/1.1/users/lookup.json', headers=headers, params=params).json()
        user_json = user[0] 
        user_str = json.dumps(user_json, ensure_ascii=False)

        addToUsers([user_str], screen_name)

    
    updateDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', [['last_friends_fetch_time']], [["'{}'".format(current_time)]], "WHERE user_screen_name = '{}'".format(screen_name))
    update_last_user_fetch_time(screen_name)


# tester fn
def typeOfArray(req):
    
    cols = req[0]
    vals = req[1]

    # colstype = list(map(lambda i: list(map(lambda j: type(j), i)), cols))
    valstype = list(map(lambda i: list(map(lambda j: type(j), i)), vals))

    # for i in range(len(cols)):
    #     for j in range(len(cols[i])):
    #         colstype[i][j] = type(cols[i][j])
    # for i in range(len(vals)):
    #     for j in range(len(vals[i])):
    #         valstype[i][j] = type(vals[i][j])

    result = []
    for i in range(len(cols)):
        # result.append(colstype[i])
        result.append(cols[i])
        result.append(valstype[i])

    pprint.pprint(result)



# tester -----------------------------------------------------

# ツイート版 done
# twitter API statuses/user_timeline: 1500/15min limit: calls max 17 times
# twitter API users/lookup: 300/15min limit: calls 1 time
def getTweets(screen_name):
    
    # screen name と そのscreen nameによる AllFromTwitterAPI 内の最も新しいツイートID を指定して、新しいツイートをTwitter API から取得、AllFromTwitterAPIに追加
    tws = getAllNewTweetsByScreenName(screen_name, getLatestTweetID(screen_name))
    if tws is None:
        print('Not authorized.')
        return
    request = prepareRequestValsArray(['request_type', 'json_col'],'getAllNewTweetsByScreenName', tws)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', request[0], request[1])
    update_last_tweet_fetch_time(screen_name)

    # AllFromTwitterAPI から 取ってきたtweetsを tweetExtractして tweetsに格納
    tws = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', ['id', 'json_col', 'extracted'], "WHERE extracted = 0 AND request_type = 'getAllNewTweetsByScreenName'")
    req = formRequestArray(tws, 'getAllNewTweetsByScreenName')
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'tweets', req[0], req[1])
    updateExtractedFlag('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', [['extracted']], [[1]], "WHERE extracted = 0 AND request_type = 'getAllNewTweetsByScreenName'")

# --------------
# fav版 done
# twitter API favorites/list: 75/15min limit: calls max 11 times
# twitter API users/lookup: 300/15min limit: calls 1 time
def getFavs(screen_name):

    fav_count_diff = getFavCountDiff(screen_name)
    favs = getAllNewFavsByScreenName(screen_name, fav_count_diff[0])
    if favs is None:
        print('Not authorized.')
        return
    request = prepareRequestValsArray(['request_type', 'json_col'],'getAllNewFavsByScreenName', favs)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', request[0], request[1])
    updateFavCount(screen_name)

    favs = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', ['id', 'json_col', 'extracted'], "WHERE extracted = 0 AND request_type = 'getAllNewFavsByScreenName'")
    req = formRequestArray(favs, 'getAllNewFavsByScreenName', screen_name)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'favs', req[0], req[1])
    updateExtractedFlag('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', [['extracted']], [[1]], "WHERE extracted = 0  AND request_type = 'getAllNewFavsByScreenName'")

# --------------
# user版 done
# twitter API friends/ids: 15/15min limit: calls max 1 time
# twitter API users/lookup: 300/15min limit: calls max 52 times
def getFriends(screen_name):

    user_ids = getAllNewFriendsByScreenName(screen_name)

    if user_ids is None:
        print('Not authorized.')
        return
    profiles = convertToUserProfiles(user_ids)

    addToFollowings(screen_name, profiles, 'getFriends')
    request = prepareRequestValsArray(['request_type', 'json_col'],'getAllNewFriendsByScreenName', profiles)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', request[0], request[1])

    profiles = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', ['id', 'json_col', 'extracted'], "WHERE extracted = 0 AND request_type = 'getAllNewFriendsByScreenName'")
    req = formRequestArray(profiles, 'getAllNewFriendsByScreenName', screen_name)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', req[0], req[1])
    for user in profiles:
        jsonCol = user["json_col"]
        jsoned = json.loads(jsonCol)
        update_last_user_fetch_time(jsoned['screen_name'])
    updateExtractedFlag('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', [['extracted']], [[1]], "WHERE extracted = 0  AND request_type = 'getAllNewFriendsByScreenName'")
    update_last_friends_fetch_time(screen_name)

# twitter API followers/ids: 15/15min limit: calls max 1 time
# twitter API users/lookup: 300/15min limit: calls max 52 times
def getFollowers(screen_name):

    user_ids = getAllNewFollowersByScreenName(screen_name)
    if user_ids is None:
        print('Not authorized.')
        return
    profiles = convertToUserProfiles(user_ids)
    addToFollowings(screen_name, profiles, 'getFollowers')
    request = prepareRequestValsArray(['request_type', 'json_col'],'getAllNewFollowersByScreenName', profiles)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', request[0], request[1])

    profiles = selectFromDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', ['id', 'json_col', 'extracted'], "WHERE extracted = 0 AND request_type = 'getAllNewFollowersByScreenName'")
    req = formRequestArray(profiles, 'getAllNewFollowersByScreenName', screen_name)
    insertToDB('localhost', 'kai', 'twigrapher', 'utf8mb4', 'users', req[0], req[1])
    for user in profiles:
        jsonCol = user["json_col"]
        jsoned = json.loads(jsonCol)
        update_last_user_fetch_time(jsoned['screen_name'])
    updateExtractedFlag('localhost', 'kai', 'twigrapher', 'utf8mb4', 'AllFromTwitterAPI', [['extracted']], [[1]], "WHERE extracted = 0  AND request_type = 'getAllNewFollowersByScreenName'")
    update_last_followers_fetch_time(screen_name)

# main -------------

getTweets('chromascore')
# getFavs('chromascore')
# getFriends('chromascore')
# getFollowers('chromascore')
