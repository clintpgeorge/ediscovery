#!/usr/bin/env python2.7
'''
This script has all the basic file access/process 
utility functions 

Created by: Abhiram J.  
Created On: Jan 28, 2013   

Modified by: Clint P. George 
Modified On: Feb 28, 2013 

'''

import os
import shutil
import ConfigParser

def nexists(file_path):
    '''
    Checks whether a particular file path 
    exists. It can handle the 'NoneType' input 
    '''
    
    if file_path <> None:
        if os.path.exists(file_path):
            return True
        
    return False
        
    

def copy_files_with_dir_tree(lcp, file_paths, output_dir_path, in_file_prefix=''):
    '''Copies the files given in path list into 
    the specified output directory. The directory structure 
    is preserved during this process. 
    
    Returns: 
        None 
        
    Arguments: 
        lcp - input directory 
        file_paths - list of files paths 
        output_dir_path - the output directory path 
    '''
    
    # find the longest common prefix (LCP)
    # lcp = os.path.commonprefix(file_paths) 
    
    for src_file_path in file_paths:
        s_fp = os.path.relpath(src_file_path, lcp)#src_file_path[len(lcp):] # ignores LCP from path   
        dest_dp, _ = os.path.split(s_fp) # to preserve source files directory structure 
        dest_dir_path = os.path.join(output_dir_path, dest_dp)

        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path)
        
        if in_file_prefix <> '':            
            src_file_path = os.path.join(in_file_prefix, src_file_path)
        
        shutil.copy2(src_file_path, dest_dir_path)


def find_files_in_folder(input_dir):
    '''Recursive descent to find files in folder.
    
    Returns: 
        a list of absolute path of all files
    Arguments: 
        input_dir - the input folder
    '''
    
    
    file_list = []
    
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            file_list.append(os.path.join(root, file_name))
    
    return file_list


def get_file_paths_index(input_dir):
    '''
    Recursive descent to find files in folder.
    
    Returns: 
        a list of (idx, root, file_name) 
    Arguments: 
        input_dir - the input folder
    '''
    
    idx = 0 
    file_path_tuples = []
    
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            file_path_tuples.append((idx, root, file_name))
            idx += 1
    
    return file_path_tuples


def store_file_paths_index(index_file, file_path_tuples):
    '''
    Stores the email paths into a text 
    file for future reference. 
    
    Returns: 
        None 
    Arguments: 
        index_file - the index file name 
        file_path_tuples - list of (idx, root, file_name) 
    ''' 
    with open(index_file, 'w') as fw:
        for ft in file_path_tuples: 
            (idx, root, file_name) = ft
            
            fw.write(str(idx)+";"+str(root)+";"+str(file_name)+"\n")


def load_file_paths_index(index_file):
    '''
    Reads the file paths index file 
    and stores into a list 
    
    Returns: 
        file_path_tuples - list of (idx, root, file_name) 
    Arguments: 
        index_file - the index file name 
    ''' 
    file_path_tuples = []
    
    with open(index_file) as fp:
        for line in fp: 
            (idx, root, file_name) = line.strip().split(";") # ";"
            file_path_tuples.append((int(idx), os.path.normpath(root), file_name))
    
    return file_path_tuples


def read_config(file_name):
    '''
    Reads configurations from the given file
    
    Arguments: 
        file_name - the configuration file 
    Returns: 
        config_dict - configurations as a dictionary object 
    '''
    
    config = ConfigParser.ConfigParser()
    config.read(file_name)
    config_dict = {}
    
    for section in config.sections():
        options_dict = {}
        for option in config.options(section):
            try:
                options_dict[option] = config.get(section, option)
                if options_dict[option] == -1: print "skip: %s" % option
            except:
                print("exception on %s!" % option)
                options_dict[option] = None
        config_dict[section] = options_dict
    
    return config_dict


