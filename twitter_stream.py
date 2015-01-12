from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import json
import re
import happy_sad as hs
import random
from optimistic import OptimisticDict
import time
import cPickle


nonalp = re.compile(r'([\W_]+)') #Removes nonaplhanumerics
url1 = re.compile(r'(http t co)') #Removes t.co urls
url2 = re.compile(r'\b(?=\w*[0-9])\w+\b') #removes blocks of text with numbers in (i.e shortened bit of url)

ss_happy = hs.build_synsets(hs.goods) #Builds synsets of happy & sad words,
ss_sad = hs.build_synsets(hs.sads)  #hs.goods & sads are just example dictionaries



token = '364804401-KfBPYVzdISBPzYHwgI0duAkFHTCnvevJIKGtLI9F'
secret_token = 'DVy6jnwdX5bdWwsFwin5kS47fQ3A07qKzUJy4qphnHE06'
cons_key = 'IK2t7YHXfZSRkZfgIhoZx5gd6'
cons_secret = 'E3FQb4AHD1s2E7yCPPQC8qOPhBWm85yW5WeF3epKCD6ObgLiyd'

def _happysad(to_test): #Computes the mean happiness of a word

    to_test = hs.wn.synsets(to_test)

    happy = [s for s in hs.slch(to_test, ss_happy) if s != None] #removes non matching word types
    sad = [s for s in hs.slch(to_test, ss_sad) if s != None]
    happy.sort(reverse=True), sad.sort(reverse=True)
    if not happy:
        happy = [0]
    if not sad:
        sad = [0]
    h_mean = int(sum(map(lambda x:x*100, happy[:10]))/10) #Mean of 10 highest values
    s_mean = int(sum(map(lambda x:x*100, sad[:10]))/10)
    return h_mean-s_mean

def process_tweet(data):
    global odict
    #print 'on_data'
    tweet = json.loads(data)
    if tweet.has_key('text'): #To dodge bookeeping tweets (e.g. deletes)
        if tweet['lang'] == 'en':
            sen = tweet['text']
            sen = url2.sub(' ', url1.sub(' ', nonalp.sub(' ', sen))) #Apples the REs defined above
            map(lambda s: sen.replace(s, ''), hs.neutral) #deletes neutral words
            sen = sen.split()
            out = map(lambda w: odict[w], sen)
            print out
    return True


class Listener(StreamListener):
    loopcounter = 100

    def on_data(self, data):
        return process_tweet(data)

    def on_error(self, error):
        print error
        return True


if __name__ == '__main__':

    try: #Imports an existing dict file, creates one if it can't access one
        with open('odict.dict', 'rb') as fil:
            odict = cPickle.load(fil)
    except IOError:
        odict = OptimisticDict(_happysad)

    listener = Listener()
    oauth = OAuthHandler(cons_key, cons_secret)
    oauth.set_access_token(token, secret_token)
    streamer = Stream(oauth, listener)
    try:
        streamer.sample()
    finally:
        with open('odict.dict','wb') as fil: #Always executed, persists dict to disk
            cPickle.dump(odict, fil)
