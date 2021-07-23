# Twigrapher Downloader

## Getting Started
```
git clone https://github.com/chromascore/twigrapher_datafetcher.git
cd src
// run createTable.sql. I do so with copying and pasting the content of the file into MySQLWorkbench.
/* modify the bottom of twiAPI_to_myDB_uauth.py (un-comment out getTweets('chromascore') and put your the screenname of the Twitter account whose Tweets you want to download instead of 'chromascore', which is my struggling-with-playing-the-piano-and-studying-whatever-arts-and-daily-shitposts account */
/* alter the username from 'kai' (mine) to your own in twiAPI_to_myDB...py. There are a lot of instances. I'm sorry I will update it soon for a public release */
touch secretkeys.py
/* open secretkey.py and write and add values to below:

  headers = {
    'Authorization': 'Bearer //get the bearer token from Twitter Dev account and put it here'
  }

  CONSUMER_KEY = '//get the consumer key from Twitter Dev account and put it here'
  CONSUMER_SECRET = '//get the consumer secret key from Twitter Dev account and put it here'

  ACCESS_TOKEN = '//get the access token of your Twitter account by using my twigrapher-react2 and put it here'
  ACCESS_TOKEN_SECRET = '//get the access token secret key of your Twitter account by using my twigrapher-react2 and put it here'

  (Access tokens are used for uauth(user authorization) access to the Twitter API. aauth(application authorization) access is limited, but uauth can access to private accounts that the user is allowed to follow. Also, the maximum number of requests you can make in a certain period of time is set for each of twitter users.)
*/
python3.8 twiAPI_to_myDB_uauth.py
(Some deprecated dependencies are still being used, and it doesn't run with the newest python yet. I will update it soon.)
(After a while, maybe about 10 seconds, the program should terminate. Whether if the Tweets are downloaded well or not can be easily checked using MySQLWorkbench.)
(fetchSchedulers...py are intended to schedule the repetition of downloads from the Twitter API. How can we swim in the web of Tweets and Twitter accounts? Pretty interesting genre, indeed.)
```

### Issues
Something not working?  Please [open an issue](https://github.com/chromascore/twigrapher-api/issues)

(The data structure of the MySQL database created by this app is really shitty. I haven't studied about optimizing the datastructure in MySQL yet, and the Twitter API returns nested json. I didn't want to lose any data, and the result is the tones of columns and a long code which is horrible to maintain. I'm learning mongoDB now.)

(fetchScheduler_RFollowee_roller.py is intended to download data of all n-th connection users from a specified user, but it's not working yet.)
  
(fetchScheduler_fav_roller.py has not developed yet. However, Twitter API has much stricter limitation for access to favorites. Thus, with a free Twitter Dev account, we cannot play with favs that much.)

### Credits
This app is developed based on countless tutorials freely available on the WEB and Takapro's help: https://github.com/takapro

### Contact
Talk to me at @dev_kael on Twitter :)