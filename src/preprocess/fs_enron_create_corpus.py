#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os 
import logging
import argparse
import codecs
import email 
from gensim import corpora
from utils_email import punkt_word_tokenizer, load_en_stopwords


def process_msg(t, count):
    
    root, _, file_name = t
    logging.info('[#%d] file: %s' % (count, os.path.join(root, file_name)) )
    
    # Handles different text encoding 
    email_text = ''
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            fp = codecs.open(os.path.join(root, file_name), 'r', body_charset)
            email_text = fp.read()
            email_text = email_text.encode('UTF-8') # encodes to UNICODE 
            fp.close()
            logging.info('[#%d] file encoding: %s --> UTF-8' % (count, body_charset))    
        except UnicodeError: pass
        else: break
    if email_text == '': return []
    
    msg = email.message_from_string(email_text)  
    
    receiver = str(msg['to'])
    sender = str(msg['from'])
    cc = str(msg['cc'])
    if receiver is None and sender is None and cc is None: return []

#    body_text = ''
#    for part in msg.walk():
#        # each part is a either non-multipart, or another multipart message
#        # that contains further parts... Message is organized like a tree
#        if part.get_content_type() == 'text/plain':
#            body_text = quopri.decodestring(part.get_payload())
#    if body_text == '': return []
    body_text = msg.get_payload()
    lines = body_text.strip().split('\n')
    message_text =  ' '.join(line.strip() for line in lines if line.strip() <> '')
    
    tokens = punkt_word_tokenizer(message_text.lower())
    
    return tokens

def create_dictionary(en_sw_file, file_tuples, dictionary_file, MIN_FREQUENCY, MIN_WORD_LENGTH):
    
    # loads stop words 
    stoplist = load_en_stopwords(en_sw_file)
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(process_msg(ft, idx+1) for idx, ft in enumerate(file_tuples))
    
    # remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq < MIN_FREQUENCY]
    sw_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if (len(dictionary[tokenid]) < MIN_WORD_LENGTH)]
    
    dictionary.filter_tokens(stop_ids + once_ids + sw_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    dictionary.save(dictionary_file) # store the dictionary, for future reference
    
    logging.info(str(dictionary))


def get_file_info(mail_dir):
    file_tuples = []
    for root, dirs, files in os.walk(mail_dir): # Walk directory tree
        for f in files:
            file_tuples.append((root, dirs, f)) 
    return file_tuples


class TextCorpus(object):
    
    def __init__(self, _dictionary, _file_tuples):
        
        self.file_tuples = _file_tuples                
        self.dictionary = _dictionary
         
    def __iter__(self):

        for idx, ft in enumerate(self.file_tuples):
            tokens = process_msg(ft, idx+1)
            yield self.dictionary.doc2bow(tokens)






'''
The main function call 

Examples: 
    python fs_enron_create_corpus.py -h 
    python fs_enron_create_corpus.py -l -d /media/Store/Research/datasets/enron/maildir/

'''
if __name__=="__main__":
    
    arg_parser = argparse.ArgumentParser('Enron email topic modeling:')
    arg_parser.add_argument("-d", dest="directory", type=str, help="the root directory for all the mails", required=True)
    arg_parser.add_argument("-l", "--log", dest="log", default=False, action="store_true", help="log details into a log file (enron_insert_db.log)")
    arg_parser.add_argument("-w", dest="stop_words_file", type=str, help="Stop words file", default='en_stopwords')
    arg_parser.add_argument("-m", dest="min_frequency", type=int, help="Minimum frequency of vocabulary terms", default=15)
    arg_parser.add_argument("-i", dest="min_word_len", type=int, help="Minimum length of vocabulary terms", default=2)
    
    args = arg_parser.parse_args()

    # create file handler which 
    # logs even debug messages
    if args.log: 
        logging.basicConfig(filename='fs_enron_create_corpus.log', 
                            format='%(asctime)s : %(levelname)s : %(message)s', 
                            level=logging.DEBUG)
    else: 
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                            level=logging.DEBUG)
        
    
    
    logging.info('=============================================================================================================')
    
    logging.info('Email root directory: %s' % args.directory)
    
    logging.info('Loads email paths...')
    file_tuples = get_file_info(args.directory)
    logging.info('%d email documents found.' % len(file_tuples))
    
    dictionary_file = 'fs_enron.dict'
    ldac_file = 'fs_enron.ldac'
    email_paths = 'fs_enron.email_paths'
    
    # Stores the email paths into a text 
    # file for future reference 
    with open(email_paths, 'w') as fw:
        for idx, ft in enumerate(file_tuples): 
            root, _, file_name = ft
            print >>fw, idx, root, file_name
        
    
    
    # Creates the dictionary 
    create_dictionary(args.stop_words_file, file_tuples, dictionary_file, args.min_frequency, args.min_word_len)
    
    # Creates the corpus 
    dictionary = corpora.Dictionary().load(dictionary_file)       
    corpus_memory_friendly = TextCorpus(dictionary, file_tuples) # doesn't load the corpus into the memory!
    corpora.BleiCorpus.serialize(ldac_file, corpus_memory_friendly, id2word=dictionary)
    
    logging.info('The Enron corpus building is completed.')
    
    logging.info('=============================================================================================================')



