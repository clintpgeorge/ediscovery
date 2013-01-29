#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script process any given query in text format 
and finds similar documents from the learned 
LDA model.  

Created On: Jan 24, 2013 
Created By: Clint P. George 
'''

import logging, gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def load_docs_info(doc_paths_file):
    '''Loads the file paths from the given file 
    
    Returns: 
        a list of lists of file details such as [doc_id, doc_dir_path, doc_name] 
    Arguments:
        file name     
    '''
    fi = [] 
    with open(doc_paths_file) as fp:
        for line in fp: 
            fi.append(line.strip().split())
    return fi

def load_lda_variables(dictionary_file, lda_mdl_file, lda_index_file):
    '''This function loads all the LDA model variables from 
    the given files 
    
    Returns: 
        a tuple of dictionary, lda model, and lda index
    Arguments:
        dictionary_file - the dictionary file
        lda_mdl_file - the LDA model file 
        lda_index_file - the LDA index file 
    '''

    dictionary = gensim.corpora.Dictionary().load(dictionary_file)
    lda = gensim.models.ldamodel.LdaModel.load(lda_mdl_file)
    index = gensim.similarities.MatrixSimilarity.load(lda_index_file)

    return (dictionary, lda, index)


def process_query(query, dictionary, lda, index, files_info, limit=5):
    '''Tokenize the input query and finds topically 
    similar documents (responsive) using LDA based 
    document search. Currently, the responsive documents 
    are determined by just taking top N records from 
    the ranked set of documents. 
    
    TODO: 
        (a) improve the method that identifies the 
        responsive documents 
    
    Returns:
        a lists of lists of responsive and non responsive 
        document details such as [doc_id, doc_dir_path, doc_name, score] 
    Arguments:
        query - the query in text format 
        dictionary - the dictionary object 
        lda - the LDA model object 
        index - the index object 
        files_info - the list of file details 
        limit - the limit on the number of responsive records 
    
    '''

    # process the query 
    
    query_vec = dictionary.doc2bow(query.lower().split())
    query_td = lda[query_vec]
    
    # querying based on cosine distance
    
    sims = index[query_td] # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    ## Identifies responsive and non-responsive documents
     
    responsive_docs_idx = sims[0:limit]
    non_responsive_docs_idx = sims[limit:len(sims)]
    
    responsive_docs = [] 
    for (doc_id, score) in responsive_docs_idx: 
        doc = files_info[doc_id]
        doc.append(score)
        responsive_docs.append(doc)
    
    non_responsive_docs = [] 
    for (doc_id, score) in non_responsive_docs_idx: 
        doc = files_info[doc_id]
        doc.append(score)
        non_responsive_docs.append(doc)
    
    ## The responsive_docs and non_responsive_docs are lists 
    ## of lists. The internal list has the following 
    ## fixed set of elements = [doc_id, email_path, file_name, score]  
    
    return (responsive_docs, non_responsive_docs)



def test_query():
    '''
    This function tests a sample query 
    '''

    dictionary_file = 'fs_enron.dict'
    doc_paths_file = 'fs_enron.email_paths'
    lda_mdl_file = 'fs_enron.lda_mdl'
    lda_index_file = 'fs_enron.lda_index'
    query = 'Human computer interaction'
    
    responsive_docs, non_responsive_docs = process_query(query, dictionary_file, lda_mdl_file, lda_index_file, doc_paths_file, limit=5)
    
    return responsive_docs, non_responsive_docs


