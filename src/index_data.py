#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script is used to index all files 
in a given folder using Lucene and topic models 

Created On: May 23, 2013
@author: Clint P. George 
'''

import os 
import sys 
import argparse
import logging 
import ConfigParser

from lucenesearch.lucene_index_dir import index_plain_text_emails
from preprocess.lucene_enron_create_corpus import build_lda_corpus
from tm.lda_estimation import run_lda_estimation 
from tm.lsi_estimation import run_lsi_estimation

LUCENE_FOLDER_NAME = 'lucene'
TM_FOLDER_NAME = 'tm' 
STOP_WORDS_FILE_NAME = 'en_stopwords'
MIN_TOKEN_FREQ = 2
MIN_TOKEN_LEN = 2 
DEFAULT_NUM_TOPICS = 30
DEFAULT_NUM_PASSES = 100
LSI_DEFAULT_NUM_TOPICS = 200




def index_data(data_folder, output_folder, project_name, cfg_folder, 
               num_topics=DEFAULT_NUM_TOPICS, num_passes=DEFAULT_NUM_PASSES, 
               min_token_freq=MIN_TOKEN_FREQ, min_token_len=MIN_TOKEN_LEN, 
               log_to_file=True, lemmatize=False, stem=False, nonascii=True):
    
    if not os.path.exists(data_folder):
        print "Please provide a valid data folder!"
        sys.exit(1)
        
    # Checks whether the output folder exists 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Checks whether the project folder exists 
    project_folder = os.path.join(output_folder, project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)

    # Create file handler which logs debug messages
    log_file_name = '%s.log' % os.path.join(project_folder, project_name)

    if log_to_file: 
        logging.basicConfig(filename=log_file_name, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    else: 
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

    
    # Handling the project configuration file 
    
    print 'Indexing Configurations:'
    print 'Project:', project_name
    print 'Number of LDA topics:', num_topics
    print 'Number of LDA passes:', num_passes
    print 'Number of LSA topics:', LSI_DEFAULT_NUM_TOPICS
    
    cfg_file_name = os.path.join( cfg_folder , project_name + '.cfg' )
    config = ConfigParser.RawConfigParser()

    config.add_section('DATA')
    config.set('DATA', 'name', project_name)
    config.set('DATA', 'root_dir', os.path.normpath(data_folder)) # may need to change the name 
    config.set('DATA', 'project_dir', os.path.normpath(project_folder))
    config.set('DATA', 'log_file', os.path.normpath(log_file_name))
    config.set('DATA', 'output_folder', os.path.normpath(output_folder))   
        
    logging.info('================================================== BEGIN LUCENE INDEXING ==================================================')
    
    lucene_folder = os.path.join(project_folder, LUCENE_FOLDER_NAME)
    if not os.path.exists(lucene_folder): os.makedirs(lucene_folder)
    path_index_file_name = os.path.join(project_folder, project_name + '.path.index')
    
    index_plain_text_emails(data_folder, path_index_file_name, lucene_folder, lemmatize=lemmatize, stem=stem, nonascii=nonascii)
    
    config.add_section('LUCENE')
    config.set('LUCENE', 'lucene_index_dir', os.path.normpath(lucene_folder))
    config.set('LUCENE', 'path_index_file', os.path.normpath(path_index_file_name))
    
    logging.info('================================================== END LUCENE INDEXING ==================================================')

    logging.info('================================================== BEGIN CORPUS BUILDING ==================================================')

    tm_folder = os.path.join(project_folder, TM_FOLDER_NAME)
    if not os.path.exists(tm_folder): os.makedirs(tm_folder)
    dict_file = os.path.join(tm_folder, project_name + '.dict')
    ldac_file = os.path.join(tm_folder, project_name + '.ldac')
    path_index_file_name = os.path.join(tm_folder, project_name + '.path.index') # it's for topic modeling alone 
    
    build_lda_corpus(lucene_folder, path_index_file_name, STOP_WORDS_FILE_NAME, dict_file, ldac_file, min_token_freq, min_token_len)
    
    config.add_section('CORPUS')
    config.set('CORPUS', 'tm_folder', os.path.normpath(tm_folder))
    config.set('CORPUS', 'path_index_file', os.path.normpath(path_index_file_name))
    config.set('CORPUS', 'blei_corpus_file', os.path.normpath(ldac_file))
    config.set('CORPUS', 'dict_file', os.path.normpath(dict_file))
    config.set('CORPUS', 'vocab_file', os.path.normpath(ldac_file + '.vocab'))  

    
    logging.info('================================================== END CORPUS BUILDING ==================================================')
    
    project_name = os.path.normpath(project_name)
    
    logging.info('================================================== BEGIN LDA ESTIMATION ==================================================')

    lda_model_file = os.path.join(tm_folder, project_name + '.lda')
    lda_beta_file = os.path.join(tm_folder, project_name + '.lda.beta')
    lda_theta_file = os.path.join(tm_folder, project_name + '.lda.theta')
    lda_cos_index_file = os.path.join(tm_folder, project_name + '.lda.cos.index')
    
    run_lda_estimation(dict_file, ldac_file, lda_model_file, lda_beta_file, lda_theta_file, lda_cos_index_file, num_topics, num_passes)
    
    # run_hdp_estimation(dict_file, ldac_file, lda_model_file, lda_beta_file, lda_theta_file, lda_cos_index_file)
    
    config.add_section('LDA')
    config.set('LDA', 'lda_model_file', lda_model_file)
    config.set('LDA', 'lda_beta_file', lda_beta_file)
    config.set('LDA', 'lda_theta_file', lda_theta_file)
    config.set('LDA', 'lda_cos_index_file', lda_cos_index_file)
    config.set('LDA', 'num_topics', str(num_topics))
    config.set('LDA', 'num_passes', str(num_passes))    
    
    logging.info('================================================== END LDA ESTIMATION ==================================================')    
    
    
    
    logging.info('================================================== BEGIN LSI ESTIMATION ==================================================')
    
    # Commented LSI due to an error from python interpreter on Feb 04, 2014

#     lsi_model_file = os.path.join(tm_folder, project_name + '.lsi')
#     lsi_beta_file = os.path.join(tm_folder, project_name + '.lsi.beta')
#     lsi_theta_file = os.path.join(tm_folder, project_name + '.lsi.theta')
#     lsi_cos_index_file = os.path.join(tm_folder, project_name + '.lsi.cos.index')
#     # 
#     
#     run_lsi_estimation(dict_file, ldac_file, lsi_model_file, lsi_beta_file, lsi_theta_file, lsi_cos_index_file, LSI_DEFAULT_NUM_TOPICS)
# 
#     config.add_section('TFIDF')
#     config.set('TFIDF', 'tfidf_file', lsi_theta_file.replace('lsi', 'tfidf'))
#         
#     config.add_section('LSI')
#     config.set('LSI', 'lsi_model_file', lsi_model_file)
#     config.set('LSI', 'lsi_beta_file', lsi_beta_file)
#     config.set('LSI', 'lsi_theta_file', lsi_theta_file)
#     config.set('LSI', 'lsi_cos_index_file', lsi_cos_index_file)
#     config.set('LSI', 'lsi_num_topics', str(LSI_DEFAULT_NUM_TOPICS))

    
    logging.info('================================================== END LSI ESTIMATION ==================================================')    
    
    
    # Writing our configuration file to 'project.cfg'
    with open(cfg_file_name, 'w') as configfile:
        config.write(configfile)
        
    logging.info('The project configuration file is written to %s', cfg_file_name)
    print 'Indexing is completed. The project configuration file is written to', cfg_file_name



if __name__=="__main__":
    '''
    The main function
    '''

    
    arg_parser = argparse.ArgumentParser('''
    
    Lucene index builder for email files  

    Examples: 
        python index_data.py -h # for help 
        python index_data.py -l -d "E:\\E-Discovery\\trec2010dataset\\202" -o "E:\\E-Discovery\\trec2010index" -p 202 -z -s -a      

    ''')
    arg_parser.add_argument("-d", dest="data_folder", type=str, help="data folder", required=True)
    arg_parser.add_argument("-o", dest="output_folder", type=str, help="output folder", required=True)
    arg_parser.add_argument("-p", dest="project_name", type=str, help="project name", required=True)
    arg_parser.add_argument("-t", dest="num_topics", type=int, help="number of topics", default=DEFAULT_NUM_TOPICS)
    arg_parser.add_argument("-n", dest="num_passes", type=int, help="number of passes", default=DEFAULT_NUM_PASSES)
    arg_parser.add_argument("-s", dest="stem", action="store_true", help="stem tokens", default=False)
    arg_parser.add_argument("-z", dest="lemmatize", action="store_true", help="lemmatize tokens", default=False)
    arg_parser.add_argument("-a", dest="nonascii", action="store_true", help="allow non-ASCII tokens", default=False)
    arg_parser.add_argument("-l", "--log", dest="log", default=False, action="store_true", help="log details into a file")
    args = arg_parser.parse_args()
    
    
    data_folder = os.path.normpath(args.data_folder)
    output_folder = os.path.normpath(args.output_folder)
    project_name = args.project_name
    num_topics = args.num_topics
    num_passes = args.num_passes 
    
    import time 
    
    print "Indexing documents...."
    
    start_time = time.time()
    index_data(data_folder, output_folder, project_name, "", 
               num_topics, num_passes, 
               min_token_freq=MIN_TOKEN_FREQ, 
               min_token_len=MIN_TOKEN_LEN, 
               log_to_file=args.log,
               lemmatize=args.lemmatize, 
               stem=args.stem, 
               nonascii=args.nonascii)
    
    print '\nIndexing time:', time.time() - start_time, 'seconds'
    
