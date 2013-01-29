#!/usr/bin/env python2.7
'''
TODO: (1) Add description ???

Created by: Abhiram J.  
Created On: Jan 28, 2013   

'''

import os
import shutil

def copy_random_files(dir_path,random_list):
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
