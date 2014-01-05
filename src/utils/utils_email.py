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
from nltk.tokenize import PunktWordTokenizer, RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import SnowballStemmer


'''
Global variables 
'''
DATE_FORMAT = "%a,%d %m %y %H:%M:%S -T (Z)"
STRIP_CHAR_LIST = [u'_', u'-', u',', u'!', u':', u'.', u'?', 
                   u';', u'=', u'…', u'•', u'–', u'¿', u'¡', 
                   u'º', u'ª', u'«', u'»', u'*', u'~', u'`', 
                   u':', u'<', u'>', u'{', u'}',
                   u'[', u']', u'//', u'(', u')'] 
REMOVE_LIST = [u"[", u"]", u"{", u"}", u"(", u")", u"'", u".", 
               u"..", u"...", u",", u"?", u"!", u"/", u"\"", 
               u"\"", u";", u":", u"-", u"`", u"~", u"@", u"$", 
               u"^", u"|", u"#", u"=", u"*"];

numeric_parser = re.compile(r"""        # A numeric string consists of:
    (?P<sign>[-+])?              # an optional sign, followed by either...
    (
        (?=\d|\.\d)              # ...a number (with at least one digit)
        (?P<int>\d*)             # having a (possibly empty) integer part
        (\.(?P<frac>\d*))?       # followed by an optional fractional part
        (E(?P<exp>[-+]?\d+))?    # followed by an optional exponent, or...
    |
        Inf(inity)?              # ...an infinity, or...
    |
        (?P<signal>s)?           # ...an (optionally signaling)
        NaN                      # NaN
        (?P<diag>\d*)            # with (possibly empty) diagnostic info.
    )
    \Z
""", re.VERBOSE | re.IGNORECASE | re.UNICODE).match
    
date_parser = re.compile(r'''(\d{2})[/.-](\d{2})[/.-](\d{4})$''',
                         re.VERBOSE | re.IGNORECASE | re.UNICODE).match
time_parser = re.compile(r'''(\d{2}):(\d{2}):(\d{2})$''',
                         re.VERBOSE | re.IGNORECASE | re.UNICODE).match
time_parser2 = re.compile(r'''(\d{2}):(\d{2})$''',
                         re.VERBOSE | re.IGNORECASE | re.UNICODE).match
'''
Initializes the tokenizer, lemmatizer, and stemmer  
'''
# Manages real numbers, numbers with comma separators, 
# dates, times, hyphenated words, email addresses, urls 
# and abbreviations
# https://code.google.com/p/nltk/issues/detail?id=128
pat1 = r'''(?:[A-Z][.])+|\d[\d,.:\-/\d]*\d|\w+[\w\-\'.&|@:/]*\w+'''

pat2 = r'''\w+|\$[\d\.]+|\S+'''

# https://code.google.com/p/nltk/issues/detail?id=128
pat3 = r'''(?x)    # set flag to allow verbose regexps
        ([A-Z]\.)+        # abbreviations, e.g. U.S.A. 
        | \w+(-\w+)*        # words with optional internal hyphens
        | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
        | \.\.\.            # ellipsis
        | [][.,;"'?():-_`]  # these are separate tokens
        '''

regx_tokenizer = RegexpTokenizer(pat1)

punkt_tokenizer = PunktWordTokenizer()
wordnet_lmtzr = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer("english") # Choose a language

def xstr(s):
    return '' if s is None else str(s)


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

stop_words = load_en_stopwords('en_stopwords')
print 'Number of stop words:', len(stop_words)

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

        # It's commented because it will remove slashes in a URL 
        # token = re.sub('[\(\)\{\}\[\]\'\"\\\/*<>|]', '', token) 

        for each_char in STRIP_CHAR_LIST:
            token = token.strip(each_char)
        
        if ((token in REMOVE_LIST) # removes if it's in the remove list 
            or (token in stop_words) # removes stop words  
            or numeric_parser(token) # discards if it's a numeric 
            or date_parser(token) # discards if it's a date  
            or time_parser(token) or time_parser2(token)): # discards if it's a time   
            return ''

    except: 
        return '' 
    
    return token.strip()

def regex_tokenizer(text):
    '''A tokenizer based on NLTK's RegexpTokenizer 
    
    Returns: 
        a list of tokens 
    Arguments:
        a string to tokenized 
    
    '''
#    try: 
#        text = ' '.join(text.lower().split()) # removes newline, tab, and white space
#    except Exception:
#        pass  
          
    tokens = regx_tokenizer.tokenize(text)

    filtered = []
    for w in tokens:
        try:
            token = cleanup(w.lower()) 
            if len(token) > 0: 
                filtered.append(token)
        except: pass 

    return filtered

   
   
def punkt_word_tokenizer(text):
    '''A tokenizer based on NLTK's PunktWordTokenizer 
    
    Returns: 
        a list of tokens 
    Arguments:
        a string to tokenized 
    
    '''
    try: 
        text = ' '.join(text.lower().split()) # removes newline, tab, and white space
    except Exception:
        pass  
          
    tokens = punkt_tokenizer.tokenize(text)
    
    print tokens 
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

 

