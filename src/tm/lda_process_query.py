#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script process any given query in text format 
and finds similar documents from the learned 
LDA model.  
'''

import logging, gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def load_doc_info(doc_paths_file):
    fi = [] 
    with open(doc_paths_file) as fp:
        for line in fp: 
            fi.append(line.strip().split())
    return fi



def process_query(query, dictionary_file, lda_mdl_file, lda_index_file, doc_paths_file, limit=5):
    '''
    Tokenize the input query and finds topically 
    similar documents (responsive) using LDA based 
    document search. Currently, the responsive documents 
    are determined by just taking top N records from 
    the ranked set of documents. 
    
    TODO: 
        (a) improve the method that identifies the 
        responsive documents 
    '''
    # corpus = gensim.corpora.BleiCorpus(ldac_file)
    id2word = gensim.corpora.Dictionary().load(dictionary_file)
    lda = gensim.models.ldamodel.LdaModel.load(lda_mdl_file)
    index = gensim.similarities.MatrixSimilarity.load(lda_index_file)
    # process the query 
    query_vec = id2word.doc2bow(query.lower().split())
    query_td = lda[query_vec]
    # querying based on cosine distance
    sims = index[query_td] # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    ## Identifies responsive and non-responsive documents
     
    responsive_docs_idx = sims[0:limit]
    non_responsive_docs_idx = sims[limit:len(sims)]
    
    fi = load_doc_info(doc_paths_file)
    
    responsive_docs = [] 
    for (doc_id, score) in responsive_docs_idx: 
        doc = fi[doc_id]
        doc.append(score)
        responsive_docs.append(doc)
    
    non_responsive_docs = [] 
    for (doc_id, score) in non_responsive_docs_idx: 
        doc = fi[doc_id]
        doc.append(score)
        non_responsive_docs.append(doc)
    
    ## The responsive_docs and non_responsive_docs are lists 
    ## of lists. The internal list has the following 
    ## fixed set of elements = [doc_id, email_path, file_name, score]  
    
    return (responsive_docs, non_responsive_docs)



def test_query():

    dictionary_file = 'fs_enron.dict'
    doc_paths_file = 'fs_enron.email_paths'
    lda_mdl_file = 'fs_enron.lda_mdl'
    lda_index_file = 'fs_enron.lda_index'
    query = 'Human computer interaction'
    
    responsive_docs, non_responsive_docs = process_query(query, dictionary_file, lda_mdl_file, lda_index_file, doc_paths_file, limit=5)
    
    return responsive_docs, non_responsive_docs


