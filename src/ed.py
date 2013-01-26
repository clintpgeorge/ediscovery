#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np 
import os  
from tm.lda_process_query import process_query, load_docs_info, load_lda_variables
from sampler.RandomSampler2 import RandomSampler

DATA_PATH = '/data/ediscovery/enron/' # raw_input('Data path: ')
dictionary_file = os.path.join(DATA_PATH, 'fs_enron.dict')
doc_paths_file = os.path.join(DATA_PATH, 'fs_enron.email_paths')
lda_mdl_file = os.path.join(DATA_PATH, 'fs_enron.lda_mdl')
lda_index_file = os.path.join(DATA_PATH, 'fs_enron.lda_index')
SEEDCONSTANT = 2013 

## Loads the LDA model and file details 

doc_paths = load_docs_info(doc_paths_file)
dictionary, lda, index = load_lda_variables(dictionary_file, lda_mdl_file, lda_index_file)


while raw_input('Exit: ').lower() <> 'y':  

    ## Enter query 
    search_algorithm = raw_input('Search algorithm [LDA or Lucene]: ').strip()
    
    if search_algorithm == 'LDA':
    
        query = raw_input('Enter query: ')  # 'Human computer interaction'
        limit = int(raw_input('Limit: '))
        ## Process the query 
        
        responsive_docs, non_responsive_docs = process_query(query, dictionary, lda, index, doc_paths, limit)
        
    elif search_algorithm == 'Lucene':
        None 
        
    nrd = np.array(non_responsive_docs)
    nrd_paths = [os.path.join(dir_path, nrd[idx,2]) for idx, dir_path in enumerate(nrd[:,1])]
    
    print 'Number of responsive documents:', len(responsive_docs)
    print 'Number of non responsive documents:', len(responsive_docs)
    # TODO: copy responsive documents into a TIMESTAMP/responsive folder 
    
    
    ## Enter confidence intervals to get samples  
    
    confidence = float( raw_input('Confidence: '))
    precision = float(raw_input('Precision: '))
    randomSample = RandomSampler(nrd_paths, confidence, precision, SEEDCONSTANT)
    
    
    # print randomSample
    print 'Number of samples', len(randomSample), 'out of', len(nrd_paths) 
    # TODO: copy responsive documents into a TIMESTAMP/nonresponsive_samples folder 
    
    



