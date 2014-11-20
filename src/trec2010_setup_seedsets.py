'''
This script filters email documents from the Enron 
dataset using the seed index file that is given 
for TREC 2010 Legal Learning Track 

The seed document has four columns: 
    (1) The XML document id of the containing email 
    (augmented by the md5 sum, if the document 
    is an attachment).
    (2) The topic number (from 200 to 207)
    (3) The assessment (1 = responsive; 0 = not 
    responsive; -1 = not assessed; -2 = not assessed)
    (4) The XML document id for the document  



Created by: Clint P. George
Created on: Feb 08, 2014 
 
'''

import os
import csv
import shutil
import sys 

from collections import defaultdict

def _build_file_index(data_dir):
    '''
    Building an index for the files in the data directory 
    '''
    file_path_dict = defaultdict(str)
    num_files = 1 # number of files in the dataset 
    num_duplicate_files = 0 # number of duplicate file instances 
    doc_id = 0
    
    print "Indexing data folder:"
    for (dir_path, dir_names, file_names) in os.walk(data_dir):
        print "Processing folder:", dir_path, "Number of subfolders:", \
            len(dir_names), "Number of files:", len(file_names)  
        for file_name in file_names:
            fn, _ = os.path.splitext(file_name)
            if fn in file_path_dict:
                num_duplicate_files += 1
            else: 
                file_path = os.path.join(dir_path, file_name)
                file_path_dict[fn] = file_path
                doc_id += 1
                
            num_files += 1 
            
    print "Total file count:", num_files
    print "Duplicate files:", num_duplicate_files
    print 
    
    return file_path_dict


def copy_seeds_no_attachments(data_dir, seed_index_file, log_file, output_dir):
    """
    Copying seeds (ignores attachments)
    
    """ 
    
    file_path_dict = _build_file_index(data_dir)
    
    num_rows = 0
    num_seeds = 0 
    
    print "Copying seeds (ignores attachments):" 
    with open(seed_index_file) as fs: 
        with open(log_file, "w") as fl: 
              
            csv_reader = csv.reader(fs)
            for row in csv_reader:
                (doc_id, seed_set_id, label, file_name) = row # see the help 
                  
                # Ignores email attachments 
                # Ignores assessments -1, -2 
                if (label in ["1", "0"]) and (doc_id == file_name) and (len(file_name.split(".")) < 4):
                    if file_name in file_path_dict: 
                        # the file exists in the dataset 
                        dest_dir = os.path.join(output_dir, 
                                                seed_set_id, label)
                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)
                          
                        shutil.copy(file_path_dict[file_name], dest_dir)
                        if (num_seeds % 100) == 0: print ".",
                        num_seeds += 1
                    else: 
                        # the file not exists in the dataset 
                        print >>fl, ",".join([doc_id, seed_set_id, label, file_name, "file-not-exists"])
                         
                elif label not in ["1", "0"]: 
                    # Ignores the assessments -1, -2
                    print >>fl, ",".join([doc_id, seed_set_id, label, file_name, "not-assessed"])
                     
                elif (doc_id <> file_name) or (len(file_name.split(".")) > 3): 
                    # TODO: This is adhoc method to check whether 
                    # the file is an attachment. To be improved                 
                    print >>fl, ",".join([doc_id, seed_set_id, label, file_name, "attachment"])
                 
                num_rows += 1
    print 
     
    print "Number of copied seeds:", num_seeds, "out of", num_rows
    print "See log in:", log_file
         
         

def copy_seeds(data_dir, seed_index_file, log_file, output_dir):
    
    file_path_dict = _build_file_index(data_dir)
    
    num_rows = 0
    num_seeds = 0 
    
    print "Copying seeds:" 
    with open(seed_index_file) as fs: 
        with open(log_file, "w") as fl: 
             
            csv_reader = csv.reader(fs)
            for row in csv_reader:
                (doc_id, seed_set_id, label, file_name) = row # see the help 
    
                if (label in ["1", "0"]):
                    if file_name in file_path_dict: 
                        # the file exists in the dataset 
                        dest_dir = os.path.join(output_dir, seed_set_id, label)
                        if not os.path.exists(dest_dir): os.makedirs(dest_dir)
                         
                        shutil.copy(file_path_dict[file_name], dest_dir)
                        if (num_seeds % 100) == 0: print ".",
                        num_seeds += 1
                    else: 
                        # the file not exists in the dataset 
                        print >>fl, ",".join([doc_id, seed_set_id, label, file_name, "file-not-exists"])
                        
                elif label not in ["1", "0"]: 
                    # Ignores the assessments -1, -2
                    print >>fl, ",".join([doc_id, seed_set_id, label, file_name, "not-assessed"])
                
                num_rows += 1
    print 
    
    print "Number of copied seeds:", num_seeds, "out of", num_rows
    print "See log in:", log_file


##################################################################
## Edit the following lines before executing this script  
##################################################################

data_dir = "E:\\E-Discovery\\edrmv2txt-v2" # 
seed_index_file = "E:\\E-Discovery\\trec2010dataset\\seed-v2.csv"
output_dir = "E:\\E-Discovery\\trec2010seeds-wa"

##################################################################


log_file = os.path.join(output_dir, "error.log") # log file 


if not os.path.exists(data_dir):
    print "Please provide a valid data folder!"
    sys.exit(1)
    
if not os.path.exists(seed_index_file):
    print "Please provide a valid seed index file!"
    sys.exit(1)
    
# Checks whether the output folder exists 

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    

copy_seeds(data_dir, seed_index_file, log_file, output_dir)


    

