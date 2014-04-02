""""""

import random
from nltk import *
from nltk.corpus import brown
from nltk.book import *

def random_text(corpus):
    print "*** Starting random text"
    big = bigrams(corpus)
    (start,ignore) = random.choice(big)
    occurrences = {}
    for (a,b) in big:
        if a in occurrences:
            occurrences[a].append(b)
        else:
            occurrences[a] = [b]
    sent_count = 3
    para = ""
    while (sent_count > 0 and occurrences[start]):
        para += start + " "
        start = random.choice(occurrences[start])
        if start[0] in ".!":
            sent_count -= 1
    print para

if __name__=="__main__":
    random_text(text1)
    random_text(text2)
