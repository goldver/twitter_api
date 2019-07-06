import tweepy
import json
import collections

TWITTER_APP_KEY = "TWITTER_APP_KEY" 
TWITTER_APP_SECRET = "TWITTER_APP_SECRET" 

TWITTER_KEY = "TWITTER_KEY"
TWITTER_SECRET = "TWITTER_SECRET"

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

hashtags_counter = collections.Counter()

class MyStreamListener(tweepy.StreamListener):

	
	def on_status(self, status):
		print("status", status)

	def on_data(self, tweet):
		tweet_dict = json.loads(tweet)		
		if 'entities' in tweet_dict:
			if 'hashtags' in tweet_dict['entities']:
				hashtags = tweet_dict['entities']['hashtags']
				if hashtags:
					for hashtag in hashtags:						
						hashtags_counter[hashtag['text']] += 1						
					
		print(hashtags_counter.most_common(10))
		print()
		# print(tweet_dict.keys())
		# if 'created_at' in tweet_dict:
		# 	print(tweet_dict['created_at'])
		# 	# Sat Jul 06 04:40:32 +0000 2019

		return True

	def on_error(self, status_code):
		print ("status_code", status_code)


stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["trump",  "donald trump"])

print("end")

