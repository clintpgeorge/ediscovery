import os 
import numpy as np 

from utils.utils_file import read_config, load_file_paths_index

RELEVANT_CLASS_ID = 1
IRRELEVANT_CLASS_ID = -1 

def get_tm_svm_data(mdl_cfg_file, positive_dir):   
    
    mdl_cfg = read_config(mdl_cfg_file)

    lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']    
    lda_file_path_index = load_file_paths_index(path_index_file)    
    lda_theta = np.loadtxt(lda_theta_file, dtype=np.longdouble)
    num_docs, num_topics = lda_theta.shape
    
    print 'LDA Theta: Number of documents ', num_docs, ' number of topics ', num_topics  
    
    class_ids = []
    file_paths = [] 
    for (_, root, file_name) in lda_file_path_index:
        if os.path.exists(os.path.join(positive_dir, file_name)):
            class_ids.append(RELEVANT_CLASS_ID)
        else:
            class_ids.append(IRRELEVANT_CLASS_ID)
        file_paths.append(os.path.normpath(os.path.join(root, file_name)))
        
    return (class_ids, lda_theta.tolist(), file_paths)


def save_tm_svm_data(class_ids, lda_theta, file_name):
    
    with open(file_name, 'w') as fw: 
        for i, class_id in enumerate(class_ids):
            features = ' '.join([str(class_id), ' '.join(['%d:%.24f' % (k, theta_dk) for k, theta_dk in enumerate(lda_theta[i])])])
            print >>fw, features
            
def plot_tm_svm_decision_values(class_ids, p_label, p_val, svm_dec_values_file=''):
    
    import pylab as pl
    
    print 
    true_class = defaultdict(list)
    for i, class_id in enumerate(class_ids):
        # print '#%d true class: %d predicted class: %d decision value: %.5f' % (i, class_id, p_label[i], p_val[i][0])
        true_class[class_id] += p_val[i]
    print 
    
    pl.plot(true_class[IRRELEVANT_CLASS_ID], 'bo', label='Irrelevant')
    x2 = range(len(true_class[IRRELEVANT_CLASS_ID]), len(class_ids))
    pl.plot(x2, true_class[RELEVANT_CLASS_ID], 'r+', label='Relevant')
    pl.axhline(0, color='black')
    pl.xlabel('Documents')
    pl.ylabel('Decision values (c-SVM)')
    pl.title('SVM decision values Query #%d' % query_id)
    pl.legend(loc='lower right', prop={'size':9})
    pl.grid(True)
    # pl.xticks(range(0, len(class_ids)))
    
    if (svm_dec_values_file == ''):
        pl.show()
    else: 
        pl.savefig(svm_dec_values_file, dpi=300, bbox_inches='tight', pad_inches=0.1)




                     
from libsvm.python.svmutil import *
from libsvm.tools.grid import *
from collections import defaultdict

    
query_id = 202 
mdl_cfg_file = "project-%d.cfg" % query_id # configuration file 
test_directory = "F:\\Research\\datasets\\trec2010\\%d" %  query_id # the directory where we keep the training set (TRUE negatives and TRUE positives) 
positive_dir = os.path.normpath(os.path.join(test_directory, "1")) # TRUE positive documents 
svm_data_file = mdl_cfg_file.replace('.cfg', '-libsvm.data') 
svm_dec_values_file = mdl_cfg_file.replace('.cfg', '-libsvm-dec.png') 


# Loads the SVM data from the given topic model 

class_ids, lda_theta, file_paths = get_tm_svm_data(mdl_cfg_file, positive_dir)


## Grid search for selecting C and g 
#
#save_tm_svm_data(class_ids, lda_theta, svm_data_file)
#rate, param = find_parameters(svm_data_file, '-log2c -10,20,1 -v 5')
#
#C = param['c']
#g = param['g']

## 201
#C = 32
#g = 0.5

# 202 
C = 32.0
g = 0.5

print 'CV results: C = %f g = %f' % (C, g)

# SVM train 

train_prob  = svm_problem(class_ids, lda_theta)
train_param = svm_parameter('-t 2 -c 0 -b 1 -c %f -g %f' % (C, g))
train_mdl = svm_train(train_prob, train_param)



# SVM prediction and plots the decision values 
# of corresponding data points 

p_label, p_acc, p_val = svm_predict(class_ids, lda_theta, train_mdl, '-b 0')
plot_tm_svm_decision_values(class_ids, p_label, p_val, svm_dec_values_file)









