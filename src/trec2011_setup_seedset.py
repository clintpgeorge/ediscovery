'''
This script filters email documents from the Enron 
dataset using the seed index file that is given 
for TREC 2011 Legal Learning Track 

The seed document has two columns: 
    (1) R or N (indicating responsive or nonresponsive, respectively)
    (2) docid  (the TREC docid)

Created by: Clint P. George
Created on: Feb 08, 2014 
 
'''

import os
import shutil
import sys 

from collections import defaultdict

##################################################################
## Edit the following lines before executing this script  
##################################################################

data_dir = "E:\\E-Discovery\\trec2010dataset\\edrmv2txt-v2" # 
seed_index_fp = "E:\\E-Discovery\\trec2011dataset\\rel."
seed_set_ids = ["401", "402", "403"]
output_dir = "E:\\E-Discovery\\trec2011dataset\\seeds"

##################################################################


log_file = os.path.join(output_dir, "error.log") # log file 
data_index_file = os.path.join(output_dir, "files.csv") # data index file 

if not os.path.exists(data_dir):
    print "Please provide a valid data folder!"
    sys.exit(1)
    

    
# Checks whether the output folder exists 

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    

# Building an index for the files in the dataset 

file_paths = defaultdict(str)
num_files = 1 # number of files in the dataset 
num_duplicate_files = 0 # number of duplicate file instances 
doc_id = 0

print "Indexing data folder:"
with open(data_index_file, "w") as fw: 
    for (dir_path, dir_names, file_names) in os.walk(data_dir):
        
        print "Processing folder:", dir_path, \
            "Number of subfolders:", len(dir_names), \
            "Number of files:", len(file_names)  
            
        for file_name in file_names:
            fn, _ = os.path.splitext(file_name)
            if fn in file_paths:
                num_duplicate_files += 1
            else: 
                file_path = os.path.join(dir_path, file_name)
                file_paths[fn] = file_path
                print >>fw, ",".join([str(doc_id), fn, file_path])
                doc_id += 1
                
            num_files += 1 
        
print "Total file count:", num_files
print "Duplicate files:", num_duplicate_files
print "See index in:", data_index_file
print 

num_rows = 0
num_seeds = 0 
ld = {"N":"0", "R":"1"} # directory names for responsive 
                        # and non-responsive documents  

print "Copying seeds:" 

with open(log_file, "w") as fl: 
    
    for seed_set_id in seed_set_ids:

        seed_index_file = seed_index_fp + seed_set_id
        
        if not os.path.exists(seed_index_file):
            print "Please provide a valid seed index file!"
            sys.exit(1)
            
        with open(seed_index_file) as fs:         
            
            for line in fs:
                
                (label, file_name) = line.strip().split(" ")
                
                # this is adhoc method to check whether 
                # the file is an attachment 
                # TODO: to be improved  
                if len(file_name.split(".")) > 3: 
                    print >>fl, ",".join([seed_set_id, file_name, label, "attachment"])
                else:             
                    if file_name in file_paths: 
                        # the file exists in the dataset 
                        dest_dir = os.path.join(output_dir, seed_set_id, ld[label])
                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)                 
                        shutil.copy(file_paths[file_name], dest_dir)
                        
                        if (num_seeds % 100) == 0: print ".",
                        num_seeds += 1
                    else: 
                        # the file not exists in the dataset 
                        print >>fl, ",".join([seed_set_id, file_name, label, "file-not-exists"])
    
                num_rows += 1
                
print 
print "Number of copied seeds:", num_seeds, "out of", num_rows
print "See log in:", log_file



        