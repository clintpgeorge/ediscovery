#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script is used to parse the enron emails 
in the palin text format (stored in the database) 
and create an LDA corpus from them. 

Created by: Clint P. George
Created On: Jan 29, 2013   

'''

import psycopg2
import logging
import argparse

from gensim import corpora
from utils_email import punkt_word_tokenizer, load_en_stopwords

'''
DB access functions 
'''

def get_message_ids():
    '''Loads message ids from 
    the enron database 
    
    Returns: 
        a list of message ids 
    '''
    mids = [] 
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("SELECT mid FROM messages;")
    records = cursor.fetchall()
    for record in records: 
        mids.append(int(record[0]))
    cursor.close()
    conn.close()
    return mids 

def process_msg(mid):
    '''Processes a single email file 
    
    Arguments: 
        mid - the email uid from the database 
    '''
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("SELECT body FROM messages where mid = %d;" % mid)
    record = cursor.fetchone()
    cursor.close()
    conn.close()
 
    tokens = punkt_word_tokenizer(str(record[0]))
    return tokens


'''
Corpus building functions 
'''

def create_dictionary(en_sw_file, msg_ids, dictionary_file, MIN_FREQUENCY, MIN_WORD_LENGTH):
    '''Creates a dictionary from the given text files using the Gensim class and functions
    
    Returns:
        None 
    Arguments:
        en_sw_file - stopwords file 
        msg_ids - list of message ids 
        dictionary_file - the dictionary object file (output)
        MIN_FREQUENCY - min frequency of a valid vocabulary term 
        MIN_WORD_LENGTH - min word length of a valid vocabulary term 
    '''
    # loads stop words 
    stoplist = load_en_stopwords(en_sw_file)
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(process_msg(mid) for mid in msg_ids)
    
    # remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq < MIN_FREQUENCY]
    sw_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if (len(dictionary[tokenid]) < MIN_WORD_LENGTH)]
    
    dictionary.filter_tokens(stop_ids + once_ids + sw_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    dictionary.save(dictionary_file) # store the dictionary, for future reference
    
    logging.info(str(dictionary))


class TextCorpus(object):
    '''The text corpus class 
    
    Returns: 
        a corpus object 
    Arguments: 
        _dictionary - a dictionary object 
        _msg_ids - a list of message ids 
    '''
    def __init__(self, _dictionary, _msg_ids):
        
        self.msg_ids = _msg_ids                
        self.dictionary = _dictionary
         
    def __iter__(self):

        for mid in self.msg_ids:
            tokens = process_msg(mid)
            yield self.dictionary.doc2bow(tokens)






'''
The main function call 

Examples: 
    python test.py -h 
    python test.py -l -s localhost -n enron -u eduser -p eddb13

'''
if __name__=="__main__":
    
    arg_parser = argparse.ArgumentParser('Enron email topic modeling:')
    # arg_parser.add_argument("-d", dest="directory", type=str, help="the root directory for all the mails", required=True)
    arg_parser.add_argument("-l", "--log", dest="log", default=False, action="store_true", help="log details into a log file (enron_insert_db.log)")
    arg_parser.add_argument("-s", dest="host", type=str, help="db server address", required=True)
    arg_parser.add_argument("-n", dest="dbname", type=str, help="db name", required=True)
    arg_parser.add_argument("-u", dest="user", type=str, help="db user name", required=True)
    arg_parser.add_argument("-p", dest="password", type=str, help="db user login password", required=True)
    arg_parser.add_argument("-w", dest="stop_words_file", type=str, help="Stop words file", default='en_stopwords')
    arg_parser.add_argument("-m", dest="min_frequency", type=int, help="Minimum frequency of vocabulary terms", default=10)
    arg_parser.add_argument("-i", dest="min_word_len", type=int, help="Minimum length of vocabulary terms", default=2)
    
    output_folder = arg_parser.parse_args()
    
    
    
    # Sets connection string from arguments 
    CONNECTION_STRING = "host='%s' dbname='%s' user='%s' password='%s'" % (output_folder.host, output_folder.dbname, output_folder.user, output_folder.password)
    

    # create file handler which 
    # logs even debug messages
    if output_folder.log: 
        logging.basicConfig(filename='db_enron_create_corpus.log', 
                            format='%(asctime)s : %(levelname)s : %(message)s', 
                            level=logging.DEBUG)
    else: 
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                            level=logging.DEBUG)

    
    
    logging.info('=============================================================================================================')
    
    mids =  get_message_ids()
    logging.info('Enron email message ids are loaded into memory. %d messages found.' % len(mids))
    
    dictionary_file = 'enron.dict'
    ldac_file = 'enron.ldac'
    
    # Creates the dictionary 
    create_dictionary(output_folder.stop_words_file, mids, dictionary_file, output_folder.min_frequency, output_folder.min_word_len)
    
    # Creates the corpus 
    dictionary = corpora.Dictionary().load(dictionary_file)       
    corpus_memory_friendly = TextCorpus(dictionary, mids) # doesn't load the corpus into the memory!
    corpora.BleiCorpus.serialize(ldac_file, corpus_memory_friendly, id2word=dictionary)
    
    logging.info('The Enron corpus building is completed.')
    
    logging.info('=============================================================================================================')



