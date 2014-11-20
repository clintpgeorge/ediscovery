'''
Created on Oct 22, 2013

@author: Clint
'''

import os 
import numpy as np 
from utils.utils_file import read_config, load_file_paths_index
from collections import defaultdict 

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
        K_fold_indices.append((random_indices[start:stop], 
                               np.concatenate((random_indices[:start], 
                                               random_indices[stop:]))))
        
        current = stop
        
    return K_fold_indices
    
    

def get_symm_KFold_train_test(class_ids, num_folds = 5):
    
    class_indices = defaultdict(list)
    for i, class_id in enumerate(class_ids):
        class_indices[class_id] += [i]
    
    min_class_len = min([len(class_indices[class_id]) for class_id in class_indices.keys()]) 
    
    balanced_class_indices = defaultdict(list)
    for key, values in class_indices.items():
        balanced_class_indices[key] = np.random.permutation(values)[:min_class_len]

    K_fold_indices = []
    fold_sizes = (min_class_len // num_folds) * np.ones(num_folds, dtype=np.int)
    
    current = 0
    for fold_size in fold_sizes:
        start, stop = current, current + fold_size

        test_fold = []
        train_fold = []
        for key, values in balanced_class_indices.items():
            # print key, len(values[start:stop]), len(np.concatenate((values[:start], values[stop:])))
            test_fold += values[start:stop]
            train_fold += np.concatenate((values[:start], values[stop:])).tolist()
        K_fold_indices.append((test_fold, train_fold))
        #print test_fold, train_fold

        current = stop
  
    return K_fold_indices
    
    
def get_stratified_KFold_train_test(class_ids, num_folds = 5):
    
    class_indices = defaultdict(list)
    for i, class_id in enumerate(class_ids):
        class_indices[class_id] += [i]
    
    fold_sizes = {}
    class_doc_idx = {}  
    for j, (_, values) in enumerate(class_indices.items()):
        fold_sizes[j] = (len(values) // num_folds) * np.ones(num_folds, dtype=np.int)
        class_doc_idx[j] = values  

    folds_counts = []
    for i in range(0, num_folds):
        folds_counts.append([fold_sizes[j][i] for j in fold_sizes.keys()])

    K_fold_indices = []      
    current = np.zeros(len(fold_sizes)).astype(int)
    
    for fold_counts in folds_counts:
        start, stop = current, current + fold_counts

        test_fold = []
        train_fold = []
        for j, values in class_doc_idx.items():
            # print key, len(values[start:stop]), len(np.concatenate((values[:start], values[stop:])))
            test_fold += values[start[j]:stop[j]]
            train_fold += np.concatenate((values[:start[j]], values[stop[j]:])).tolist()
        K_fold_indices.append((test_fold, train_fold))
        
        # print len(test_fold), len(train_fold)

        current = stop
  
    return K_fold_indices


