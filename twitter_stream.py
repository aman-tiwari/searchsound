from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import happy_sad as hs

nonalp = re.compile(r'([\W_]+)') #Removes nonaplhanumerics
url1 = re.compile(r'(http t co)') #Removes t.co urls
url2 = re.compile(r'\b(?=\w*[0-9])\w+\b') #removes blocks of text with numbers in (i.e shortened bit of url)

ss_happy = hs.build_synsets(hs.goods) #Builds synsets of happy & sad words, hs.goods can be any list
ss_sad = hs.build_synsets(hs.sads)



token = '364804401-KfBPYVzdISBPzYHwgI0duAkFHTCnvevJIKGtLI9F'
secret_token = 'DVy6jnwdX5bdWwsFwin5kS47fQ3A07qKzUJy4qphnHE06'
cons_key = 'IK2t7YHXfZSRkZfgIhoZx5gd6'
cons_secret = 'E3FQb4AHD1s2E7yCPPQC8qOPhBWm85yW5WeF3epKCD6ObgLiyd'

def _happysad(to_test):

    to_test = hs.wn.synsets(to_test)

    happy = [s for s in hs.slch(to_test, ss_happy) if s != None]
    sad = [s for s in hs.slch(to_test, ss_sad) if s != None]
    happy.sort(reverse=True), sad.sort(reverse=True)
    if not happy:
        happy = [0]
    if not sad:
        sad = [0]
    h_mean = sum(map(lambda x:x*100, happy[:10]))/10 #Mean of 10 highest values
    s_mean = sum(map(lambda x:x*100, sad[:10]))/10
    return h_mean-s_mean

class Listener(StreamListener):

    def on_data(self, data):
        #print 'trying'
        tweet = json.loads(data)
        try:
            if tweet['lang'] == 'en':
                sen = tweet['text']
                sen = url2.sub(' ', url1.sub(' ', nonalp.sub(' ', sen))) #Apples the REs defined above
                map(lambda s: sen.replace(s, ''), hs.neutral) #deletes neutral words
                sen = sen.split()
                out = []
                out = map(lambda w: _happysad(w), sen)
                print out

        except KeyError:
            pass
        #print data
        return True

    def on_error(self, error):
        print error


if __name__ == '__main__':

        listener = Listener()
        oauth = OAuthHandler(cons_key, cons_secret)
        oauth.set_access_token(token, secret_token)
        streamer = Stream(oauth, listener)
        streamer.sample()
