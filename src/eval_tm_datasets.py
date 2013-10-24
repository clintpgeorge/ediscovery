'''
Created on Oct 22, 2013

@author: Clint
'''

import os 
import numpy as np 
from utils.utils_file import read_config, load_file_paths_index

RELEVANT_CLASS_ID = 0
IRRELEVANT_CLASS_ID = 1

def get_tm_classification_dataset(mdl_cfg_file, positive_dir):   
    
    mdl_cfg = read_config(mdl_cfg_file)

    lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']    
    lda_file_path_index = load_file_paths_index(path_index_file)    
    lda_theta = np.loadtxt(lda_theta_file, dtype=np.float)
    num_docs, num_topics = lda_theta.shape
    
    print 'LDA Theta: Number of documents ', num_docs, ' number of topics ', num_topics  
    
    class_ids = np.zeros(num_docs)
    file_paths = [] 
    for i, (_, root, file_name) in enumerate(lda_file_path_index):
        if positive_dir == root: # os.path.exists(os.path.join(positive_dir, file_name)):
            class_ids[i] = RELEVANT_CLASS_ID
        else:
            class_ids[i] = IRRELEVANT_CLASS_ID
        file_paths.append(os.path.join(root, file_name))

        
    return (class_ids, lda_theta, file_paths)



def get_random_train_test(class_ids, features, test_perc = 0.4):
    
    num_samples = len(class_ids)
    random_indices = np.random.permutation(range(0, num_samples))
    
    test_count = int(test_perc * num_samples)
    test_indices = random_indices[0:test_count] 
    train_indices = random_indices[test_count:num_samples]
    test_y, test_x = class_ids[test_indices], features[test_indices]
    train_y, train_x = class_ids[train_indices], features[train_indices]
    
    return test_y, test_x, train_y, train_x


def get_KFold_train_test(class_ids, num_folds = 5):
    
    num_samples = len(class_ids)
    random_indices = np.random.permutation(np.arange(num_samples))    

    fold_sizes = (num_samples // num_folds) * np.ones(num_folds, dtype=np.int)
    
    K_fold_indices = []
    current = 0
    for fold_size in fold_sizes:
        start, stop = current, current + fold_size
        # print fold_size, start, stop
        # print random_indices[start:stop]
        # print np.concatenate((random_indices[:start], random_indices[stop:]))
        # print len(random_indices[start:stop])
        
        K_fold_indices.append((random_indices[start:stop], np.concatenate((random_indices[:start], random_indices[stop:]))))
        
        current = stop
        
    return K_fold_indices
    
    

def get_symm_KFold_train_test(class_ids, num_folds = 5):
    
    from collections import defaultdict    
    
    class_dict = defaultdict(list)
    for i, class_id in enumerate(class_ids):
        class_dict[class_id] += [i]
    
    # print class_dict[0]
    # print class_dict[1]
    
    
    min_class_len = min([len(class_dict[class_id]) for class_id in class_dict.keys()]) 
    
    balanced_class_dict = defaultdict(list)
    for key, values in class_dict.items():
        balanced_class_dict[key] = np.random.permutation(values)[:min_class_len]
    
    
    K_fold_indices = []
    fold_sizes = (min_class_len // num_folds) * np.ones(num_folds, dtype=np.int)
    
    current = 0
    for fold_size in fold_sizes:
        start, stop = current, current + fold_size

        test = []
        train = []
        for key, values in balanced_class_dict.items():
            test += values[start:stop].tolist()
            train += np.concatenate((values[:start], values[stop:])).tolist()

        K_fold_indices.append((test, train))

        current = stop
  
    return K_fold_indices
    
    


