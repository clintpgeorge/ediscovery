#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script performs LSI estimation on a given Blei corpus 


Created On: Feb 27, 2013
@author: Clint P. George 
'''

import sys 
import argparse
import logging
import os 
from tm.lsi_estimation import run_lsi_estimation




if __name__=="__main__":
    '''
    Performs LDA estimation process 
    '''
    
    log_file = 'run_lsi.log'
    
    arg_parser = argparse.ArgumentParser('''
    Performs LSI estimation

    Examples: 
        python run_lsi.py -h # for help 
        python run_lsi.py -l -d /home/cgeorge/data/tm -c enron.ldac -w enron.dict -m enron.lsi -b enron.lsi.beta -t enron.lsi.theta -i enron.lsi.cos.index -n 300   

    ''')
    arg_parser.add_argument("-d", dest="data_folder", type=str, help="The data folder", required=True)
    arg_parser.add_argument("-c", dest="ldac_file", type=str, help="LDA corpus file", required=True)
    arg_parser.add_argument("-w", dest="dict_file", type=str, help="Dictionary file", required=True)
    arg_parser.add_argument("-m", dest="model_file", type=str, help="LSI model file (out)", required=True)
    arg_parser.add_argument("-b", dest="beta_file", type=str, help="Topics file (out)", required=True)
    arg_parser.add_argument("-t", dest="theta_file", type=str, help="Theta file (out)", required=True)
    arg_parser.add_argument("-i", dest="index_file", type=str, help="LSI cosine index file (out)", required=True)
    arg_parser.add_argument("-n", dest="num_topics", type=int, help="Number of topics", default=50)
    arg_parser.add_argument("-l", "--log", dest="log", default=False, action="store_true", help="log details into a file")
    arg_parser.add_argument("-f", dest="log_file", type=str, help="logs file (default: run_lsi.log)", default='run_lsi.log')
    
    args = arg_parser.parse_args()
    
    
    if not os.path.exists(args.data_folder):
        print "Please provide a valid data folder!"
        sys.exit(1)

    # Setup the output folder and files     
    dict_file = os.path.join(args.data_folder, args.dict_file)
    ldac_file = os.path.join(args.data_folder, args.ldac_file)
    model_file = os.path.join(args.data_folder, args.model_file)   
    beta_file = os.path.join(args.data_folder, args.beta_file)   
    theta_file = os.path.join(args.data_folder, args.theta_file)   
    index_file = os.path.join(args.data_folder, args.index_file)  

    # create file handler which 
    # logs even debug messages
    
    if args.log: 
        logging.basicConfig(filename=args.log_file, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    else: 
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        
    
    
    logging.info('=============================================================================================================')
    run_lsi_estimation(dict_file, ldac_file, model_file, beta_file, theta_file, index_file, args.num_topics)
    logging.info('=============================================================================================================')
