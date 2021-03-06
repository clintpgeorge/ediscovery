#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script has all the utility functions for 
processing the enron email dataset  

Created by: Clint P. George
Created On: Jan 29, 2013   

@deprecated: June 21, 2013
@note: Please use utils.utils_email instead 
'''

import re 
import quopri
import codecs
import email 
from nltk.tokenize import PunktWordTokenizer


'''
Global variables 
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

    except: 
        None 
    
    return token.strip()

   
def punkt_word_tokenizer(text):
    '''A tokenizer based on NLTK's PunktWordTokenizer 
    
    Returns: 
        a list of tokens 
    Arguments:
        a string to tokenized 
    
    '''

    
    tokens = tokenizer.tokenize(text)
    tokens = [cleanup(w) for w in tokens]
    tokens = [w for w in tokens if w not in REMOVE_LIST]
    return tokens


def load_en_stopwords(filename):
    '''Loads English stop-words from a given file 
    
    Return: 
        a list of stop words
    Arguments: 
        the stop-words file name
    '''
    
    stopwords = list();
    with codecs.open(filename, mode='r', encoding='utf-8') as fSW: 
        for line in fSW: 
            stopwords.append(line.strip().lower())
    return stopwords



def parse_plain_text_email(file_path):
    '''Processes a single email file that's in plain/text format 
    
    Arguments: 
        file_path - the email file path 
    '''
    
    # Handles different text encoding 
    email_text = ''
    receiver = ''
    sender = ''
    cc = ''
    subject = ''
    body_text = ''

    
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            fp = codecs.open(file_path, 'r', body_charset)
            email_text = fp.read()
            email_text = email_text.encode('UTF-8') # encodes to UNICODE 
            fp.close()
        except UnicodeError: pass
        else: break

    if email_text == '': 
    
        msg = email.message_from_string(email_text)  
        receiver = xstr(msg['to'])
        sender = xstr(msg['from'])
        cc = xstr(msg['cc'])
        subject = xstr(msg['subject'])
        body_text = msg.get_payload()
        body_text = ' '.join(body_text.split())  # removes newline, tab, and white space 
        
    
    return (receiver, sender, cc, subject, body_text)
    

