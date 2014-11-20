#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script is used to parse the enron email  
body text stored in Lucene index and create an LDA 
corpus from them. 

Created by: Sahil Puri
Created On: Apr 8, 2014   

'''
import logging
from gensim import corpora
from whoosh import index
from utils.utils_email import whitespace_tokenize
from utils.utils_email import stop_words, pat4
from whoosh.analysis import StemmingAnalyzer, StandardAnalyzer

 
def store_file_paths_index(index_reader, paths_index_file): # TODO: update based on utils_file
    with open(paths_index_file, 'w') as fw:
        for doc in index_reader.iter_docs():
            file_id = doc[1]['file_id']
            file_path = doc[1]['file_path']
            file_name = doc[1]['file_name']
            fw.write(str(file_id) + ";" + file_path.rstrip(file_name) + ";" 
                     + file_name + "\n")
        
def process_index_doc(doc):
    '''Processes a single email file 
    
    Arguments: 
        doc - a Document in the Lucene index  
    '''
    tokens = []
    if doc is not None:
        all_text = doc['all']
        file_path = doc['file_path']
        if all_text is None:
            logging.error('%s does not have any contents.', file_path)
            tokens = []
        else:
            tokens = whitespace_tokenize(all_text) # regex_tokenizer(all_text)
        
    return tokens

def process_index_doc2(doc, analyzer):
    '''Processes a single email file 
    
    Arguments: 
        doc - a Document in the Lucene index  
    '''
    tokens = []
    if doc is not None:
        all_text = doc['all']
        file_path = doc['file_path']
        if all_text is None:
            logging.error('%s is empty.', file_path)
            tokens = []
        else:
            tokens = [token.text for token in analyzer(all_text)]
        
    return tokens

def create_dictionary(index_reader, dictionary_file, min_token_freq, 
                      min_token_len, max_token_len):
    '''
    Creates a dictionary from the given text files using the Gensim class 
    and functions
    
    Returns:
        None 
    Arguments:
        index_reader - the Whoosh index reader 
        dictionary_file - the dictionary object file (output)
        min_token_freq - min frequency of a valid vocabulary term 
        min_token_len - min word length of a valid vocabulary term 
        max_token_len - min word length of a valid vocabulary term 
    '''
    
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(process_index_doc(doc[1]) 
                                    for doc in index_reader.iter_docs())
    # remove stop words and words that appear only once
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() 
                if docfreq < min_token_freq]
    sw_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() 
              if (len(dictionary[tokenid]) < min_token_len)]
    max_word_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() 
                    if (len(dictionary[tokenid]) > max_token_len)]
    
    # remove stop words and words that appear only once
    dictionary.filter_tokens(once_ids + sw_ids + max_word_ids) 
    # remove gaps in id sequence after words that were removed
    dictionary.compactify() 
    # store the dictionary, for future reference
    dictionary.save(dictionary_file) 

    logging.info(str(dictionary))


def create_dictionary2(index_reader, dictionary_file, min_token_freq, 
                       analyzer):
    '''
    Creates a dictionary from the given text files using the Gensim class 
    and functions
    
    Returns:
        None 
    Arguments:
        index_reader - the Whoosh index reader 
        dictionary_file - the dictionary object file (output)
        min_token_freq - min frequency of a valid vocabulary term 
        analyzer - the Whoosh analyzer 
    '''
    
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(process_index_doc2(doc[1], analyzer) 
                                    for doc in index_reader.iter_docs())
    
    # remove stop words and words that appear only once
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() 
                if docfreq < min_token_freq]
    dictionary.filter_tokens(once_ids) 
    # remove gaps in id sequence after words that were removed
    dictionary.compactify() 
    # store the dictionary, for future reference
    dictionary.save(dictionary_file) 

    logging.info(str(dictionary))



class TextCorpus(object):
    '''The text corpus class. It doesn't load the corpus into the memory!
    
    Returns: 
        a corpus object 
    Arguments: 
        _dictionary - the dictionary object 
        _index_reader - the Whoosh index reader object 
    '''
    
    def __init__(self, _dictionary, _index_reader):
        
        self.index_reader = _index_reader               
        self.dictionary = _dictionary
         
    def __iter__(self):

        for doc in self.index_reader.iter_docs():
            tokens = process_index_doc(doc[1]) 
            yield self.dictionary.doc2bow(tokens)


class TextCorpus2(object):
    '''The text corpus class. It doesn't load the corpus into the memory!
    
    Returns: 
        a corpus object 
    Arguments: 
        _dictionary - the dictionary object 
        _index_reader - the Whoosh index reader object 
    '''
    
    def __init__(self, _dictionary, _index_reader, _analyzer):
        
        self.index_reader = _index_reader               
        self.dictionary = _dictionary
        self.analyzer = _analyzer
         
    def __iter__(self):

        for doc in self.index_reader.iter_docs():
            tokens = process_index_doc2(doc[1], self.analyzer) 
            yield self.dictionary.doc2bow(tokens)


def build_lda_corpus(index_folder, paths_index_file, dictionary_file, 
                     ldac_file, min_frequency, min_word_len, max_token_len):

    ix = index.open_dir(index_folder)
    index_reader = ix.reader()

    # Stores the file paths index (for LDA)
    store_file_paths_index(index_reader, paths_index_file) 
    
    # Creates the dictionary 
    create_dictionary(index_reader, dictionary_file, min_frequency, 
                      min_word_len, max_token_len)
    

    # Creates the corpus 
    dictionary = corpora.Dictionary().load(dictionary_file)       
    corpus_memory_friendly = TextCorpus(dictionary, index_reader) 
    corpora.BleiCorpus.serialize(ldac_file, corpus_memory_friendly, 
                                 id2word=dictionary)
    
    logging.info('The corpus building is completed.')
    
     
def build_lda_corpus2(index_folder, paths_index_file, dictionary_file, 
                     ldac_file, min_frequency, min_token_len, max_token_len, 
                     stem_tokens):
    if stem_tokens:
        analyzer = StemmingAnalyzer(expression=pat4, stoplist=stop_words, 
                                    minsize=min_token_len, 
                                    maxsize=max_token_len, 
                                    cachesize=-1)
    else: 
        analyzer = StandardAnalyzer(expression=pat4, stoplist=stop_words, 
                                    minsize=min_token_len, 
                                    maxsize=max_token_len)
    
    ix = index.open_dir(index_folder)
    index_reader = ix.reader()

    # Stores the file paths index (for LDA)
    store_file_paths_index(index_reader, paths_index_file) 
    
    # Creates the dictionary 
    create_dictionary2(index_reader, dictionary_file, min_frequency, analyzer)
    

    # Creates the corpus 
    dictionary = corpora.Dictionary().load(dictionary_file)       
    corpus_memory_friendly = TextCorpus2(dictionary, index_reader, analyzer) 
    corpora.BleiCorpus.serialize(ldac_file, corpus_memory_friendly, 
                                 id2word=dictionary)
    
    logging.info('The corpus building is completed.')