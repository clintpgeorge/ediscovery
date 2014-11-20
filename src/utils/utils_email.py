#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script has all the utility functions for 
processing the enron email data set  

Created by: Clint P. George
Created On: Jan 29, 2013   

'''
import sys
import quopri
import codecs
import email 
import locale
from nltk.tokenize import PunktWordTokenizer, RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from dateutil import parser
from fractions import Fraction


locale.setlocale(locale.LC_NUMERIC, 'US')



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
# Updated on June 26, 2014 
pat4 = r'''(?x)                    # set flag to allow verbose regexps
        ([A-Z]\.)+                 # abbreviations, e.g. U.S.A. 
        | \d[\d,.:\-/\d]*\d        # currency and percentages, e.g. $12.40, 82%
        | \w+[\w\-_\.&|@:/]*\w+    # words with optional internal hyphens
        | \.\.\.                   # ellipsis
        | [][.,;"'?():-_`]         # these are separate tokens
        '''


regx_tokenizer = RegexpTokenizer(pat1)

punkt_tokenizer = PunktWordTokenizer()
wordnet_lmtzr = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer("english") # Choose a language

def xstr(s):
    return '' if s is None else str(s)

def is_date(token):
    try:
        parser.parse(token)
    except:
        return False
    return True 

def is_numeric(num_str):
    try:
        float(num_str)
        return True 
    except ValueError:
        try:
            locale.atof(num_str)
            return True 
        except ValueError:
            try:
                float(Fraction(num_str))
                return True 
            except ValueError:
                return False  

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
# print 'Number of stop words:', len(stop_words)

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
            if token.endswith(u"'s"): token = token.rstrip(u"'s")            
        
        if ((token in REMOVE_LIST) # removes if it's in the remove list 
            or (token in stop_words) # removes stop words  
            or is_date(token) # discards if it's a date  
            or is_numeric(token)): # discards if it's a numeric
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

    cleaned_tokens = []
    for w in tokens:
        try: token = cleanup(w.lower()) 
        except: token = u"" 
        if len(token) > 0: cleaned_tokens.append(token)

    return cleaned_tokens

   
   
def punkt_word_tokenizer(text):
    '''A tokenizer based on NLTK's PunktWordTokenizer 
    
    Returns: 
        a list of tokens 
    Arguments:
        a string to tokenized 
    
    '''
    try: text = ' '.join(text.lower().split()) 
    except Exception: pass  
    tokens = punkt_tokenizer.tokenize(text)
    
    cleaned_tokens = []
    for w in tokens:
        try: token = cleanup(w.lower()) 
        except: pass 
        if len(token) > 0: 
            for wt in token.split(','): 
                cleaned_tokens.append(wt)

    return cleaned_tokens


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
        try: token = wordnet_lmtzr.lemmatize(token)
        except: pass 
        tokens.append(token)
    return tokens


def stem_tokens(word_tokens):
    '''
    Stem tokens based on Snowball stemmer  
    '''
    tokens = [] 
    for token in word_tokens:
        try: token = snowball_stemmer.stem(token)
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
        for l in ['***********', 
                  'EDRM Enron Email Data Set has been produced in EML']:
            if line.startswith(l): 
                return True  
        return ret
    
    
    cnt = 0
#     cleaned_lines = []
    stripped_text = ''
    for line in email_text.split('\n'): # Gets each line 
        if cnt > 2: 
            break # ignores all the text after the 3 footer lines 
        elif __is_email_footer(line): 
            cnt += 1 # increments the footer line count 
        else: 
            cnt = 0 # resets to zero 
            stripped_text += line + '\n'
#             cleaned_lines.append(line)            
#     
#     stripped_text = u'\n'.join(cleaned_lines)
    
    return stripped_text


def __strip_email_header_fields(body_text):
    
    cleaned_body = []
    for line in body_text.split(u'\n'):
        for header_field in ['to:', 'from:', 'subject:', 'date:', 'cc:', 
                             'bcc:', 're:']:
            if line.lower().startswith(header_field):
                line = line[len(header_field):]
                break 
        cleaned_body.append(line)
    
    return u'\n'.join(cleaned_body)
        
def parse_text_emails_and_attachments(file_path, file_type="E"):
    '''Reads a given email or attachment which is in plain text format  
    
    Arguments: 
        file_path - the email or attachment file path
        file_type - [E] - email and [A] - attachment   
    '''
    doc_text = u''
    receiver = u''
    sender = u''
    cc = u''
    bcc = u''
    subject = u''
    body_text = u''
    date = u''
    
    try:
        with codecs.open(file_path, 'r', encoding='ascii', 
                         errors='ignore') as fp: 
            doc_text = fp.read()

        if file_type == "E": # if it's an email 
            doc_text = __strip_email_footer(doc_text) 
            msg = email.message_from_string(doc_text)  
            receiver = xstr(msg['to'])
            sender = xstr(msg['from'])
            cc = xstr(msg['cc'])
            bcc = xstr(msg['bcc']) # Subodh - Rahul - Get BCC attribute from the email 
            subject = xstr(msg['subject'])
            date = xstr(msg['date'])
            if msg.is_multipart(): 
                body_text = ' '.join(str(w) for w in msg.get_payload())
            else: 
                body_text = msg.get_payload()
            doc_text = ' '.join([receiver, sender, cc, bcc, subject])
            doc_text += ' ' + body_text
    except UnicodeError as ue: 
        print "Unicode error({0}): {1}".format(ue.errno, ue.strerror)
        pass 
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    
    return (receiver, sender, cc, subject, body_text, bcc, date, doc_text)

    
# def parse_plain_text_email2(file_path, lemmatize=False, stem=False, 
#                             text_tokenizer=regex_tokenizer, file_type="E"):
#     '''Processes a single email file that's in plain/text format 
#     
#     Arguments: 
#         file_path - the email file path 
#     '''
#     
#     # Handles different text encoding 
#     doc_text = u''
#     receiver = u''
#     sender = u''
#     cc = u''
#     bcc = u''
#     subject = u''
#     body_text = u''
#     date = u''
#     
#     try:
#         with codecs.open(file_path, 'r', encoding='ascii', 
#                          errors='ignore') as fp: 
#             doc_text = fp.read()
# 
#         if file_type == "E": # if it's an email 
#             doc_text = __strip_email_footer(doc_text) 
#             msg = email.message_from_string(doc_text)  
#             receiver = xstr(msg['to'])
#             sender = xstr(msg['from'])
#             cc = xstr(msg['cc'])
#             bcc = xstr(msg['bcc']) # Subodh - Rahul - Get BCC attribute from the email 
#             subject = xstr(msg['subject'])
#             date = xstr(msg['date'])
#             
#             if msg.is_multipart(): 
#                 body_text = u' '.join(str(w) for w in msg.get_payload())
#             else: 
#                 body_text = msg.get_payload()
#             body_tokens = text_tokenizer(body_text)
#             
#             if lemmatize: body_tokens = lemmatize_tokens(body_tokens)
#             if stem: body_tokens = stem_tokens(body_tokens)
#             
#             body_text = u' '.join(body_tokens)
#     
#             doc_text = u' '.join(text_tokenizer(u' '.join([receiver, sender, 
#                                                            cc, bcc, subject])))
#             doc_text += u' ' + body_text
#         else: # if it's an attachment 
#             body_tokens = text_tokenizer(doc_text)            
#             if lemmatize: body_tokens = lemmatize_tokens(body_tokens)
#             if stem: body_tokens = stem_tokens(body_tokens)
#     
#             doc_text = u' '.join(body_tokens)
#         
#     except UnicodeError as ue: 
#         print "Unicode error({0}): {1}".format(ue.errno, ue.strerror)
#         pass 
#     except:
#         print "Unexpected error:", sys.exc_info()[0]
#         raise
#     
#     return (receiver, sender, cc, subject, body_text, bcc, date, doc_text)
#   



def parse_plain_text_email(file_path, lemmatize=False, stem=False, 
                           nonascii=True, text_tokenizer=regex_tokenizer, 
                           file_type="E"):
    '''Processes a single email file that's in plain/text format 
    
    Arguments: 
        file_path - the email file path 
    '''
    def remove_non_ascii(s): 
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

    
    if file_type == "E": # if it's an email 

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
    
    #         if tokenize:
            body_tokens = text_tokenizer(body_text)
            
            if lemmatize: body_tokens = lemmatize_tokens(body_tokens)
            if stem: body_tokens = stem_tokens(body_tokens)
            
            # This is added to remove stop words after normalization  
            if lemmatize or stem:
                body_tokens = [w for w in body_tokens if len(cleanup(w)) > 0]
            
            body_text = ''
            if body_charset == 'ISO-8859-1':
                for ch in body_tokens:
                    try:
                        token = ch.decode('ascii')
                        body_text += ' ' + token
                    except UnicodeDecodeError:
                        pass
            else:
                try: body_text = ' '.join(body_tokens)
                except Exception: pass
    
    #         else:
    #             # If message is multi-part, we only want the text version of 
    #             # the body, this walks the message and gets the body.
    #             if msg.get_content_maintype() == 'multipart': 
    #                 for part in msg.walk():       
    #                     if part.get_content_type() == "text/plain":
    #                         body_text += part.get_payload(decode=True)
    
            
            email_text = ' '.join(text_tokenizer(' '.join([receiver, sender, 
                                                           cc, bcc, subject])))
            email_text += ' ' + body_text
        
        body_text = body_text.strip()
        email_text = email_text.strip()
        
        if not nonascii:            
            ret = (remove_non_ascii(receiver), 
                    remove_non_ascii(sender), 
                    remove_non_ascii(cc), 
                    remove_non_ascii(subject), 
                    remove_non_ascii(body_text), 
                    remove_non_ascii(bcc), 
                    remove_non_ascii(date),
                    remove_non_ascii(email_text))
        else: 
            ret = (receiver, sender, cc, subject, body_text, bcc, date, 
                   email_text)
    
    else: # if it's an attachment 
        
        body_tokens = text_tokenizer(email_text)
            
        if lemmatize: body_tokens = lemmatize_tokens(body_tokens)
        if stem: body_tokens = stem_tokens(body_tokens)
        
        # This is added to remove stop words after normalization  
        if lemmatize or stem:
            body_tokens = [w for w in body_tokens if len(cleanup(w)) > 0]
        
        email_text = ''
        if body_charset == 'ISO-8859-1':
            for ch in body_tokens:
                try:
                    token = ch.decode('ascii')
                    email_text += ' ' + token
                except UnicodeDecodeError: pass
        else:
            try: email_text = ' '.join(body_tokens)
            except Exception: pass
            
        if not nonascii: email_text = remove_non_ascii(email_text)
        ret = (receiver, sender, cc, subject, body_text, bcc, date, email_text)

    return ret
    
# if __name__ == '__main__':
#     
#     file_path = 'E:\\E-Discovery\\trec2010dataset\\seeds-a\\201\\1\\3.215558.MUQRZJDAZEC5GAZM0JG5K2HCKBZQA1TEB.1.txt'
#     (receiver, sender, cc, subject, body_text, bcc, date, 
#      email_text) = parse_plain_text_email(file_path, True, True, True, False)
#     print body_text 
    
