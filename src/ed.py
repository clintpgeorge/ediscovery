#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script is to test the basic query processing 
based on LDA and pyLucene 

Created by: Clint P. George and Abhiram J. 
Created on: Jan 28, 2013 

'''
import os
import datetime
import numpy as np 

from lucenesearch.lucene_index import lucene_index
from lucenesearch.lucene_search import lucene_search  
#from tm.lda_process_query import process_query, load_docs_info, load_lda_variables
from sampler.random_sampler import random_sampler
from file_utils import copy_random_files, find_files_in_folder, copy_files_with_dir_tree



'''
Global variables 

TODO: The hard coded values should be removed 
'''

DATA_PATH = '/media/Non OS/EDiscovery/enron_mail_20110402'# '/data/ediscovery/enron' # raw_input('Data path: ')
dictionary_file = os.path.join(DATA_PATH, 'fs_enron.dict')
doc_paths_file = os.path.join(DATA_PATH, 'fs_enron.email_paths')
lda_mdl_file = os.path.join(DATA_PATH, 'fs_enron.lda_mdl')
lda_index_file = os.path.join(DATA_PATH, 'fs_enron.lda_index_kl')
SEEDCONSTANT = 2013 

# Loads the LDA model and file details 

#doc_paths = load_docs_info(doc_paths_file)
#dictionary, lda, index = load_lda_variables(dictionary_file, lda_mdl_file, lda_index_file)

#Lucene specific settings and indexing 
output_folder = raw_input('Enter output folder: ')
choice = 'n'
lucene_index_file = os.path.join(output_folder, 'lucene.index')
if not os.path.exists(lucene_index_file):
    lucene_index(DATA_PATH, lucene_index_file)
while choice <> 'y':  

    ## Enter query 
    search_algorithm = raw_input('Search algorithm [LDA or Lucene]: ').strip()
    
    query = raw_input('Enter query: ')  # 'Human computer interaction'
    limit = int(raw_input('Limit: '))
    
    
    if search_algorithm == 'LDA':
    
        None
        # Process the query 
        
#        responsive_docs, non_responsive_docs = process_query(query, dictionary, lda, index, doc_paths, limit)
#        nrd = np.array(non_responsive_docs)
#        nrd_paths = [os.path.join(dir_path, nrd[idx,2]) for idx, dir_path in enumerate(nrd[:,1])] # looks like i'm not getting full file paths
        
    elif search_algorithm == 'Lucene':
#        None 
        responsive_docs = lucene_search(lucene_index_file, limit, query)
        non_responsive_docs = []
        for file_name in find_files_in_folder(DATA_PATH):
            if os.path.dirname(file_name) is not lucene_index_file:       # skipping index directory
                if file_name not in responsive_docs:
                    non_responsive_docs.append(file_name)
        nrd_paths=non_responsive_docs 
    
    print 'Number of responsive documents:', len(responsive_docs)
    print 'Number of non responsive documents:', len(non_responsive_docs) 
    
    print 'The responsive files are: '
    for f in responsive_docs:
        print f 
    
    
#    ## Enter confidence intervals to get samples  
#    
#    confidence = float( raw_input('Confidence: '))
#    precision = float(raw_input('Precision: '))
#    sampled_nrd_paths = random_sampler(nrd_paths, confidence, precision, SEEDCONSTANT)
#    print 'Number of samples', len(sampled_nrd_paths), 'out of', len(nrd_paths) 
#    
#    
#    timestamp_appender = "non-responsive -- "+ str(datetime.datetime.now())
#    nrd_file_folder= os.path.join(output_folder,timestamp_appender)
#    copy_files_with_dir_tree(sampled_nrd_paths, nrd_file_folder, DATA_PATH)
#    
#
#    choice = raw_input('Exit [Y - Yes or N - No]: ').lower()


