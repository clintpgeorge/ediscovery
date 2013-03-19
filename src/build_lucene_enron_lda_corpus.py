#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script builds an LDA corpus from 
the Lucene indexed documents  


Created On: Feb 27, 2013
@author: Clint P. George 
'''

import sys 
import argparse
import logging
import os 
from preprocess.lucene_enron_create_corpus import build_lda_corpus


if __name__=="__main__":
    '''
    The main function: Here we only consider the Enron data set 
    '''
    arg_parser = argparse.ArgumentParser('''
    Enron corpus builder for topic models

    Examples: 
        python build_lucene_enron_lda_corpus.py -h # for help 
        python build_lucene_enron_lda_corpus.py -l -d /home/cgeorge/ediscovey/enron/lucene -o /home/cgeorge/ediscovey/enron/tm 

    ''')
    arg_parser.add_argument("-d", dest="index_folder", type=str, help="data folder", required=True)
    arg_parser.add_argument("-o", dest="output_folder", type=str, help="output folder", required=True)
    arg_parser.add_argument("-p", dest="output_prefix", type=str, help="output (default: enron)", default='enron')
    arg_parser.add_argument("-l", "--log", dest="log", default=False, action="store_true", help="log details into a file")
    arg_parser.add_argument("-f", dest="log_file", type=str, help="logs file (default: build_lucene_enron_lda_corpus.log)", default='build_lucene_enron_lda_corpus.log')
    arg_parser.add_argument("-w", dest="stop_words_file", type=str, help="stop words file (default: en_stopwords)", default='en_stopwords')
    arg_parser.add_argument("-m", dest="min_frequency", type=int, help="minimum frequency of vocabulary terms (default: 15)", default=15)
    arg_parser.add_argument("-i", dest="min_word_len", type=int, help="minimum length of vocabulary terms (default: 2)", default=2)    
    args = arg_parser.parse_args()
    
    
    if not os.path.exists(args.index_folder):
        print "Please provide a valid data folder!"
        sys.exit(1)
    if not os.path.exists(args.stop_words_file):
        print "Please provide a valid stop words file!"
        sys.exit(1)
        

    # Setup the output folder and files     
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    dictionary_file = os.path.join(args.output_folder, args.output_prefix + '.dict')
    ldac_file = os.path.join(args.output_folder, args.output_prefix + '.ldac')
    path_file = os.path.join(args.output_folder, args.output_prefix + '.path.index')   


    # Creates file handler which 
    # logs even debug messages
    if args.log: 
        logging.basicConfig(filename=args.log_file, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    else: 
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

    
    logging.info('=============================================================================================================')
    build_lda_corpus(args.index_folder, path_file, args.stop_words_file, dictionary_file, ldac_file, args.min_frequency, args.min_word_len)
    logging.info('=============================================================================================================')


