#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script loads any Blei corpus and dictionary 
and performs the online LDA inference and saves 
the model and parameters to files     

Created On: Jan 24, 2013 
Created By: Clint P. George 
  
'''


import numpy as np
import gensim

CHUNK_SIZE = 10000


def is_number(s):
    '''Checks whether a given token is a number 
    Returns: 
        a boolean 
    Arguments: 
        a token 
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def normalize_columns(arr):
    '''Normalize the columns of a given numpy matrix or array 
    
    Returns: 
        a numpy matrix/array 
    Arguments: 
        a numpy matrix/array  
    '''
    _, cols = arr.shape
    for col in xrange(cols):
        col_sum = sum(arr[:, col])
        if is_number(col_sum) and col_sum > 0: 
            arr[:, col] /= col_sum
        else: 
            arr[:, col] = 0 
    return arr 

def normalize_rows(arr):
    '''Normalize the rows of a given numpy matrix or array 
    
    Returns: 
        a numpy matrix/array  
    Arguments: 
        a numpy matrix/array  
    '''
    rows, _ = arr.shape
    for row in xrange(rows):
        row_sum = sum(arr[row, :])
        if is_number(row_sum) and row_sum > 0: 
            arr[row, :] /= row_sum
        else: 
            arr[row, :] = 0 
    return arr 

def run_lda_estimation(dictionary_file, ldac_file, lda_mdl_file, lda_beta_file, lda_theta_file, lda_index_file, num_topics, num_passes):
    '''The main function that does the LDA estimation 
    process and saves all the model parameters and the 
    index created by the Gensim Similarity class.   
    '''

    # loads the corpus 
    
    corpus = gensim.corpora.BleiCorpus(ldac_file)
    id2word = gensim.corpora.Dictionary().load(dictionary_file)
    
    # runs the LDA inference 
    
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics, update_every=1, chunksize=CHUNK_SIZE, passes=num_passes)
    lda.save(lda_mdl_file)
    
    # saves the LDA beta 
    
    beta = lda.expElogbeta
    np.savetxt(lda_beta_file, beta)
    
    # Saves document topic distributions 
    
    doc_topics = lda[corpus] # get topic probability distribution for a document
    num_docs = len(doc_topics)
    theta_matrix = np.zeros((num_docs, num_topics))
    count = 0
    for doc in doc_topics: 
        doc = dict(doc)
        theta_matrix[count, doc.keys()] = doc.values()
        count += 1 
    np.savetxt(lda_theta_file, theta_matrix)
    
    
    # Saves index 
    
    index = gensim.similarities.MatrixSimilarity(lda[corpus]) # transform corpus to LDA topic space and index it
    index.save(lda_index_file)




#************** TESTING **************

## Loads the matrix to memory 

#tm = np.loadtxt(lda_theta_file, dtype=float)
#bm = np.loadtxt(lda_beta_file, dtype=float)
#
## normalizes the rows 
#nbm = normalize_rows(bm)
#ntm = normalize_rows(tm)


## writes the topics into a file 
#topic_list = lda.show_topics(topics=num_topics, topn=10000, formatted=False)
#with open(lda_beta_file, 'w') as fw:  
#    for tl in topic_list:
#        print >> fw, ' '.join('%0.8f|%s' % x for x in tl)
## writes the document distributions to a file   
## CASE I
# theta = gensim.matutils.corpus2dense(doc_topics, num_topics)
## CASE III
#doc_topics = lda[corpus] # get topic probability distribution for a document
#num_docs = len(doc_topics)
#theta_matrix = np.zeros((num_docs, num_topics))
#count = 0
#for doc in doc_topics: 
#    for each_tuple in doc:
#        theta_matrix[count, each_tuple[0]] = each_tuple[1]
#    count += 1




