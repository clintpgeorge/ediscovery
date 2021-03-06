#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script loads any Blei corpus and dictionary 
and performs the LSI inference and saves 
the model and parameters to files     

Created On: Mar 24, 2013 
Created By: Clint P. George 
  
'''

import numpy as np
import gensim

def run_tfidf(dictionary_file, ldac_file, tfidf_file):
    
    corpus = gensim.corpora.BleiCorpus(ldac_file)    
    tfidf = gensim.models.TfidfModel(corpus) 
    corpus_tfidf = tfidf[corpus]

    with open(tfidf_file, 'w') as fw:
        for doc_tfidf in corpus_tfidf:
            print >>fw, doc_tfidf        

    

def run_lsi_estimation(dictionary_file, ldac_file, lsi_mdl_file, lsi_beta_file, lsi_theta_file, lsi_index_file, num_topics):
    '''The main function that does the LSI estimation 
    process and saves all the model parameters and the 
    index created by the Gensim Similarity class.   
    '''

    # loads the corpus 
    
    corpus = gensim.corpora.BleiCorpus(ldac_file)
    id2word = gensim.corpora.Dictionary().load(dictionary_file)
    
    # runs the LSA inference
    
    tfidf = gensim.models.TfidfModel(corpus) 
    corpus_tfidf = tfidf[corpus]

    with open(lsi_theta_file.replace('lsi', 'tfidf'), 'w') as fw:
        for doc_tfidf in corpus_tfidf:
            print >>fw, doc_tfidf        
    
    lsi = gensim.models.lsimodel.LsiModel(corpus=corpus_tfidf, id2word=id2word, num_topics=num_topics)
    lsi.save(lsi_mdl_file)
    
    # TODO: saves the lsi topics 
    # implement this part if we need in future 
    
    
    # Saves document LSI transformations 
    
    doc_topics = lsi[corpus_tfidf] # get the document represented in LSI space 
    num_docs = len(doc_topics)
    theta_matrix = np.zeros((num_docs, num_topics))
    count = 0
    for doc in doc_topics: 
        doc = dict(doc)
        theta_matrix[count, doc.keys()] = doc.values()
        count += 1 
    np.savetxt(lsi_theta_file, theta_matrix)
    
    
    # Saves the indices  
    
    index = gensim.similarities.MatrixSimilarity(lsi[corpus_tfidf]) # transform corpus to lsi topic space and index it
    index.save(lsi_index_file)

