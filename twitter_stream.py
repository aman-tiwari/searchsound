from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import json
import re
import happy_sad as hs
import random
from optimistic import OptimisticDict
import time
import cPickle
import multiprocessing as mp
from Queue import Empty, Full
import itertools
from math import atan, ceil

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
    if 'text' in tweet: #To dodge bookeeping tweets (e.g. deletes)
        if tweet['lang'] == 'en':
            sen = tweet['text']
            sen = url2.sub(' ', url1.sub(' ', nonalp.sub(' ', sen))) #Apples the REs defined above
            map(lambda s: sen.replace(s, ''), hs.neutral) #deletes neutral words
            sen = sen.split()
            out = map(lambda w: odict[w], sen)
            out = sum([[0]*min(len(list(v)), 4) if k == 0 else list(v) for k,v in itertools.groupby(out)], []) #removes long runs of 0
            return out
    return [0]

def warm_up():
    for word in 'hello world welcome to this happiness filled day'.split():
        _happysad(word)
    return

class Listener(StreamListener):

    def on_data(self, data):
        try:
            eat_que.put_nowait(data)
            #print 'putted!'
        except Full:
            #print 'full :('
            return True
        return True

    def on_error(self, error):
        print error
        return True

def eater(queue):
    while True:
        try:
            tweet = queue.get()
            #print 'processing'
            processed = process_tweet(tweet)
            #print processed
            for note in processed:
                note = ceil(70*atan( 0.07 * note )) + 110
                note = chr(int(note))
                print note,
            #print 'processed!'
        except Empty:
            pass



if __name__ == '__main__':


    #print 'Warming up! (~30secs)'
    warm_up()
    #print 'Warm!'
    eat_que = mp.Queue(maxsize=50)

    eater_process = mp.Process(target=eater, args=((eat_que),))
    eater_process.daemon = True

    try: #Imports an existing dict file, creates one if it can't access one
        with open('odict.dict', 'rb') as fil:
            odict = cPickle.load(fil)
            print 'Loaded odict!'
    except IOError:
        odict = OptimisticDict(_happysad)

    listener = Listener()
    oauth = OAuthHandler(cons_key, cons_secret)
    oauth.set_access_token(token, secret_token)
    streamer = Stream(oauth, listener)
    try:
        eater_process.start()
        print 'process started!'
        streamer.sample()
        #print 'stream started!'
    except KeyboardInterrupt:
        raise SystemExit
    finally:
        eater_process.join()
        with open('odict.dict','wb') as fil: #Always executed, persists dict to disk
            cPickle.dump(odict, fil)
        print 'process killed and file saved!'
