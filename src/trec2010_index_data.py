#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This is a script wrote to index the TREC 2010 seeds data sets with varying 
number of topics.    

Created on July 3, 2014

@author: Clint P. George 
'''
import time 
import os 
import sys 
import logging 

from whoosh_index_dir import index_plain_text_emails2
from whoosh_enron_create_corpus import build_lda_corpus2
from topicmodels import run_tfidf, run_lda_estimation
from index_data_whoosh import LOG_FORMAT, TM_FOLDER_NAME, WHOOSH_FOLDER_NAME

def index_and_tm(data_folder, output_folder, project_name, num_topics, 
                num_passes, min_token_freq, min_token_len, max_token_len, 
                stem=False, procs=4, limitmb=512, multisegment=True):

    if not os.path.exists(data_folder):
        logging.error("Please provide a valid data folder!")
        sys.exit(1)
           
    # Checks whether the output folder exists 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Checks whether the project folder exists 
    project_folder = os.path.join(output_folder, project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
        
    tm_folder = os.path.join(project_folder, TM_FOLDER_NAME)
    whoosh_folder = os.path.join(project_folder, WHOOSH_FOLDER_NAME)

    
    # Handling the project configuration file 
    
    logging.info('Indexing Configurations:')
    logging.info('Project: %s', project_name)
    
    #print "Indexing documents...."
    start_time = time.time()
    

    logging.info('================================= BEGIN WHOOSH INDEXING')
    
    if not os.path.exists(whoosh_folder): os.makedirs(whoosh_folder)
    path_index_file_name = os.path.join(project_folder, 
                                        project_name + '.path.index')
    
    index_plain_text_emails2(data_folder, path_index_file_name, 
                             whoosh_folder, stem, 
                             min_token_len, max_token_len, 
                             procs, limitmb, multisegment) 

    logging.info('================================= END WHOOSH INDEXING')

    print '\nIndexing time:', (time.time() - start_time), 'seconds'
    
    #print "Corpus building...."
    start_time = time.time()


    logging.info('=============================== BEGIN CORPUS BUILDING')
     
    if not os.path.exists(tm_folder): os.makedirs(tm_folder)
    dict_file = os.path.join(tm_folder, project_name + '.dict')
    ldac_file = os.path.join(tm_folder, project_name + '.ldac')
    path_index_file_name = os.path.join(tm_folder, project_name + '.path.index')     
    build_lda_corpus2(whoosh_folder, path_index_file_name, dict_file, 
                     ldac_file, min_token_freq, min_token_len, 
                     max_token_len, stem)
     
    logging.info('=============================== END CORPUS BUILDING')
     
    
    print '\nCorpus building time:', (time.time() - start_time), 'seconds'
     
    #print "Topic modeling...."
    start_time = time.time()
    
    for k in num_topics:
        logging.info('=============================== BEGIN LDA ESTIMATION')
        logging.info('LDA Number of topics: %d', k)
        logging.info('LDA Number of passes: %d', num_passes)
        lda_model_file = os.path.join(tm_folder, project_name + '-K%d-VB.lda' % k)
        lda_beta_file = os.path.join(tm_folder, project_name + '-K%d-VB.lda.beta' % k)
        lda_theta_file = os.path.join(tm_folder, project_name + '-K%d-VB.lda.theta' % k)
        lda_cos_index_file = os.path.join(tm_folder, project_name + '-K%d-VB.lda.cos.index' % k)
        run_lda_estimation(dict_file, ldac_file, lda_model_file, lda_beta_file, 
                           lda_theta_file, lda_cos_index_file, k, 
                           num_passes)
        logging.info('=============================== END LDA ESTIMATION')    
 
    logging.info('=============================== BEGIN TFIDF')
    tfidf_theta_file = os.path.join(tm_folder, project_name + '.tfidf.theta')
    run_tfidf(dict_file, ldac_file, tfidf_theta_file)
    logging.info('=============================== END TFIDF')    


    print '\nTopic modeling time:', (time.time() - start_time), 'seconds'




'''
TEST SCRIPTS 
'''


#########################################################
## Hard coded values. Should be edited/checked before 
## running this script  
#########################################################


data_folder = "E:\\E-Discovery\\trec2010seeds-wa"
output_folder = "E:\\E-Discovery\\trec2010index-wa"
query_ids = [201, 202, 203, 207]
topic_counts = [5, 10, 15, 20, 30, 40, 50, 60, 70, 80]
num_passes = 10
log_file_name = os.path.join(output_folder, 'index_trec2010_data.log')


#########################################################


if not os.path.exists(output_folder): os.makedirs(output_folder)

logging.basicConfig(filename=log_file_name, format=LOG_FORMAT, level=logging.DEBUG)
 
print "Indexing documents...."
 
start_time = time.time()
     
for query_id in query_ids:
    query_data_folder = "%s\%d" % (data_folder, query_id)
    print "Indexing ", query_data_folder
        
    # With stemmed tokens 
    project_name = "Q%d-S" % query_id
    index_and_tm(query_data_folder, output_folder, project_name, 
        topic_counts, num_passes, min_token_freq=5, min_token_len=2, 
        max_token_len=100, stem=True, procs=1, limitmb=4096, 
        multisegment=False)
    
    # With raw tokens 
    project_name = "Q%d-R" % query_id
    index_and_tm(query_data_folder, output_folder, project_name, 
        topic_counts, num_passes, min_token_freq=5, min_token_len=2, 
        max_token_len=100, stem=False, procs=1, limitmb=4096, 
        multisegment=False)
 
print '\nIndexing time:', time.time() - start_time, 'seconds'        

