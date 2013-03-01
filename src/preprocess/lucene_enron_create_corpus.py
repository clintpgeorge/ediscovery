#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script is used to parse the enron email  
body text stored in Lucene index and create an LDA 
corpus from them. 

Created by: Clint P. George
Created On: Feb 28, 2013   

'''

import logging
from gensim import corpora
from lucene import SimpleFSDirectory, File, initVM, Version, IndexReader
from utils.utils_email import load_en_stopwords
from lucenesearch.lucene_index_dir import MetadataType 


def store_file_paths_index(index_reader, paths_index_file): 
    with open(paths_index_file, 'w') as fw: 
        for i in range(0, index_reader.maxDoc()):
            doc = index_reader.document(i)
            if doc is not None:
                file_id = doc.get(MetadataType.FILE_ID)
                file_path = doc.get(MetadataType.FILE_PATH)
                file_name = doc.get(MetadataType.FILE_NAME)
                print >>fw, file_id, file_path.rstrip(file_path), file_name

    

def process_index_doc(doc):
    '''Processes a single email file 
    
    Arguments: 
        doc - a Document in the Lucene index  
    '''
    tokens = []
    if doc is not None:
        body_text = doc.get(MetadataType.EMAIL_BODY)
        tokens = body_text.split()
    return tokens

def create_dictionary(en_sw_file, index_reader, dictionary_file, MIN_FREQUENCY, MIN_WORD_LENGTH):
    '''Creates a dictionary from the given text files using the Gensim class and functions
    
    Returns:
        None 
    Arguments:
        en_sw_file - stopwords file 
        index_reader - the lucene index reader 
        dictionary_file - the dictionary object file (output)
        MIN_FREQUENCY - min frequency of a valid vocabulary term 
        MIN_WORD_LENGTH - min word length of a valid vocabulary term 
    '''
    
    # loads stop words 
    stoplist = load_en_stopwords(en_sw_file)
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(process_index_doc(index_reader.document(i)) for i in range(0, index_reader.maxDoc()))
    
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
        index_reader - the Lucene index reader object 
    '''
    
    def __init__(self, _dictionary, _index_reader):
        
        self.index_reader = _index_reader               
        self.dictionary = _dictionary
         
    def __iter__(self):

        for i in range(0, self.index_reader.maxDoc()):
            tokens = process_index_doc(self.index_reader.document(i)) 
            yield self.dictionary.doc2bow(tokens)


def build_lda_corpus(index_folder, paths_index_file, stop_words_file, dictionary_file, ldac_file, min_frequency, min_word_len):
    '''
    The main function that does the job! 
    
    '''
    
    '''
    The analyzer used for both indexing and searching  
    '''
    initVM()  
    store = SimpleFSDirectory(File(index_folder))
    index_reader = IndexReader.open(store)
    # Stores the file paths index (for LDA)
    # TODO: need to find out whether this can be 
    # avoided with the help of Lucene index  
    store_file_paths_index(index_reader, paths_index_file) 
    
    # Creates the dictionary 
    create_dictionary(stop_words_file, index_reader, dictionary_file, min_frequency, min_word_len)
    
    # Creates the corpus 
    dictionary = corpora.Dictionary().load(dictionary_file)       
    corpus_memory_friendly = TextCorpus(dictionary, index_reader) # doesn't load the corpus into the memory!
    corpora.BleiCorpus.serialize(ldac_file, corpus_memory_friendly, id2word=dictionary)
    
    logging.info('The Enron corpus building is completed.')
    
    
    



