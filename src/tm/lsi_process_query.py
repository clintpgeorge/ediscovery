#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script process any given query in text format 
and finds similar documents from the learned 
LSI model.  

Created On: March 24, 2013 
Created By: Clint P. George 
'''

import logging, gensim
from utils.utils_file import load_file_paths_index 

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




def load_lsi_variables(dictionary_file, lsi_mdl_file, lsi_index_file):
    '''This function loads all the lsi model variables from 
    the given files 
    
    Returns: 
        a tuple of dictionary, lsi model, and lsi index
    Arguments:
        dictionary_file - the dictionary file
        lsi_mdl_file - the LSI model file 
        lsi_index_file - the LSI index file 
    '''

    dictionary = gensim.corpora.Dictionary().load(dictionary_file)
    lsi = gensim.models.lsimodel.LsiModel.load(lsi_mdl_file)
    index = gensim.similarities.MatrixSimilarity.load(lsi_index_file)

    return (dictionary, lsi, index)


def process_query(query, dictionary, lsi, index, files_info, limit=5):
    '''Tokenize the input query and finds topically 
    similar documents (responsive) using lsi based 
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
        lsi - the lsi model object 
        index - the index object 
        files_info - the list of file details 
        limit - the limit on the number of responsive records 
    
    '''

    # process the query 
    
    query_vec = dictionary.doc2bow(query.lower().split())
    query_td = lsi[query_vec]
    
    # querying based on cosine distance
    
    sims = index[query_td] # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    ## Identifies responsive and non-responsive documents
     
    responsive_docs_idx = sims[0:limit]
    non_responsive_docs_idx = sims[limit:len(sims)]
    
    responsive_docs = [] 
    for (doc_id, score) in responsive_docs_idx: 
        doc = list(files_info[doc_id])
        doc.append(score)
        responsive_docs.append(doc)
    
    non_responsive_docs = [] 
    for (doc_id, score) in non_responsive_docs_idx: 
        doc = list(files_info[doc_id])
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

    dictionary_file = '/home/cgeorge/data/tm/enron.dict'
    doc_paths_file = '/home/cgeorge/data/enron.path.index'
    lsi_mdl_file = '/home/cgeorge/data/tm/enron.lsi'
    lsi_index_file = '/home/cgeorge/data/tm/enron.lsi.cos.index'
    query = 'half from new deals and the other half from reserve releases, and when you back out the prudency release you get back to zero net curve shift for 2001, which is what the original file had'
    
    dictionary, lsi, index = load_lsi_variables(dictionary_file, lsi_mdl_file, lsi_index_file)
    files_info = load_file_paths_index(doc_paths_file)
    
    responsive_docs, non_responsive_docs = process_query(query, dictionary, lsi, index, files_info, limit=5)
    
    return responsive_docs, non_responsive_docs


# responsive_docs, non_responsive_docs = test_query()
# print responsive_docs




    
    
    
