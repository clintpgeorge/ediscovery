#!/usr/bin/env python2.7
'''
This samples a folder specified by the user and generates a random sample from the folder which agrees
with a user given confidence and precision. The mathematical details are covered here: 

1) http://www.surveysystem.com/sample-size-formula.htm
2) http://www.edrm.net/resources/guides/edrm-search-guide/appendix-2

Created by: Abhiram J.  
Created On: Jan 28, 2013   

'''
import sys
import os
import math
import random
import argparse
import datetime
import logging
from file_utils import find_files_in_folder, copy_random_files
from decimal import Decimal

# setting up z , the diction of confidence -> zvalues
SUPPORTED_CONFIDENCES = {}
SUPPORTED_CONFIDENCES[Decimal('0.999')] = 3.3
SUPPORTED_CONFIDENCES[Decimal('0.99')] = 2.577
SUPPORTED_CONFIDENCES[Decimal('0.985')] = 2.43
SUPPORTED_CONFIDENCES[Decimal('0.975')] = 2.243
SUPPORTED_CONFIDENCES[Decimal('0.95')] = 1.96
SUPPORTED_CONFIDENCES[Decimal('0.90')] =1.645
SUPPORTED_CONFIDENCES[Decimal('0.85')] = 1.439
SUPPORTED_CONFIDENCES[Decimal('0.75')] = 1.151

DEFAULT_CONFIDENCE_LEVEL = Decimal('95.000')
DEFAULT_CONFIDENCE_INTERVAL = 5.0

# PREVALENCE is the likelihood of finding a responsive/positive example in population
# We assume this as 0.5 (most conservative) as we do not know prior information about data
PREVALENCE = 0.5
logger = logging.getLogger('random_sampler_test_function')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)
logger.addHandler(ch)

# input:
# inputFolder/pst = Source of the datasets
# confidence: float between 0 & 1,
# precision: confidence: float between 0 & 1
def main():
	
	
	timestamp = datetime.datetime.now()
	arg_parser = argparse.ArgumentParser('Random sample test function:')
	arg_parser.add_argument("-d", dest="input_folder", type=str,
						    help="the root directory for all the mails",
						    required=True)
	arg_parser.add_argument("-c", dest="confidence", type=float,
						    help="The confidence interval eg. 0.95 for 95%",
						    required=True)
	arg_parser.add_argument("-p", dest="precision", type=float,
						    help="The precision for the interval eg. 0.02 precision for\
						    .95 confidence gives 95%  +/-2% error",
						    required=True)
	arg_parser.add_argument("-o", dest="output_dir", type=str, help="Output directory of samples",
						    default="/home/abhiramj/code/temp/samples",
						    required=False)
	args = arg_parser.parse_args()
	
	if  not os.path.isdir(args.output_dir):
		logger.debug("Making output directory" + args.output_dir)
		os.makedirs(args.output_dir)
	
	file_handle = logging.FileHandler(os.path.join(args.output_dir,'random_sampler_test_function--' +str(timestamp)+'.log'))
	file_handle.setLevel(logging.INFO)
	file_handle.setFormatter(formatter)
	logger.addHandler(file_handle)
	
	logger.info("Args are: ")
	logger.info("input_folder: "+ args.input_folder)
	logger.info("confidence: "+ str(args.confidence))
	logger.info("precision: "+ str(args.precision))
	logger.info("output_dir: "+ args.output_dir)
	

	if not os.path.exists(args.input_folder) :
		logger.error("Exiting with error: Input folder cannot be found")
		raise Exception, "Input folder cannot be found"
	if args.confidence <= 0 or args.confidence > 1:
		logger.error("Exiting with error: Confidence is not valid, enter as a probability between 0 and 1")
		raise Exception, "Confidence is not valid, enter as a probability between 0 and 1"
	if args.precision <= 0 or args.precision > 1:
		logger.error( "Exiting with error: Precision is not valid, enter as a probability between 0 and 1")
		raise Exception, "Precision is not valid, enter as a probability between 0 and 1"


	file_list = find_files_in_folder(args.input_folder)
	message_random_sample = random_sampler(file_list,args.confidence,args.precision,SEEDCONSTANT=0.5)
	
	
	file_destination_dir = args.output_dir +"--"+ str(timestamp)
	copy_random_files(file_destination_dir,message_random_sample)
	return message_random_sample





def random_sampler(message_id_list, confidence, precision, SEEDCONSTANT):
	'''
	Returns a random sample as a list from an input list with certain precision and confidence
	
	Returns: 
		Random sample as a list
	Arguments:
	        message_id_list: list of inputs to sample from
	        confidence: Confidence expressed out of 1. Example: 0.95 for 95%. See documentation
	        at top of file for details.
	        precision: Precision expressed out of 1. Example: 0.04 for +/- 4%.See documentation
	        at top of file for details.
		
	'''

	random.seed(SEEDCONSTANT)


	# check that the confidence interval is supported
	if confidence in SUPPORTED_CONFIDENCES:
		# sample size formula based on infinite population
		sample_size= pow(SUPPORTED_CONFIDENCES[confidence],2)*(PREVALENCE)*(1-PREVALENCE)/(pow(precision,2))

		# correction for finite size
		corrected_sample_size = sample_size/(1 + (sample_size-1)/len(message_id_list))
		corrected_sample_size = int(math.ceil(corrected_sample_size))
		logger.info("Sample size is " + str(corrected_sample_size))
		print "Sample size is " + str(corrected_sample_size)
		random_sample = random.sample(message_id_list,corrected_sample_size)
		return random_sample
	else:
		logger.debug("Exiting with reason: Confidence interval not supported")
		raise Exception, "Confidence interval not supported"
		sys.exit(1)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
	main()
