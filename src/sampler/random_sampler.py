#!/usr/bin/env python2.7

'''

TODO: If this is an obsolete function delete it from repository 

'''

import sys
import math
import random

# PREVALENCE is the likelihood of finding a responsive/positive example in population
# We assume this as 0.5 (most conservative) as we do not know prior information about data
PREVALENCE = 0.5

# input: messageIdList: comma separated list of values(no spaces), confidence: float between 0 & 1, precision: confidence: float between 0 & 1  
def main():
	
	
	if len(sys.argv) != 4:
		sys.stderr.write("Please enter input in expected format: random_sampler messageidlist, confidence, precision")
		sys.exit(1)
	else:
	#checking for input
		try:
			# evaluating input for testing, will change in final system
			message_id_list = sys.argv[1].split(",")
			
			
			confidence = float(sys.argv[2])
			precision = float(sys.argv[3])
		
			if len(message_id_list) <= 0: 
				print "MessageId is not a list, interpreting as a range"
			if confidence <= 0 or confidence > 1:
				raise Exception, "Confidence is not valid, enter as a probability between 0 and 1"
			if precision <= 0 or precision > 1:
				raise Exception, "Precision is not valid, enter as a probability between 0 and 1"
			
			#change to required constant for testing
			SEEDCONSTANT = 0.5
			message_random_sample = random_sampler(message_id_list,confidence,precision,SEEDCONSTANT)
			return message_random_sample			
			
		except Exception as anyException:
			print "Error: " + anyException
			sys.exit(1)
			
	
		

		


# SEEDCONSTANT unused currently
def random_sampler(message_id_list,confidence,precision,SEEDCONSTANT):
	
	
	# Uncomment to test sample size of big numbers and verify
	# message_id_list = xrange(10000)
	random.seed(SEEDCONSTANT)
	
	# setting up z , the diction of confidence -> zvalues
	z = {}
	z[0.999] = 3.3
	z[0.99] =2.577
	z[0.985] =2.43
	z[0.975] = 2.243
	z[0.95]= 1.96
	z[0.90] =1.645
	z[0.85] = 1.439
	z[0.75] = 1.151
	
	
	
	
	# check that the confidence interval is supported
	if confidence in z:
		# sample size formula based on infinite population
		sample_size= pow(z[confidence],2)*(PREVALENCE)*(1-PREVALENCE)/(pow(precision,2))
		
		# correction for finite size
		corrected_sample_size = sample_size/(1+ (sample_size-1)/len(message_id_list))
		corrected_sample_size = int(math.ceil(corrected_sample_size))
		print "Sample size is "+ str(corrected_sample_size)
		random_sample = random.sample(message_id_list,corrected_sample_size)
		return random_sample
	else:
		raise Exception, "Confidence interval not supported"
		sys.exit(1)
		
	


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()