""""""

import random
from nltk import *
from nltk.corpus import brown
from nltk.book import text1, text2, text3

def random_text(corpus, sentence_count, delim):
    print "*** Starting random text"
    big = bigrams(corpus)
    (word,ignore) = random.choice(big)
    cfd = ConditionalFreqDist(
        (first,second)
        for (first, second) in big)
    para = ""
    while (sentence_count > 0):
        para += word
        if word[0] in ".!?":
            sentence_count -= 1
            para += delim
        else:
            para += " "
        word = random.choice(cfd[word].samples())
    print para

if __name__=="__main__":
    random_text(text1,4, "___")
    random_text(text2,3, "  ")
