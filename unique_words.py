"""Finding unique words from a URL text"""

import nltk
import urllib
import re
from nltk.corpus import words


def find_words(string):
    """Parse out plaintext words from the input text
    >>>find_words("Ad0 0012 REM monitor Mount Everest plain-text aFunction")
    ['REM', 'monitor', 'Mount', 'Everest', 'plain-text']
    """
    pattern = r'(\b[A-Z]+\b)|(\b[A-Za-z][a-z]*(-[a-z]+)*\b)'
    url_words = nltk.regexp_tokenize(raw, pattern)


def unique_words(url):
    """Find words in the url text that are not in the 'words' corpus"""
    raw = nltk.clean_html(urllib.urlopen(url).read())
    url_words = find_words(raw[:8192])    # take a sample for testing purposes
    print url_words
    dict_words = words.words('en')
    return [w for w in url_words if w not in dict_words and w.lower() not in dict_words]

if __name__=="__main__":
    ws = unique_words('http://news.bbc.co.uk')
    avg = sum(len(w) for w in ws)/len(ws)
    print avg
