__version__ = '1.0.0'

import argparse
import collections
import datetime
import json

import matplotlib.pyplot as plt
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

x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

plt.ion()
fig = plt.figure(figsize=(13, 6))
ax = fig.add_subplot(111)
ax.set_ylim(bottom=0, top=30)
line1, = ax.plot(x, y, '-o', alpha=0.8)
plt.show()


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        """
        :param status:
        :return:
        """
        logger.info("status", status)

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
        if (datetime.datetime.now() - start_time > datetime.timedelta(0, 5, 0)):
            start_time = datetime.datetime.now()
            temp = hashtags_counter.most_common(100)
            hashtags_counter.clear()
            for ht in temp:
                hashtags_counter[ht[0]] = ht[1] * 0.9
            # drawing
            ht_zip = list(zip(*(hashtags_counter.most_common(10))))
            x_range = list(range(10))
            line1.set_xdata(x_range)
            line1.set_ydata(ht_zip[1])
            plt.xticks(x_range, ht_zip[0])
            plt.pause(0.1)
        return True

    def on_error(self, status_code):
        """
        :param status_code:
        :return:
        """
        logger.info("status_code", status_code)


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