def __strip_email_footer(email_text):
    '''
    Removes the email footer text and the following lines 
    from the email body 
    
    TODO: It's highly specific to the TREC 2010 Enron email 
    dataset. It may not work for other datasets.  
    ''' 
    def __is_email_footer(line):
        ret = False  
        for l in ['***********', 'EDRM Enron Email Data Set has been produced in EML']:
            if line.startswith(l): 
                return True  
        return ret
    
    
    cnt = 0
    cleaned_lines = []
    for line in email_text.split('\n'): # Gets each line 
        if cnt > 2: 
            break # ignores all the text after the 3 footer lines 
        elif __is_email_footer(line): 
            cnt += 1 # increments the footer line count 
        else: 
            cnt = 0 # resets to zero 
            cleaned_lines.append(line)            
    
    stripped_text = '\n'.join(cleaned_lines)
    
    return stripped_text


def __strip_email_header_fields(body_text):
    
    cleaned_body = []
    for line in body_text.split("\n"):
        for header_field in ['to:', 'from:', 'subject:', 'date:', 'cc:', 'bcc:', 're:']:
            if line.lower().startswith(header_field):
                line = line[len(header_field):]
                break 
        cleaned_body.append(line)
    
    return '\n'.join(cleaned_body)
        
    
     

def parse_plain_text_email(file_path, tokenize = True, 
                           lemmatize = False, stem = False, 
                           nonascii = True, 
                           text_tokenizer=regex_tokenizer):
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

    email_text = __strip_email_footer(email_text)
  

    if len(email_text) > 0: 
    
        msg = email.message_from_string(email_text)  
        receiver = xstr(msg['to'])
        sender = xstr(msg['from'])
        cc = xstr(msg['cc'])
        bcc = xstr(msg['bcc']) # Subodh - Rahul - Get BCC attribute from the email 
        subject = xstr(msg['subject'])
        date = xstr(msg['date'])
        body_text = str(msg.get_payload())

        body_text = __strip_email_header_fields(body_text) 

        if tokenize:
            body_tokens = text_tokenizer(body_text)
            if lemmatize: 
                body_tokens = lemmatize_tokens(body_tokens)
            if stem: 
                body_tokens = stem_tokens(body_tokens)
            
            # This is added to remove stop words after normalization  
            if lemmatize or stem:
                body_tokens = [w for w in body_tokens if len(cleanup(w)) > 0]
            
            if body_charset == 'ISO-8859-1':
                body_text = ''
                for ch in body_tokens:
                    try:
                        token = ch.decode('ascii')
                        body_text += ' ' + token
                    except UnicodeDecodeError:
                        pass
            else:
                try:
                    body_text = ' '.join(body_tokens)
                except Exception:
                    pass

        else:
            # If message is multi-part, we only want the text version of 
            # the body, this walks the message and gets the body.
            if msg.get_content_maintype() == 'multipart': 
                for part in msg.walk():       
                    if part.get_content_type() == "text/plain":
                        body_text += part.get_payload(decode=True)

        
        email_text = ' '.join(text_tokenizer(' '.join([receiver, sender, cc, bcc, subject])))
        email_text += ' ' + body_text
        
    
    if not nonascii:            
        ret = (removeNonAscii(receiver), 
                removeNonAscii(sender), 
                removeNonAscii(cc), 
                removeNonAscii(subject), 
                removeNonAscii(body_text), 
                removeNonAscii(bcc), 
                removeNonAscii(date),
                removeNonAscii(email_text))
    else: 
        ret = (receiver, sender, cc, subject, body_text, bcc, date, email_text)
    
    return ret
    
if __name__ == '__main__':
    
    file_path = 'C:\\Users\\Clint\\SMARTeR\\prj-207-re-30t\\files\\1\\3.546995.DXMALIWB1YBIEAJKZ00OSLZ2QXCTTNB1B.txt'
    ret = parse_plain_text_email(file_path)
    print ret[4] 
    print ret[7] 
    

#    file_path = 'C:\\Users\\Clint\\SMARTeR\\prj-207\\files\\0\\3.181161.OPMT5EU0PZGZEDI4MHNK4P5KDX551MJEB.txt'
#    ret = parse_plain_text_email(file_path)
#    print ret[4] 
    
#    text = '''
#    abbreviations: U.S.A., eg., AT&T
#    possessives: John's, Lars'
#    contractions: that's, it's, that'll, I've, couldn't 
#    diacritics: non-english languages may have apostrophes as diacritics
#    hyphenated words: low-budget, pre-owned
#    email addresses: foo.bar@baz.com
#    urls: http://www.foo.com
#    foreign phrases: et cetera
#    
#    units:
#    real numbers/ measures: 1,210,234.3245, 2.3, 2.3 kgs.
#    currencies: $ 4.5, $ 150,000, AU$ 6.7, 67 AUD
#    date: 29/01/2009, 29-01-2009, and various other date formats
#    time: 2:30 pm., 2.30 pm.
#    
#    http://stackoverflow.com/questions/5214177/regex-tokenizer-to-split-a-text-into-words-digits-and-punctuation-marks
#    https://code.google.com/p/nltk/issues/detail?id=128
#    https://www.google.com/search?q=nltk.word_tokenize()&rlz=1C1_____enUS391US391&oq=nltk.word_tokenize()&aqs=chrome..69i57&sourceid=chrome&espv=210&es_sm=122&ie=UTF-8
#    
#    '''
#    
#    print regx_tokenizer.tokenize(text)

    
    
    
