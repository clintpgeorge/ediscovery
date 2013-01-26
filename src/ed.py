#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np 

from tm.lda_process_query import process_query
from sampler.RandomSampler2 import RandomSampler


dictionary_file = 'fs_enron.dict'
doc_paths_file = 'fs_enron.email_paths'
lda_mdl_file = 'fs_enron.lda_mdl'
lda_index_file = 'fs_enron.lda_index'
query = raw_input('Enter query: ')  # 'Human computer interaction'

responsive_docs, non_responsive_docs = process_query(query, dictionary_file, lda_mdl_file, lda_index_file, doc_paths_file, limit=100)


nrd = np.array(non_responsive_docs)
nrd_paths = nrd[:,1]


confidence = float( raw_input('Confidence: '))
precision = float('Precision: ')
SEEDCONSTANT = float('Seed: ')

randomSample = RandomSampler(nrd_paths, confidence, precision, SEEDCONSTANT)


print randomSample


