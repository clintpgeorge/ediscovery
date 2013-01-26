#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np 
import os  
from tm.lda_process_query import process_query
from sampler.RandomSampler2 import RandomSampler

DATA_PATH = '/data/ediscovery/enron/' # raw_input('Data path: ')
dictionary_file = os.path.join(DATA_PATH, 'fs_enron.dict')
doc_paths_file = os.path.join(DATA_PATH, 'fs_enron.email_paths')
lda_mdl_file = os.path.join(DATA_PATH, 'fs_enron.lda_mdl')
lda_index_file = os.path.join(DATA_PATH, 'fs_enron.lda_index')
query = raw_input('Enter query: ')  # 'Human computer interaction'

responsive_docs, non_responsive_docs = process_query(query, dictionary_file, lda_mdl_file, lda_index_file, doc_paths_file, limit=100)


nrd = np.array(non_responsive_docs)
nrd_paths = [os.path.join(dir_path, nrd[idx,2]) for idx, dir_path in enumerate(nrd[:,1])]


confidence = float( raw_input('Confidence: '))
precision = float(raw_input('Precision: '))
SEEDCONSTANT = float(raw_input('Seed: '))

randomSample = RandomSampler(nrd_paths, confidence, precision, SEEDCONSTANT)


print randomSample
print 'number of samples', len(randomSample), 'out of', len(nrd_paths) 

