import os 
import numpy as np 

from utils.utils_file import read_config, load_file_paths_index


def get_tm_svm_data(mdl_cfg_file, positive_dir):   
    
    mdl_cfg = read_config(mdl_cfg_file)

    lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']    
    lda_file_path_index = load_file_paths_index(path_index_file)    
    lda_theta = np.loadtxt(lda_theta_file, dtype=np.longdouble)
    num_docs, num_topics = lda_theta.shape
    
    print 'LDA Theta: Number of documents ', num_docs, ' number of topics ', num_topics  
    
    class_ids = []
    for (_, _, file_name) in lda_file_path_index:
        if os.path.exists(os.path.join(positive_dir, file_name)):
            class_ids.append(1)
        else:
            class_ids.append(0)
        
    return (class_ids, lda_theta.tolist())


def save_tm_svm_data(class_ids, lda_theta, file_name):
    
    with open(file_name, 'w') as fw: 
        for i, class_id in enumerate(class_ids):
            features = ' '.join([str(class_id), ' '.join(['%d:%.24f' % (k, theta_dk) for k, theta_dk in enumerate(lda_theta[i])])])
            fw.write(features)
            
            
                     
         
    
    
mdl_cfg_file = "project-204-raw.cfg" # "gui/project3.cfg" # configuration file, created using the SMARTeR GUI 
test_directory = "F:\\Research\\datasets\\trec2010\\204"# the directory where we keep the training set (TRUE negatives and TRUE positives) 
positive_dir = os.path.normpath(os.path.join(test_directory, "1")) # TRUE positive documents 

class_ids, lda_theta = get_tm_svm_data(mdl_cfg_file, positive_dir)

save_tm_svm_data(class_ids, lda_theta, mdl_cfg_file + '.libsvm.data')


