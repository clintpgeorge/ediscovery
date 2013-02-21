#!/usr/bin/env python2.7
'''
TODO: (1) Add description ???

Created by: Abhiram J.  
Created On: Jan 28, 2013   

'''

import os
import shutil
import ConfigParser

def copy_files_with_dir_tree(file_paths, output_dir_path, in_file_prefix=''):
    '''Copies the files given in path list into 
    the specified output directory. The directory structure 
    is preserved during this process. 
    
    Returns: 
        None 
        
    Arguments: 
        file_paths - list of files paths 
        output_dir_path - the output directory path 
    '''
    
    # find the longest common prefix (LCP)
    lcp = os.path.commonprefix(file_paths) 
    
    for src_file_path in file_paths:
        s_fp = src_file_path[len(lcp):] # ignores LCP from path   
        dest_dp, _ = os.path.split(s_fp)
        dest_dir_path = os.path.join(output_dir_path, dest_dp)

        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path)
        
        if in_file_prefix <> '':
            src_file_path = os.path.join(in_file_prefix, src_file_path)
        
        shutil.copy2(src_file_path, dest_dir_path)


def copy_random_files(dir_path, random_list):
    '''Copies the random files to a given folder. 
    
    TODO: Throws error for sample already existing. Need to fix
    
    Returns: 
        ??
    Arguments: 
        ??
    '''
    try:
        if  not os.path.exists(dir_path):
            os.makedirs(dir_path)
        i = 1
        for file_name in random_list:
            curr_file_name = os.path.basename(file_name)
            shutil.copy2(file_name, dir_path)
            # Do rename to avoid overwriting files with same name
            os.rename(os.path.join(dir_path, curr_file_name), os.path.join(dir_path, curr_file_name + "--" + str(i)))
            i += 1
    except OSError:
            print str(OSError)
            print "Cannot copy the required files. Check that destination directory is empty"
    return


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



def read_config(file_name):
    
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



