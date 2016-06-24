from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

from collections import defaultdict
from datetime import datetime, timedelta 
import sys, pdb, pprint, time, os

# Twitter Credentials
consumer_key = os.environ['API_KEY']
consumer_secret = os.environ['API_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_SECRET']

# Normally I might use a fun library for this, but I didn't want to force any unnecessary 
#installs so some unicode will do! 
BOLD = '\033[1m'
NORMAL = '\033[0m'
BLUE = '\033[94m'
LBLUE = '\033[95m'
BLACK = '\033[30m'

COMMAND_ARGS = "command should match: python streaming.py n (where n is number of minutes) \n setting minutes to 2"
DEFAULT_MINS = 2

def default_tweet():
    """Returns/creates value for defaultdict 
    when no tweet_id key exists in processed_tweets.
    """
    return ([('', datetime.now().time())]) # a dummy tweet, nec??? )

def get_minutes():
    """Returns n minutes where n is defined by the user or set as
    2 if no argument is provided
    """
    if len(sys.argv) == 2: 
        if int(sys.argv[1]) < 0: 
            print("must provide an integer (number, >0)")
            print(COMMAND_ARGS)
            return DEFAULT_MINS
        return int(sys.argv[-1])
    else:
        print("no more than 1 minute quantity allowed")
        print(COMMAND_ARGS)

    return DEFAULT_MINS


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    mins = get_minutes()
    
    processed_tweets = defaultdict(default_tweet)
    current_twts = []
    pp = pprint.PrettyPrinter(indent=4)
    last = datetime.now() 

    def on_status(self, data):
        """ For each status in stream, status is processed and current_tweets refreshed
        Includes calls to print top retweets
        :param data: a tweet returned from stream 
        """
       
        now = datetime.now().time()  # so we don't refresh on every new tweet, start the clock 

        info = self.process_tweet(data) 
        self.current_twts.append(info)

        if datetime.now() > self.last + timedelta(seconds = 10):
            self.current_twts = self.refresh(self.mins, self.current_twts)
            top_tweets = self.top_tweets(self.current_twts)
            self.print_top(top_tweets)
            self.last = datetime.now() 
            return True 

    def on_error(self, status):
        print(status)
    
    def process_tweet(self, data):
        """ For each status in stream, status is processed and current_tweets refreshed
        Includes calls to print top retweets
        :param data: a tweet returned from stream 
        """

        if hasattr(data, 'retweeted_status'): # only difference is ID (key storage)
            id = data.retweeted_status.id
        else: 
            id = data.id
        
        self.processed_tweets[id].append((data.text, data.created_at))

        count = len(self.processed_tweets[id]) -1

        lookup = self.processed_tweets[id] 
        return (lookup[-1][0], lookup[-1][1], count)

    def refresh(self, mins, tweets): 
        start_time = datetime.utcnow() + timedelta(minutes=-mins) # the current one 
        tweets = filter(lambda twt: twt[1] > start_time, tweets)

        return tweets 

    def top_tweets(self, current):
        top = sorted(current, key=lambda info: info[2], reverse = True) # EEK

        return top[:10] 

    def print_top(self, top):
        print(BLUE + BOLD + 'TOP RETWEETS ' + u'\U0001F4AC' + '  IN PAST ' + str(self.mins) + ' ' + u'\U0001F550' + BLUE + '  MINUTES SINCE ' + BLACK)
        print(datetime.utcnow().time())
        print("\n")
        counter = 1
        for i in top: 
            print(BOLD + str(counter)+ NORMAL + ': ' + i[0].encode('utf-8'))
            print(BOLD + BLUE + '  RT count:  ' + BLACK + NORMAL +str(i[2]) + BOLD + '   Time:  ' + NORMAL + str(i[1]) + '\n')
            counter += 1

        print("==========================================================================\n \n")
    

if __name__ == '__main__':
    
    l = StdOutListener() # odnt want to override init
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)

    #** QUESTION: TWEEPY NEEDS A TRACK/LOCATION
    stream.filter(track=['Harry_Styles'])#locations=[-180,-90,180,90])
