import nltk
from nltk.corpus import wordnet as wn
from itertools import chain


#Example list
goods = ['good', 'happiness', 'birth', 'life', 'justice', 'love', 'benefit'
         'sunshine', 'warmth', 'acceptance', 'smile', 'laugh', 'laughter', 'joy']
sads = ['bad', 'sadness', 'kill', 'death', 'unjust', 'hate', 'loss', 'lose',
        'war', 'sorrow', 'atrocity', 'tears', 'hitler']

#neutral list
neutral = set(['the', 'to', 'and', 'while', 'is', "'if", 'will', "not", 'that', 'this', 'there'])

def build_synsets(words):
    """Builds a flat list of synsets from a list of words"""
    return frozenset(chain(*[wn.synsets(word) for word in words]))

def slch(to_test, targets):
    """Takes a list of synsets to test and a list of target synsets & finds the lch similarity"""
    similarities = []
    for i in to_test:
            for j in targets:
                    try:
                            similarities.append(i.lch_similarity(j))
                    except nltk.corpus.reader.wordnet.WordNetError: #Ignore incomparable types of words
                        pass
    return similarities

def wup(to_test, targets):
    """ Takes a list of synsets to test and a list of target synsets & finds the wup similarity"""
    similarities = []
    for i in to_test:
            for j in targets:
                    try:
                            similarities.append(i.wup_similarity(j))
                    except nltk.corpus.reader.wordnet.WordNetError: #Ignore incomparable types
                        pass
    return similarities


if __name__ == '__main__':
    ss_happy    = build_synsets(goods)
    ss_sad      = build_synsets(sads)
    #print ss_happy
    while True:
        sen = raw_input(' : ')
        map(lambda s: sen.replace(s, ''), neutral)
        sen = sen.split()
        out = []
        for word in sen:
            to_test = wn.synsets(word)

            happy = [s for s in wup(to_test, ss_happy) if s != None]
            sad = [s for s in wup(to_test, ss_sad) if s != None]
            happy.sort(reverse=True), sad.sort(reverse=True)
            if not happy:
                happy = [0]
            if not sad:
                sad = [0]
            h_mean = float(sum(happy[:10]))/10
            s_mean = float(sum(sad[:10]))/10

            out.append(h_mean-s_mean)

            # print 'Happy: ' + str(h_mean)
            # print 'Sad: ' + str(s_mean)
            # print 'Wup'
            #
            # # happy = [s for s in wup(to_test, ss_happy) if s != None]
            # # sad = [s for s in wup(to_test, ss_sad) if s != None]
            # # happy.sort(reverse=True), sad.sort(reverse=True)
            # # if not happy:
            # #     happy = [0]
            # # if not sad:
            # #     sad = [0]
            # # h_mean = float(sum(happy))/len(sad)
            # # s_mean = float(sum(sad))/len(sad)
            # #
            # # print 'Happy: ' + str(h_mean)
            # # print 'Sad: ' + str(s_mean)
        print out
