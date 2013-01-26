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
import logging, gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def normalize_columns(arr):
    _, cols = arr.shape
    for col in xrange(cols):
        col_sum = sum(arr[:, col])
        if is_number(col_sum) and col_sum > 0: 
            arr[:, col] /= col_sum
        else: 
            arr[:, col] = 0 
    return arr 

def normalize_rows(arr):
    rows, _ = arr.shape
    for row in xrange(rows):
        row_sum = sum(arr[row, :])
        if is_number(row_sum) and row_sum > 0: 
            arr[row, :] /= row_sum
        else: 
            arr[row, :] = 0 
    return arr 




# Initializes the variables 

dictionary_file = 'fs_enron.dict'
ldac_file = 'fs_enron.ldac'
lda_mdl_file = 'fs_enron.lda_mdl'
lda_beta_file = 'fs_enron.lda_beta'
lda_theta_file = 'fs_enron.lda_theta'
lda_index_file = 'fs_enron.lda_index'
num_topics = 100
passes = 10 


# loads the corpus 

corpus = gensim.corpora.BleiCorpus(ldac_file)
id2word = gensim.corpora.Dictionary().load(dictionary_file)

# runs the LDA inference 

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics, update_every=1, chunksize=10000, passes=passes)
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




