"""Some fun with random text generation"""

import random
from nltk import *
from nltk.util import trigrams
from nltk.book import text1, text2, text3
from nltk.corpus import gutenberg
import textwrap

def best_n_sents(corpus_file, n):
    print "*** Printing best N sentences"
    words = gutenberg.words(corpus_file)
    fd = FreqDist(words)
    sents = gutenberg.sents(corpus_file)
    ss= sorted(sents, reverse=True, key=(lambda x:sum(fd[w] for w in x)) )
    for i in range(n):
        for line in textwrap.wrap(' '.join(ss[i])):
            print line


def random_text_bigram(corpus, sentence_count, delim):
    """Generate some random sentences in the style of the corpus.
    Uses a bigram distribution"""
    print "*** Starting random text bigram"
    big = bigrams(corpus)
    (word,ignore) = random.choice(big)
    cfd = ConditionalFreqDist(
        (first,second)
        for (first, second) in big[:-1])
        # must remove the last bigram, as we may not be able to
        # proceed from the very last word in the corpus
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

def random_text_trigram(corpus, sentence_count, delim):
    """Generate some random sentences in the style of the corpus.
    Uses a trigram distribution"""
    print "*** Starting random text trigram"
    tri = trigrams(corpus)
    (prev_word,crnt_word,ignore) = random.choice(tri)
    cfd = ConditionalFreqDist(
        ((first,second),third)
        for (first, second, third) in tri[:-2])
        # must remove the last 2 trigrams, as we may not be able to
        # proceed from the last 2 words in the corpus
    para = ""
    while (sentence_count > 0):
        para += crnt_word
        if crnt_word[0] in ".!?":
            sentence_count -= 1
            para += delim
        else:
            para += " "
        index = (prev_word,crnt_word)
        prev_word = crnt_word
        crnt_word = random.choice(cfd[index].samples())
    print para

if __name__=="__main__":
#    random_text_bigram(text1,4, "  ")
#    random_text_bigram(text2,3, "  ")
#    random_text_trigram(text1,4, "  ")
#    random_text_trigram(text2,3, "  ")
    best_n_sents('austen-emma.txt',25)
