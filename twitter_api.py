__version__ = '1.0.0'

import argparse
import collections
import datetime
import json
import os
import sys

import tweepy

from logs import logger

logger.info("### RUNNING TWITTER_API SCRIPT ###")

parser = argparse.ArgumentParser(prog='main',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=100,
                                                                                     width=200))
parser.add_argument('PATTERN_1', help='Please write your pattern')
parser.add_argument('PATTERN_2', help='Please write your another pattern')

args = parser.parse_args()
pattern_1 = args.PATTERN_1
pattern_2 = args.PATTERN_2

TWITTER_APP_KEY = ""
TWITTER_APP_SECRET = ""

TWITTER_KEY = ""
TWITTER_SECRET = ""

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

hashtags_counter = collections.Counter()
start_time = datetime.datetime.now()


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        """
        :param status:
        :return:
        """
        print("status", status)

    def on_data(self, tweet):
        """
        :param tweet:
        :return:
        """
        global start_time
        tweet_dict = json.loads(tweet)
        if 'entities' in tweet_dict:
            if 'hashtags' in tweet_dict['entities']:
                hashtags = tweet_dict['entities']['hashtags']
                if hashtags:
                    for hashtag in hashtags:
                        hashtags_counter[hashtag['text']] += 1
        logger.info(hashtags_counter.most_common(10))
        if (datetime.datetime.now() - start_time > datetime.timedelta(0, 10, 0)):
            start_time = datetime.datetime.now()
            temp = hashtags_counter.most_common(100)
            hashtags_counter.clear()
            # reduce time
            for ht in temp:
                hashtags_counter[ht[0]] = ht[1] * 0.9

        logger.info(datetime.datetime.now() - start_time)

        return True

    def on_error(self, status_code):
        """
        :param status_code:
        :return:
        """
        print("status_code", status_code)


def main():
    try:
        stream_listener = MyStreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        stream.filter(track=[pattern_1, pattern_2])

        logger.info("end")
    except Exception as ex:
        logger.info("### oops, something is wrong :( " + str(ex) + " ###")
        sys.exit(os.EX_OSERR)


if __name__ == "__main__":
    main()
