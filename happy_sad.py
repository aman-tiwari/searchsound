import nltk
import numpy as np
from nltk.corpus import wordnet as wn
from itertools import chain

goods = ['good', 'happiness', 'birth', 'life', 'justice', 'love', 'benefit'
         'sunshine', 'warmth', 'acceptance', 'smile', 'laugh', 'laughter', 'joy']
sads = ['bad', 'sadness', 'kill', 'death', 'unjust', 'hate', 'loss', 'lose',
        'war', 'sorrow', 'atrocity', 'tears', 'hitler']

ss_happy    = frozenset(chain(*[wn.synsets(good) for good in goods]))
ss_sad      = frozenset(chain(*[wn.synsets(sad) for sad in sads]))
#print ss_happy

def slch(to_test, feel):
    o_list = []
    for i in to_test:
            for j in feel:
                    try:
                            o_list.append(i.lch_similarity(j))
                    except nltk.corpus.reader.wordnet.WordNetError:
                        pass
    return o_list

def wup(to_test, feel):
    o_list = []
    for i in to_test:
            for j in feel:
                    try:
                            o_list.append(i.wup_similarity(j))
                    except:
                        pass
    return o_list
while True:
    to_test = wn.synsets(raw_input(' : '))

    happy = [s for s in slch(to_test, ss_happy) if s != None]
    sad = [s for s in slch(to_test, ss_sad) if s != None]
    happy.sort(reverse=True), sad.sort(reverse=True)
    if not happy:
        happy = [0]
    if not sad:
        sad = [0]
    h_mean = float(sum(happy[:10]))/10
    s_mean = float(sum(sad[:10]))/10

    print 'Happy: ' + str(h_mean)
    print 'Sad: ' + str(s_mean)
    print 'Wup'

    happy = [s for s in wup(to_test, ss_happy) if s != None]
    sad = [s for s in wup(to_test, ss_sad) if s != None]
    happy.sort(reverse=True), sad.sort(reverse=True)
    if not happy:
        happy = [0]
    if not sad:
        sad = [0]
    h_mean = float(sum(happy))/len(sad)
    s_mean = float(sum(sad))/len(sad)

    print 'Happy: ' + str(h_mean)
    print 'Sad: ' + str(s_mean)
