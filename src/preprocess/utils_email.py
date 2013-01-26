#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re 
import quopri
import codecs
from nltk.tokenize import PunktWordTokenizer


'''
Globals 
'''
STRIP_CHAR_LIST = [u'_', u'-', u',', u'!', u':', u'.', u'?', 
                   u';', u'=', u'…', u'•', u'–', u'¿', u'¡', 
                   u'º', u'ª', u'«', u'»', u'*', u'~', u'`', 
                   u':', u'.', u'#'] 
REMOVE_LIST = [u"[", u"]", u"{", u"}", u"(", u")", 
          u"'", u".", u"..", u"...", u",", u"?", u"!", 
          u"/", u"\"", u"\"", u";", u":", u"-", 
          u"`", u"~", u"@", u"$", u"^", u"|", u"#", u"=", u"*"];
          
'''
Initializes the tokenizer 
'''
tokenizer = PunktWordTokenizer()

def cleanup(token):
    try:
        
        token = quopri.decodestring(token).encode('UTF-8')

        token = re.sub('[\(\)\{\}\[\]\'\"\\\/*<>|]', '', token)    
        for each_char in STRIP_CHAR_LIST:
            token = token.strip(each_char)

    except: 
        None 
    
    return token.strip()

   
def punkt_word_tokenizer(text):
    '''
    A tokenizer based on NLTK's PunktWordTokenizer 
    '''

    
    tokens = tokenizer.tokenize(text)
    tokens = [cleanup(w) for w in tokens]
    tokens = [w for w in tokens if w not in REMOVE_LIST]
    return tokens


def load_en_stopwords(filename):
    
    stopwords = list();
    with codecs.open(filename, mode='r', encoding='utf-8') as fSW: 
        for line in fSW: 
            stopwords.append(line.strip().lower())
    return stopwords

