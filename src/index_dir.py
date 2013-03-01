#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script is used to index all files 
in a given folder using the Lucene index.   

Created On: Feb 28, 2013
@author: Clint P. George 
'''

import os 
import sys 
import argparse
import logging 
from lucenesearch.lucene_index_dir import index_plain_text_emails

if __name__=="__main__":
    '''
    The main function
    '''

    
    arg_parser = argparse.ArgumentParser('''
    Lucene index builder for email files  

    Examples: 
        python index_dir.py -h # for help 
        python index_dir.py -l -d /media/Store/Research/datasets/es/maildir/ -o /media/Store/Research/datasets/es/lucene -p /media/Store/Research/datasets/es/enron.path.index    

    ''')
    arg_parser.add_argument("-d", dest="data_folder", type=str, help="the data folder", required=True)
    arg_parser.add_argument("-o", dest="index_folder", type=str, help="the output folder", required=True)
    arg_parser.add_argument("-p", dest="path_index_file", type=str, help="File paths index file", required=True)
    arg_parser.add_argument("-l", "--log", dest="log", default=False, action="store_true", help="log details into a file")
    arg_parser.add_argument("-f", dest="log_file", type=str, help="Logs file (default: index_dir.log)", default='index_dir.log')
    args = arg_parser.parse_args()
    
    if not os.path.exists(args.data_folder):
        print "Please provide a valid data folder!"
        sys.exit(1)
    if not os.path.exists(args.index_folder):
        os.makedirs(args.index_folder)
    

    # create file handler which 
    # logs debug messages
    if args.log: 
        logging.basicConfig(filename=args.log_file, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    else: 
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
        


        
    logging.info('=============================================================================================================')
    index_plain_text_emails(args.data_folder, args.path_index_file, args.index_folder)
    logging.info('=============================================================================================================')


