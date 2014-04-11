"""Finding unique words from a URL text"""

import nltk
import urllib
import re
from nltk.corpus import words

def unique_words(url):
    raw = urllib.urlopen(url).read()
    url_words = [w for w in nltk.word_tokenize(raw) if re.search('\w+',w)]
    dict_words = words.words('en')
    return [w for w in url_words if w not in dict_words]

if __name__=="__main__":
    print unique_words('http://news.google.com')
