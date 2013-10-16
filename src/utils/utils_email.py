#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script has all the utility functions for 
processing the enron email data set  

Created by: Clint P. George
Created On: Jan 29, 2013   

'''

import re 
import quopri
import codecs
import email 
from nltk.tokenize import PunktWordTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import SnowballStemmer

'''
Global variables 
'''
DATE_FORMAT = "%a,%d %m %y %H:%M:%S -T (Z)"
STRIP_CHAR_LIST = [u'_', u'-', u',', u'!', u':', u'.', u'?', 
                   u';', u'=', u'…', u'•', u'–', u'¿', u'¡', 
                   u'º', u'ª', u'«', u'»', u'*', u'~', u'`', 
                   u':', u'.', u'#'] 
REMOVE_LIST = [u"[", u"]", u"{", u"}", u"(", u")", 
          u"'", u".", u"..", u"...", u",", u"?", u"!", 
          u"/", u"\"", u"\"", u";", u":", u"-", 
          u"`", u"~", u"@", u"$", u"^", u"|", u"#", u"=", u"*"];
          
'''
Initializes the tokenizer, lemmatizer, and stemmer  
'''
tokenizer = PunktWordTokenizer()
wordnet_lmtzr = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer("english") # Choose a language

def xstr(s):
    return '' if s is None else str(s)


def cleanup(token):
    '''Clean up a given token based on regular expression, strip(),
    and a predefined set of characters 
    
    Returns: 
        a cleaned up token 
    Arguments:
        a token (str) 
    '''
    try:
        
        token = quopri.decodestring(token).encode('UTF-8')

        token = re.sub('[\(\)\{\}\[\]\'\"\\\/*<>|]', '', token)    
        for each_char in STRIP_CHAR_LIST:
            token = token.strip(each_char)
        
        if token in REMOVE_LIST: 
            return ''
    except: 
        '' 
    
    return token.strip()

   
def punkt_word_tokenizer(text):
    '''A tokenizer based on NLTK's PunktWordTokenizer 
    
    Returns: 
        a list of tokens 
    Arguments:
        a string to tokenized 
    
    '''

    text = ' '.join(text.lower().split()) # removes newline, tab, and white space        
    tokens = tokenizer.tokenize(text)
    # tokens = [cleanup(w) for w in tokens]
    # tokens = [w for w in tokens if w not in REMOVE_LIST]
    filtered = []
    for w in tokens:
        try: 
            w = cleanup(w)
            if len(w) > 0: 
                for wt in w.split(','): 
                    filtered.append(wt)
        except: 
            pass 
    
    return filtered

def whitespace_tokenize(doc_text):
    '''
    This function will tokenize the given 
    document text into tokens  based on whitespace 
    
    '''
    return doc_text.lower().split()


def load_en_stopwords(filename):
    '''Loads English stop-words from a given file 
    
    Return: 
        a list of stop words
    Arguments: 
        the stop-words file name
    '''
    
    stopwords = []
    with codecs.open(filename, mode='r', encoding='utf-8') as fSW: 
        for line in fSW: 
            stopwords.append(line.strip().lower())
    return stopwords


def lemmatize_tokens(word_tokens):
    '''
    Lemmatize tokens based on WordNet 
    '''
    tokens = [] 
    for token in word_tokens:
        try:
            # print 'lemma:', token, '-->', wordnet_lmtzr.lemmatize(token)   
            token = wordnet_lmtzr.lemmatize(token)
        except: pass 
        tokens.append(token)
    
    return tokens


def stem_tokens(word_tokens):
    '''
    Stem tokens based on Snowball stemmer  
    '''
    tokens = [] 
    for token in word_tokens:
        try:
            # print 'stem:', token, '-->', snowball_stemmer.stem(token)   
            token = snowball_stemmer.stem(token)
        except: pass 
        tokens.append(token)
        
    return tokens




def parse_plain_text_email(file_path, tokenize = True, lemmatize = False, stem = False, nonascii = True):
    '''Processes a single email file that's in plain/text format 
    
    Arguments: 
        file_path - the email file path 
    '''
    def removeNonAscii(s): 
        return ''.join(i for i in s if ord(i) < 128)
    
    
    # Handles different text encoding 
    email_text = ''
    receiver = ''
    sender = ''
    cc = ''
    bcc = ''
    subject = ''
    body_text = ''
    date = ''
    
# TODO: Need to handle the issue of encoding... Oct 16, 2013  
#    import chardet 
#    with open(file_path) as fp:
#        email_text = fp.read()
#        chardet_charset = chardet.detect(email_text)
        
    
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            fp = codecs.open(file_path, 'r', body_charset)
            email_text = fp.read()
            email_text = email_text.encode('UTF-8') # encodes to UNICODE 
            fp.close()
        except UnicodeError:
            pass
        else: break

    
#    print 'Body char set:', body_charset, 'chardet:', chardet_charset  

    if len(email_text) > 0: 
    
        msg = email.message_from_string(email_text)  
        receiver = xstr(msg['to'])
        sender = xstr(msg['from'])
        cc = xstr(msg['cc'])
        bcc = xstr(msg['bcc']) # Subodh - Rahul - Get BCC attribute from the email 
        subject = xstr(msg['subject'])
        date = xstr(msg['date'])
        body_text = msg.get_payload()
        
        if tokenize:
            tokens = punkt_word_tokenizer(body_text)
            if lemmatize: tokens = lemmatize_tokens(tokens)
            if stem: tokens = stem_tokens(tokens)
            
            if body_charset == 'ISO-8859-1':
                body_text = ''
                for ch in tokens:
                    try:
                        token = ch.decode('ascii')
                        body_text += ' ' + token
                    except UnicodeDecodeError:
                        pass
            else:
                body_text = ' '.join(tokens)
        else:
            # If message is multi-part, we only want the text version of 
            # the body, this walks the message and gets the body.
            if msg.get_content_maintype() == 'multipart': 
                for part in msg.walk():       
                    if part.get_content_type() == "text/plain":
                        body_text += part.get_payload(decode=True)
                    else:
                        continue
        
    if not nonascii:            
        ret = (removeNonAscii(receiver), 
                removeNonAscii(sender), 
                removeNonAscii(cc), 
                removeNonAscii(subject), 
                removeNonAscii(body_text), 
                removeNonAscii(bcc), 
                removeNonAscii(date))
    else: 
        ret = (receiver,  sender, cc, subject, body_text, bcc, date)
    
    return ret
    

