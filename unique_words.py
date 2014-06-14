"""Finding unique words from a URL text"""

import nltk
import urllib
import re
from nltk.corpus import words


def trie_insert(trie, word, value):
    if word:
        first, rest = word[0], word[1:]
        if first not in trie:
            trie[first] = {}
        trie_insert(trie[first],rest, value)
    else:
        trie['value'] = value

def build_trie(word_list):
    root_trie = {}
    for word in word_list:
        trie_insert(root_trie,word,word)
    return root_trie

def unique_part(trie, word):
    last_mult = -1
    crnt = trie
    for i in range (0,len(word)):
        if len(crnt) > 1:
            last_mult = i
        crnt = crnt[word[i]]
    return word[:last_mult+1]

def catalan_sum(previous, n):
    sum = 0;
    for i in range (n):
        sum += previous[i] * previous[n-i-1]
    return sum

def catalan(n):
    if n<1:
        return 1
    c = [1]
    for i in range(1,n+1):
        sum = catalan_sum(c,i)
        c.append(sum)
    return c[n]

def find_words(string):
    """Parse out plaintext words from the input text
    >>>find_words("Ad0 0012 REM monitor Mount Everest plain-text aFunction")
    ['REM', 'monitor', 'Mount', 'Everest', 'plain-text']
    """
    pattern = r'(\b[A-Z]+\b)|(\b[A-Za-z][a-z]*(-[a-z]+)*\b)'
    url_words = nltk.regexp_tokenize(string, pattern)
    return url_words

def search(substring, ws):
    for word in ws:
        if substring in word:
            yield word

def words10(txt):
    ws = find_words(txt)
    cutoff = 9 * len(ws) / 10
    return [w for w in set(ws[cutoff:]) if w not in set(ws[:cutoff])]

def get_first(url, count):
    raw = nltk.clean_html(urllib.urlopen(url).read())
    return (raw[:count],raw[count:])

def words10url(url):
    (words,ignore) = get_first(url, 65536)
    return words10(words)

def unique_words(url):
    """Find words in the url text that are not in the 'words' corpus"""
    (url_words,ignore) = get_first(url,8192)
    dict_words = words.words('en')
    return filter(lambda w:w not in dict_words and w.lower() not in dict_words,
                  url_words )

if __name__=="__main__":
    wlist = (['tom','the','mary','torn','zzz','zulu', 'i','igloo'])
    foo = build_trie(wlist)
    for w in wlist:
        print unique_part(foo,w)

#    print catalan(1)
#    print catalan(2)
#    print catalan(3)
#    print catalan(4)
#    print catalan(5)
#    print catalan(6)
#    ws = words10url('http://news.bbc.co.uk')
#    print ws
