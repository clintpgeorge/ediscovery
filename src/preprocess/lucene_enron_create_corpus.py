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
from lucene import SimpleFSDirectory, File, initVM, IndexReader
from utils.utils_email import whitespace_tokenize
from lucenesearch.lucene_index_dir import MetadataType 


def _store_file_paths_index(index_reader, paths_index_file): 
    '''
    Stores the file paths into a text file 
    
    '''
    with open(paths_index_file, 'w') as fw: 
        for i in range(0, index_reader.maxDoc()):
            doc = index_reader.document(i)
            if doc is not None:
                file_id = doc.get(MetadataType.FILE_ID)
                file_path = doc.get(MetadataType.FILE_PATH)
                file_name = doc.get(MetadataType.FILE_NAME)
                fw.write(file_id + ";" + file_path.rstrip(file_name) + ";" + 
                         file_name + "\n")

    

def _process_doc(doc):
    '''Processes a single email file 
    
    Arguments: 
        doc - a Document in the Lucene index  
    '''
    tokens = []
    if doc is not None:
        all_text = doc.get(MetadataType.ALL)
        file_path = doc.get(MetadataType.FILE_PATH)
        if all_text is None:
            # file_name = doc.get(MetadataType.FILE_NAME)
            logging.error('%s does not have any contents.', file_path)
            tokens = []
        else:
            tokens = whitespace_tokenize(all_text) # regex_tokenizer(all_text)# 
        
    return tokens

def _create_dictionary(index_reader, dictionary_file, min_frequency, 
                       min_word_len, max_word_len):
    '''Creates a dictionary from the given text files using the Gensim class 
    and functions
    
    Returns:
        None 
    Arguments:
        index_reader - the lucene index reader 
        dictionary_file - the dictionary object file (output)
        MIN_FREQUENCY - min frequency of a valid vocabulary term 
        MIN_WORD_LENGTH - min word length of a valid vocabulary term 
    '''
    
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(_process_doc(index_reader.document(i)) 
                                    for i in range(0, index_reader.maxDoc()))
    
#     # remove stop words and words that appear only once
#     stoplist = load_en_stopwords(en_sw_file) # loads stop words 
#     stop_ids = [dictionary.token2id[stopword] for stopword in stoplist 
#                 if stopword in dictionary.token2id]
    
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() 
                if docfreq < min_frequency]
    sw_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() 
              if (len(dictionary[tokenid]) < min_word_len)]
    max_word_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() 
                    if (len(dictionary[tokenid]) > max_word_len)]
    
    dictionary.filter_tokens(once_ids + sw_ids + max_word_ids) 
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    dictionary.save(dictionary_file) # store the dictionary, for future reference
    
    logging.info(str(dictionary))


class _TextCorpus(object):
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
            tokens = _process_doc(self.index_reader.document(i)) 
            yield self.dictionary.doc2bow(tokens)


def build_lda_corpus(index_folder, paths_index_file,  
                     dictionary_file, ldac_file, min_frequency, 
                     min_word_len, max_word_len=20):
    '''
    The main function that does the job! 
    
    '''
    initVM()  
    store = SimpleFSDirectory(File(index_folder))
    index_reader = IndexReader.open(store)

    # Stores the file paths index (for LDA)
    _store_file_paths_index(index_reader, paths_index_file) 
    
    # Creates the dictionary 
    _create_dictionary(index_reader, dictionary_file, min_frequency, 
                       min_word_len, max_word_len)

    # Creates the corpus 
    dictionary = corpora.Dictionary().load(dictionary_file)      
    # doesn't load the corpus into the memory! 
    corpus_memory_friendly = _TextCorpus(dictionary, index_reader) 
    corpora.BleiCorpus.serialize(ldac_file, corpus_memory_friendly, 
                                 id2word=dictionary)
    
    logging.info('The Enron corpus building is completed.')
    
    
    



