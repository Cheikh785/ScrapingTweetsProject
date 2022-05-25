from __future__ import print_function
from errno import errorcode
import twitter
import mysql.connector
from datetime import date, datetime, timedelta

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "",
	database = "getTweetsProject",
	auth_plugin = "mysql_native_password"
)

# Create an Api instance.
api = twitter.Api(consumer_key = CONSUMER_KEY,
					consumer_secret = CONSUMER_SECRET,
					access_token_key = ACCESS_TOKEN,
					access_token_secret = ACCESS_TOKEN_SECRET)
# users = api.GetFriends()
results = api.GetSearch(
	raw_query="q=bitcoin OR cryptomoney OR cryptocurrency OR blockchain&count=500&tweet_mode=extended"
)

mycursor = mydb.cursor(buffered=True)

add_tweets = ("INSERT INTO tweets "
               "(created_at, id_str, text, contributors, truncated, coordinates, source, retweet_count, url, "
			   "screen_name, name, followers_count, listed_count, friends_count, lang, user_location, profile_image_url) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			)

add_hashtags = ("INSERT INTO hashtags "
				"(text, id_owner) "
				"VALUES (%s, %s) "
		)
add_user_mentions = ("INSERT INTO user_mentions "
                                "(name, id_str, id_owner) "
                                "VALUES (%s, %s, %s) "
			)


k = 0
cpt_tweets = 0
cpt_hashtags = 0
cpt_user_mentions = 0
for u in results:
	print("-------------------------------------------------------------------------------------------------------------")
	print(u.created_at, '\n\n', u.id_str, '\n\n', u.full_text, '\n\n', u.contributors, '\n\n', u.truncated, '\n\n', u.coordinates, '\n\n', u.source, '\n\n', u.retweet_count, '\n\n', u.urls, '\n\n', u.user.screen_name, '\n\n', u.user.name, '\n\n', u.user.followers_count, '\n\n', u.user.listed_count, '\n\n', u.user.friends_count, '\n\n', u.lang, '\n\n', u.location, '\n\n', u.user.profile_banner_url, '\n\n')
	print("\n\n")
	data_id = (u.id_str)
	data_tweets = (u.created_at, u.id_str, u.full_text, u.contributors, u.truncated, u.coordinates, u.source, u.retweet_count, 'null', u.user.screen_name, u.user.name, u.user.followers_count, u.user.listed_count, u.user.friends_count, u.lang, u.location, u.user.profile_banner_url)
	user_mentions = u.user_mentions
	list_hashtags = u.hashtags
	#hashtags_text = ""
	#for j in range(0, len(list_hashtags)):
	#	hashtags_text += list_hashtags[j].text
	#	hashtags_text += " "
	#data_hashtags = (hashtags_text, u.id_str)
	#print("$$$", hashtags_text)
	#mycursor.execute("SELECT count(*) from tweets where id_str = %s", (data_id))
	#k = mycursor.fetchone()[0]
	mycursor.execute("SELECT * FROM tweets")
	for row in mycursor.fetchall():
		if(u.id_str == row[1]):
			k += 1;
			print("###Tweet already exist")
	if k == 0: 
		try: 
			mycursor.execute(add_tweets, data_tweets)
			cpt_tweets += 1
			print("Tweet successfuly insert")
			#insert hashtags if exist
			try: 
				for l in range(0, len(list_hashtags)):
					data_hashtags = (list_hashtags[l].text, u.id_str)
					mycursor.execute(add_hashtags, data_hashtags)
					cpt_hashtags += 1
					print("hashtag successfuly insert")
			except mysql.connector.Error as err: 
				print("Error insert hashtags ! ! !", err.msg)
			#insert user_mentions if exist
			try: 
				for l in range(0, len(user_mentions)): 
					data_user_mentions = (user_mentions[l].name, user_mentions[l].id_str, u.id_str)
					mycursor.execute(add_user_mentions, data_user_mentions)
					cpt_user_mentions += 1
					print("user_mention successfuly insert")
			except mysql.connector.Error as err: 
				print("Error insert user_mentions ! ! !", err.msg)

		except mysql.connector.Error as err: 
			print("Error insert tweets ! ! ! ", err.msg)
	mydb.commit()
	print("-------------------------------------------------------------------------------------------------------------")


print("\n\n\n")
print(cpt_tweets, "tweets save")
print(cpt_hashtags, "hashtags insert")
print(cpt_user_mentions, "user mentions insert")
print("\n\n")

mycursor.close()
mydb.close()





# # from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream 

# import twitter_credentials

# class StdOutListener(Stream) :

#     def on_data(self, data) :
#         print(data)
#         return True;

#     def on_error(self, status) : 
#         print(status)


# if __name__ == "main" : 
#     listener = StdOutListener()
#     auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, Twitter.CONSUMER_SECRET)
#     auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

# stream = Stream(auth, listener)

# stream.filter(track=['donal trump', 'hillary clinton', 'barack obama'])




