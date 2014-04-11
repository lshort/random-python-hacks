"""Finding unique words from a URL text"""

import nltk
import urllib
import re
from nltk.corpus import words

def unique_words(url):
    raw = nltk.clean_html(urllib.urlopen(url).read())
    raw = raw[:8192]    # take a sample for testing purposes
    pattern = r'(\b[A-Z]+\b)|(\b[A-Za-z][a-z]*(-[a-z]+)*\b)'
    url_words = nltk.regexp_tokenize(raw, pattern)
    print url_words
    dict_words = words.words('en')
    return [w for w in url_words if w not in dict_words]

if __name__=="__main__":
    print unique_words('http://news.bbc.co.uk')
