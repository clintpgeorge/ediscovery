#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script is used to parse the enron emails 
in the plain text format and create an LDA 
corpus from them. 

Created by: Clint P. George
Created On: Jan 12, 2013   

'''

import os 
import logging

from gensim import corpora
from utils.utils_email import punkt_word_tokenizer, load_en_stopwords, parse_plain_text_email
from utils.utils_file import get_file_paths_index, load_file_paths_index, store_file_paths_index

def process_msg(file_path_tuple):
    '''Processes a single email file 
    
    Arguments: 
        file_path_tuple - a tuple of (idx, root, file_name) 
    '''
    
    (idx, root, file_name)  = file_path_tuple
    logging.info('[#%d] file: %s' % (idx, os.path.join(root, file_name)) )
    
    
    _, _, _, _, body_text = parse_plain_text_email(os.path.join(root, file_name))
    tokens = punkt_word_tokenizer(body_text.lower())
    
    return tokens

def create_dictionary(en_sw_file, file_tuples, dictionary_file, MIN_FREQUENCY, MIN_WORD_LENGTH):
    '''Creates a dictionary from the given text files using the Gensim class and functions
    
    Returns:
        None 
    Arguments:
        en_sw_file - stopwords file 
        file_tuples - list of file details 
        dictionary_file - the dictionary object file (output)
        MIN_FREQUENCY - min frequency of a valid vocabulary term 
        MIN_WORD_LENGTH - min word length of a valid vocabulary term 
    '''
    
    # loads stop words 
    stoplist = load_en_stopwords(en_sw_file)
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(process_msg(ft) for ft in file_tuples)
    
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
        _file_tuples - a list of file details (idx, root, file_name) 
    '''
    
    def __init__(self, _dictionary, _file_tuples):
        
        self.file_tuples = _file_tuples                
        self.dictionary = _dictionary
         
    def __iter__(self):

        for ft in self.file_tuples:
            tokens = process_msg(ft)
            yield self.dictionary.doc2bow(tokens)


def build_lda_corpus(data_folder, path_index_file, stop_words_file, dictionary_file, ldac_file, min_frequency, min_word_len):
    '''
    The main function that does the job! 
    
    '''
    
    if os.path.exists(path_index_file): 
        logging.info('Loading file paths index...')
        file_tuples = load_file_paths_index(path_index_file)
        logging.info('%d files found in the index.' % len(file_tuples))
    else: 
        logging.info('Loading files in the data folder %s...' % data_folder)
        file_tuples = get_file_paths_index(data_folder)
        logging.info('%d email documents found.' % len(file_tuples))

        store_file_paths_index(path_index_file, file_tuples)
        logging.info('File paths index is stored into %s' % path_index_file)

    
    # Creates the dictionary 
    create_dictionary(stop_words_file, file_tuples, dictionary_file, min_frequency, min_word_len)
    
    # Creates the corpus 
    dictionary = corpora.Dictionary().load(dictionary_file)       
    corpus_memory_friendly = TextCorpus(dictionary, file_tuples) # doesn't load the corpus into the memory!
    corpora.BleiCorpus.serialize(ldac_file, corpus_memory_friendly, id2word=dictionary)
    
    logging.info('The Enron corpus building is completed.')
    
    
    



