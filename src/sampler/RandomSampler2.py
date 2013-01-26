#!/usr/bin/env python2.7

import sys
import os
import shutil
import math
import random

# input:
# inputFolder/pst = Source of the datasets
# confidence: float between 0 & 1,
# precision: confidence: float between 0 & 1  
def main():
	if len(sys.argv) != 4:
		sys.stderr.write("Please enter input in expected format: RandomSampler inputFolder, confidence, precision")
		sys.exit(1)
	else:
	#checking for input
		try:
			# evaluating input for testing, will change in final system
			inputFolder = sys.argv[1]
			
			
			confidence = float(sys.argv[2])
			precision = float(sys.argv[3])
		
			if not os.path.exists(inputFolder) : 
				print "Input folder cannot be found"
			if confidence <= 0 or confidence > 1:
				raise Exception, "Confidence is not valid, enter as a probability between 0 and 1"
			if precision <= 0 or precision > 1:
				raise Exception, "Precision is not valid, enter as a probability between 0 and 1"
			
			
			fileList = FindFilesInFolder(inputFolder) 
			#change to required constant for testing
			SEEDCONSTANT = 0.5
			messageRandomSample = RandomSampler(fileList,confidence,precision,SEEDCONSTANT)
			#currently constant
			outputDir= "C:\\Users\\abhiramj\\Desktop\\sample"
			CopyRandomFiles(outputDir,messageRandomSample)
			return messageRandomSample			
			
		except Exception as anyException:
			print "Error: " + str(anyException)
			sys.exit(1)
			
	
# Recursive descent to find files in folder.
# Input is input folder, output is absolute path of all files
# Output is list of absolute path of all files
def FindFilesInFolder(inputDir):
	fileList = []
	for root,dir,files in os.walk(inputDir):
		for file in files:
			fileList.append(os.path.join(root,file))
	print "Found " + str(len(fileList)) + " files"
	return fileList

# SEEDCONSTANT unused currently
def RandomSampler(messageIdList,confidence,precision,SEEDCONSTANT):
	# Uncomment to test sample size of big numbers and verify
	# messageIdList = xrange(10000)
	random(SEEDCONSTANT)
	
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
	
	
	
	# prevalence is the likelihood of finding a responsive/positive example in population
	# We assume this as 0.5 (most conservative) as we do not know prior information about data
	prevalence = 0.5
	
	# check that the confidence interval is supported
	if confidence in z:
		# sample size formula based on infinite population
		sampleSize= pow(z[confidence],2)*(prevalence)*(1-prevalence)/(pow(precision,2))
		
		# correction for finite size
		correctedSampleSize = sampleSize/(1+ (sampleSize-1)/len(messageIdList))
		correctedSampleSize = int(math.ceil(correctedSampleSize))
		print "Sample size is "+ str(correctedSampleSize)
		randomSample = random.sample(messageIdList,correctedSampleSize)
		return randomSample
	else:
		raise Exception, "Confidence interval not supported"
		sys.exit(1)
		
# Copies the random files to a given folder		
def CopyRandomFiles(dir,randomList):
	print "Now creating directory and copying .... "
	if not os.path.exists(dir):
		os.mkdir(dir)
	i=1
	for file in randomList:
		currFileName = os.path.basename(file)
		shutil.copy2(file,dir)
		os.rename(os.path.join(dir,currFileName),os.path.join(dir,currFileName+"--"+str(i)))
		i+=1
	print "Copying complete"
	return

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
	main()