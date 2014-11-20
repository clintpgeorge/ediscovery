#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script is used to index all files in a given folder using Whoosh and 
topic models 

Created On: May 23, 2013
@author: Clint P. George

Updated On: Apr 12, 2014
@author: Sahil Puri 

Updated On: June 04, 2014
@author: Clint P. George 

'''
import time 
import os 
import sys 
import argparse
import logging 
import ConfigParser

from whoosh_index_dir import index_plain_text_emails2
from whoosh_enron_create_corpus import build_lda_corpus2
from topicmodels import run_tfidf, run_lda_estimation

WHOOSH_FOLDER_NAME = 'whoosh'
TM_FOLDER_NAME = 'tm' 
MIN_TOKEN_FREQ = 20
MIN_TOKEN_LEN = 2 
MAX_TOKEN_LEN = 30
DEFAULT_NUM_TOPICS = 30
DEFAULT_NUM_PASSES = 1
LSI_DEFAULT_NUM_TOPICS = 200
LOG_FORMAT = '%(asctime)s: %(levelname)s: [%(filename)s:%(lineno)s:%(funcName)s()] %(message)s'


def index_data(data_folder, output_folder, project_name, cfg_folder, 
               num_topics=DEFAULT_NUM_TOPICS, num_passes=DEFAULT_NUM_PASSES, 
               min_token_freq=MIN_TOKEN_FREQ, min_token_len=MIN_TOKEN_LEN, 
               max_token_len=MAX_TOKEN_LEN, log_to_file=False, lemmatize=False, 
               stem=False, nonascii=True, procs=4, limitmb=512, multisegment=True):
    
    def save_config(cfg_file_name, config):
        # Writing our configuration file
        with open(cfg_file_name, 'w') as configfile:
            config.write(configfile)
        logging.info('The project configuration file is written to %s', 
                     cfg_file_name)
        # print 'The project configuration file is written to', cfg_file_name


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
    dict_file = os.path.join(tm_folder, project_name + '.dict')
    ldac_file = os.path.join(tm_folder, project_name + '.ldac')
    cfg_file_name = os.path.join(cfg_folder, project_name + '.cfg')
    
    # Create file handler which logs debug messages
    if log_to_file: 
        log_file_name = os.path.join(cfg_folder, project_name + '.log')
        logging.basicConfig(filename=log_file_name, format=LOG_FORMAT, 
                            level=logging.DEBUG)
        print "Log file:", log_file_name
    else: 
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

    
    # Handling the project configuration file 
    
    logging.info('Indexing Configurations:')
    logging.info('Project: %s', project_name)
    logging.info('Number of LDA topics: %d', num_topics)
    logging.info('Number of LDA passes: %d', num_passes)
    logging.info('Number of LSA topics: %d', LSI_DEFAULT_NUM_TOPICS)

    config = ConfigParser.RawConfigParser()
    if os.path.exists(cfg_file_name): config.read(cfg_file_name)

    if not config.has_section('DATA'):
        config.add_section('DATA')
        config.set('DATA', 'name', project_name)
        config.set('DATA', 'root_dir', os.path.normpath(data_folder)) 
        config.set('DATA', 'project_dir', os.path.normpath(project_folder))
        config.set('DATA', 'output_folder', os.path.normpath(output_folder))   
        save_config(cfg_file_name, config)
    
    print "Indexing documents...."
    start_time = time.time()
    
    if not config.has_section('WHOOSH'):
        logging.info('================================= BEGIN WHOOSH INDEXING')
        
        if not os.path.exists(whoosh_folder): os.makedirs(whoosh_folder)
        path_index_file_name = os.path.join(project_folder, 
                                            project_name + '.path.index')
        
#         index_plain_text_emails(data_folder, path_index_file_name, 
#                                 whoosh_folder, lemmatize=lemmatize, 
#                                 stem=stem, nonascii=nonascii) 
        
        index_plain_text_emails2(data_folder, path_index_file_name, 
                                 whoosh_folder, stem, 
                                 min_token_len, max_token_len, 
                                 procs, limitmb, multisegment) 
            
        config.add_section('WHOOSH')
        config.set('WHOOSH', 'whoosh_index_dir', 
                   os.path.normpath(whoosh_folder))
        config.set('WHOOSH', 'path_index_file', 
                   os.path.normpath(path_index_file_name))
        config.set('WHOOSH', 'lemmatize', lemmatize)
        config.set('WHOOSH', 'stem', stem)
        config.set('WHOOSH', 'nonascii', nonascii)
        save_config(cfg_file_name, config)
        logging.info('================================= END WHOOSH INDEXING')

    print '\nIndexing time:', (time.time() - start_time), 'seconds'
    
    print "Corpus building...."
    start_time = time.time()

    if not config.has_section('CORPUS'):
        logging.info('=============================== BEGIN CORPUS BUILDING')
         
        if not os.path.exists(tm_folder): os.makedirs(tm_folder)
        path_index_file_name = os.path.join(tm_folder, 
                                            project_name + '.path.index') 
#         build_lda_corpus(whoosh_folder, path_index_file_name, dict_file, 
#                          ldac_file, min_token_freq, min_token_len, 
#                          max_token_len)
        
        build_lda_corpus2(whoosh_folder, path_index_file_name, dict_file, 
                         ldac_file, min_token_freq, min_token_len, 
                         max_token_len, stem)
         
        config.add_section('CORPUS')
        config.set('CORPUS', 'tm_folder', os.path.normpath(tm_folder))
        config.set('CORPUS', 'path_index_file', 
                   os.path.normpath(path_index_file_name))
        config.set('CORPUS', 'blei_corpus_file', os.path.normpath(ldac_file))
        config.set('CORPUS', 'dict_file', os.path.normpath(dict_file))
        config.set('CORPUS', 'vocab_file', 
                   os.path.normpath(ldac_file + '.vocab')) 
        config.set('CORPUS', 'min_token_freq', min_token_freq)
        config.set('CORPUS', 'min_token_len', min_token_len)
        config.set('CORPUS', 'max_token_len', 20)
        save_config(cfg_file_name, config) 
        logging.info('=============================== END CORPUS BUILDING')
     
    
    print '\nCorpus building time:', (time.time() - start_time), 'seconds'
    
    # project_name = os.path.normpath(project_name)
     
    print "Topic modeling...."
    start_time = time.time()
    
    if not config.has_section('LDA'):
        logging.info('=============================== BEGIN LDA ESTIMATION')
        lda_model_file = os.path.join(tm_folder, project_name + '.lda')
        lda_beta_file = os.path.join(tm_folder, project_name + '.lda.beta')
        lda_theta_file = os.path.join(tm_folder, project_name + '.lda.theta')
        lda_cos_index_file = os.path.join(tm_folder, 
                                          project_name + '.lda.cos.index')
        run_lda_estimation(dict_file, ldac_file, lda_model_file, lda_beta_file, 
                           lda_theta_file, lda_cos_index_file, num_topics, 
                           num_passes)
        config.add_section('LDA')
        config.set('LDA', 'lda_model_file', lda_model_file)
        config.set('LDA', 'lda_beta_file', lda_beta_file)
        config.set('LDA', 'lda_theta_file', lda_theta_file)
        config.set('LDA', 'lda_cos_index_file', lda_cos_index_file)
        config.set('LDA', 'num_topics', str(num_topics))
        config.set('LDA', 'num_passes', str(num_passes))    
        save_config(cfg_file_name, config)
        logging.info('=============================== END LDA ESTIMATION')    
     
     
     
#     logging.info('=============================== BEGIN LSI ESTIMATION')
#     
#     # Commented LSI due to an error from python interpreter on Feb 04, 2014
#  
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
# 
#     
#     logging.info('=============================== END LSI ESTIMATION')    
 
    if not config.has_section('TFIDF'):
        logging.info('=============================== BEGIN TFIDF')
        tfidf_theta_file = os.path.join(tm_folder, project_name + '.tfidf.theta')
        run_tfidf(dict_file, ldac_file, tfidf_theta_file)
        config.add_section('TFIDF')
        config.set('TFIDF', 'tfidf_file', tfidf_theta_file)
        save_config(cfg_file_name, config)
        logging.info('=============================== END TFIDF')    


    print '\nTopic modeling time:', (time.time() - start_time), 'seconds'

    
def index_data2(data_folder, output_folder, project_name, 
                num_topics=DEFAULT_NUM_TOPICS, num_passes=DEFAULT_NUM_PASSES, 
                min_token_freq=MIN_TOKEN_FREQ, min_token_len=MIN_TOKEN_LEN, 
                max_token_len=MAX_TOKEN_LEN, stem=False, procs=4, limitmb=512, 
                multisegment=True):
    
    def save_config(cfg_file_name, config):
        # Writing our configuration file
        with open(cfg_file_name, 'w') as configfile:
            config.write(configfile)
        logging.info('The project configuration file is written to %s', 
                     cfg_file_name)


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
    dict_file = os.path.join(tm_folder, project_name + '.dict')
    ldac_file = os.path.join(tm_folder, project_name + '.ldac')
    cfg_file_name = os.path.join(output_folder, project_name + '.cfg')
    
    
    # Handling the project configuration file 
    
    logging.info('Indexing Configurations:')
    logging.info('Project: %s', project_name)
    logging.info('LDA Number of topics: %d', num_topics)
    logging.info('LDA Number of passes: %d', num_passes)

    config = ConfigParser.RawConfigParser()
    if os.path.exists(cfg_file_name): config.read(cfg_file_name)

    if not config.has_section('DATA'):
        config.add_section('DATA')
        config.set('DATA', 'name', project_name)
        config.set('DATA', 'root_dir', os.path.normpath(data_folder)) 
        config.set('DATA', 'project_dir', os.path.normpath(project_folder))
        config.set('DATA', 'output_folder', os.path.normpath(output_folder))   
        save_config(cfg_file_name, config)
    
    #print "Indexing documents...."
    start_time = time.time()
    
    if not config.has_section('WHOOSH'):
        logging.info('================================= BEGIN WHOOSH INDEXING')
        
        if not os.path.exists(whoosh_folder): os.makedirs(whoosh_folder)
        path_index_file_name = os.path.join(project_folder, 
                                            project_name + '.path.index')
        
        index_plain_text_emails2(data_folder, path_index_file_name, 
                                 whoosh_folder, stem, 
                                 min_token_len, max_token_len, 
                                 procs, limitmb, multisegment) 
            
        config.add_section('WHOOSH')
        config.set('WHOOSH', 'whoosh_index_dir', 
                   os.path.normpath(whoosh_folder))
        config.set('WHOOSH', 'path_index_file', 
                   os.path.normpath(path_index_file_name))
        config.set('WHOOSH', 'stem', stem)
        save_config(cfg_file_name, config)
        logging.info('================================= END WHOOSH INDEXING')

    print '\nIndexing time:', (time.time() - start_time), 'seconds'
    
    #print "Corpus building...."
    start_time = time.time()

    if not config.has_section('CORPUS'):
        logging.info('=============================== BEGIN CORPUS BUILDING')
         
        if not os.path.exists(tm_folder): os.makedirs(tm_folder)
        path_index_file_name = os.path.join(tm_folder, 
                                            project_name + '.path.index') 
        
        build_lda_corpus2(whoosh_folder, path_index_file_name, dict_file, 
                         ldac_file, min_token_freq, min_token_len, 
                         max_token_len, stem)
         
        config.add_section('CORPUS')
        config.set('CORPUS', 'tm_folder', os.path.normpath(tm_folder))
        config.set('CORPUS', 'path_index_file', 
                   os.path.normpath(path_index_file_name))
        config.set('CORPUS', 'blei_corpus_file', os.path.normpath(ldac_file))
        config.set('CORPUS', 'dict_file', os.path.normpath(dict_file))
        config.set('CORPUS', 'vocab_file', 
                   os.path.normpath(ldac_file + '.vocab')) 
        config.set('CORPUS', 'min_token_freq', min_token_freq)
        config.set('CORPUS', 'min_token_len', min_token_len)
        config.set('CORPUS', 'max_token_len', 20)
        save_config(cfg_file_name, config) 
        logging.info('=============================== END CORPUS BUILDING')
     
    
    print '\nCorpus building time:', (time.time() - start_time), 'seconds'
     
    #print "Topic modeling...."
    start_time = time.time()
    
    if not config.has_section('LDA'):
        logging.info('=============================== BEGIN LDA ESTIMATION')
        lda_model_file = os.path.join(tm_folder, project_name + '.lda')
        lda_beta_file = os.path.join(tm_folder, project_name + '.lda.beta')
        lda_theta_file = os.path.join(tm_folder, project_name + '.lda.theta')
        lda_cos_index_file = os.path.join(tm_folder, 
                                          project_name + '.lda.cos.index')
        run_lda_estimation(dict_file, ldac_file, lda_model_file, lda_beta_file, 
                           lda_theta_file, lda_cos_index_file, num_topics, 
                           num_passes)
        config.add_section('LDA')
        config.set('LDA', 'lda_model_file', lda_model_file)
        config.set('LDA', 'lda_beta_file', lda_beta_file)
        config.set('LDA', 'lda_theta_file', lda_theta_file)
        config.set('LDA', 'lda_cos_index_file', lda_cos_index_file)
        config.set('LDA', 'num_topics', str(num_topics))
        config.set('LDA', 'num_passes', str(num_passes))    
        save_config(cfg_file_name, config)
        logging.info('=============================== END LDA ESTIMATION')    
 
    if not config.has_section('TFIDF'):
        logging.info('=============================== BEGIN TFIDF')
        tfidf_theta_file = os.path.join(tm_folder, project_name + '.tfidf.theta')
        run_tfidf(dict_file, ldac_file, tfidf_theta_file)
        config.add_section('TFIDF')
        config.set('TFIDF', 'tfidf_file', tfidf_theta_file)
        save_config(cfg_file_name, config)
        logging.info('=============================== END TFIDF')    


    print '\nTopic modeling time:', (time.time() - start_time), 'seconds'


if __name__=="__main__":
      
    arg_parser = argparse.ArgumentParser('''
      
    Whoosh index builder for email files  
  
    Examples: 
        python index_data_whoosh.py -h # for help 
        python index_data_whoosh.py -d "E:\\E-Discovery\\edrmv2txt-a-b" -o "E:\\E-Discovery\\" -p edrmv2txt-a-b-index-t50-2 -n 1 -t 50 -f 20 -m 2 -x 40 -l     
        python index_data_whoosh.py -d "E:\\E-Discovery\\trec2010seeds-wa\\201" -o "E:\\E-Discovery\\trec2010seeds-wa\\" -p Q201-SW-K10 -n 10 -t 10 -f 2 -m 2 -x 100 -s -l
    ''')
    arg_parser.add_argument("-d", dest="data_folder", type=str, 
                            help="data folder", required=True)
    arg_parser.add_argument("-o", dest="output_folder", type=str, 
                            help="output folder", required=True)
    arg_parser.add_argument("-p", dest="project_name", type=str, 
                            help="project name", required=True)
    arg_parser.add_argument("-t", dest="num_topics", type=int, 
                            help="number of topics (default %d)" % \
                            DEFAULT_NUM_TOPICS, default=DEFAULT_NUM_TOPICS)
    arg_parser.add_argument("-n", dest="num_passes", type=int, 
                            help="number of passes (default %d)" % \
                            DEFAULT_NUM_PASSES, default=DEFAULT_NUM_PASSES)
    arg_parser.add_argument("-f", dest="min_token_freq", type=int, 
                            help="minimum token frequency (default %d)" % \
                            MIN_TOKEN_FREQ, default=MIN_TOKEN_FREQ)
    arg_parser.add_argument("-m", dest="min_token_len", type=int, 
                            help="minimum token length (default %d)" % \
                            MIN_TOKEN_LEN, default=MIN_TOKEN_LEN)
    arg_parser.add_argument("-x", dest="max_token_len", type=int, 
                            help="maximum token length (default %d)" % \
                            MAX_TOKEN_LEN, default=MAX_TOKEN_LEN)
    arg_parser.add_argument("-s", dest="stem", action="store_true", 
                            help="stem tokens (default False)", default=False)
    arg_parser.add_argument("-z", dest="lemmatize", action="store_true", 
                            help="lemmatize tokens (default False)", 
                            default=False)
    arg_parser.add_argument("-a", dest="nonascii", action="store_true", 
                            help="allow non-ASCII tokens (default False)", 
                            default=False)
    arg_parser.add_argument("-l", dest="log", action="store_true", 
                            help="enable logging (default True)", default=True)
    args = arg_parser.parse_args()
      
    data_folder = os.path.normpath(args.data_folder)
    output_folder = os.path.normpath(args.output_folder)
    # Checks whether the output folder exists 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
      
    # Create file handler which logs debug messages
    if args.log: 
        log_file_name = os.path.join(output_folder, args.project_name + '.log')
        logging.basicConfig(filename=log_file_name, format=LOG_FORMAT, 
                            level=logging.DEBUG)
    else: 
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
        
  
    stime = time.time()
  
    index_data2(data_folder, output_folder, args.project_name, 
               args.num_topics, args.num_passes, args.min_token_freq, 
               args.min_token_len, args.max_token_len, stem=args.stem, 
               procs=6, limitmb=512, multisegment=True)
      
    print '\nTotal execution time:', (time.time() - stime)/60.0, 'minutes'
     


