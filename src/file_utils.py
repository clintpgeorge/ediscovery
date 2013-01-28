import sys
import os
import shutil

# Copies the random files to a given folder
# Throws error for sample already existing. Need to fix
def copy_random_files(dir,random_list):
    
    
    try:
        if  not os.path.exists(dir):
            os.makedirs(dir)
        i = 1
        for file in random_list:
            curr_file_name = os.path.basename(file)
            shutil.copy2(file,dir)
            # Do rename to avoid overwriting files with same name
            os.rename(os.path.join(dir,curr_file_name),os.path.join(dir,curr_file_name+"--"+str(i)))
            i += 1
    except OSError:
            print str(OSError)
            print "Cannot copy the required files. Check that destination directory is empty"
    return


# Recursive descent to find files in folder.
# Input is input folder, output is absolute path of all files
# Output is list of absolute path of all files
def find_files_in_folder(input_dir):
    
    
    file_list = []
    for root,dir,files in os.walk(input_dir):
        for file in files:
            file_list.append(os.path.join(root,file))
    return file_list
