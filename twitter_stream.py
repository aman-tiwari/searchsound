from TwitterAPI import TwitterAPI
from optimistic import OptimisticDict
import cPickle
import itertools
from math import atan, ceil, exp
import re
from numpy import clip
from datetime import datetime
import happy_sad as hs


nonalp = re.compile(r'([\W_]+)') #Removes nonalphanumerics
url1 = re.compile(r'(http t co)') #Removes t.co urls
url2 = re.compile(r'\b(?=\w*[0-9])\w+\b') #removes blocks of text with numbers in (i.e shortened bit of url)

token = ''
secret_token = ''
cons_key = ''
cons_secret = ''

api = TwitterAPI(cons_key, cons_secret, token, secret_token)

def _happysad(to_test): #Computes the mean happiness of a word

    to_test = hs.wn.synsets(to_test)

    happy = [s for s in hs.slch(to_test, ss_happy) if s != None] #removes non matching word types
    sad = [s for s in hs.slch(to_test, ss_sad) if s != None]
    happy.sort(reverse=True), sad.sort(reverse=True)
    if not happy:
        happy = [0]
    if not sad:
        sad = [0]
    h_mean = (sum(happy[:10]))/10 #Mean of 10 highest values
    s_mean = (sum(sad[:10]))/10
    return h_mean-s_mean

def piano_sigmoid(x): #Maps -1 to 1 to 65 to 111, using a logistic function
    return int(((1 / (1+exp( -6*clip(x,-1.0,1.0) )))*47) + 65)

def process_tweet_into_notes(tweet):
    global odict
    #print 'on_data'
    if 'text' in tweet: #To dodge bookeeping tweets (e.g. deletes)
        if tweet['lang'] == 'en':
            sen = tweet['text']
            sen = url2.sub(' ', url1.sub(' ', nonalp.sub(' ', sen))) #Apples the REs defined above
            map(lambda s: sen.replace(s, ''), hs.neutral) #deletes neutral words
            sen = sen.split()
            out = []
            for w in sen:
                out.append(odict[w])

            #need to make removing long runs of 0s more efficient
            out = sum([[0]*min(len(list(v)), 4) if k == 0 else list(v) for k,v in itertools.groupby(out)], [])#
            out = map(piano_sigmoid, out)
            return ''.join(map(chr, out))
    return chr(65)

#to load up wordnet
def warm_up():
    for word in 'hello world welcome to this happiness filled day'.split():
        _happysad(word)
    return


try: #Imports an existing dict file, creates one if it can't access one
    with open('odict.dict', 'rb') as fil:
        odict = cPickle.load(fil)
        print 'Loaded odict!'
except IOError:
    odict = OptimisticDict(_happysad)


print 'computing happiness/sadness'
ss_happy = hs.build_synsets(hs.goods) #Builds synsets of happy & sad words,
ss_sad = hs.build_synsets(hs.sads)  #hs.goods & sads are just example dictionaries
from collections import deque
s_deque = deque()

try:
    r = api.request('statuses/sample', {'filter_level':'medium'})
    for item in r:
        s_deque.append(process_tweet_into_notes(item))
except KeyboardInterrupt:
    raise SystemExit
finally:
    saved = ''.join(s_deque)
    with open('odict.dict','wb') as fil: #Always executed, persists dict to disk
        cPickle.dump(odict, fil)
    with open('saved.txt', 'a') as fil:
        fil.write(saved)
    print 'process killed and file saved!'
