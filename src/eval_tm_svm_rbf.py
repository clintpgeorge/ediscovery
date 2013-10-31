'''
Created on Oct 22, 2013

@author: Clint
'''
import os 
import pyradbas.pyradbas as pyrb   

from eval_tm_datasets import get_tm_classification_dataset, get_random_train_test, get_KFold_train_test, get_symm_KFold_train_test
from eval_tm_svm import plot_tm_svm_decision_values, svm_cv
from eval_tm_lucene import plot_results_rocs
from rbf import plot_tm_rbf_decision_values, rbf_cv 
from libsvm.python.svmutil import svm_problem, svm_parameter, svm_train, svm_predict


if __name__ == '__main__':


    query_id = 201
    mdl_cfg_file = "project-%d.cfg" % query_id # configuration file 
    test_directory = "F:\\Research\\datasets\\trec2010\\%d" %  query_id # the directory where we keep the training set (TRUE negatives and TRUE positives) 
    positive_dir = os.path.normpath(os.path.join(test_directory, "1")) # TRUE positive documents 

    num_folds = 5
    
    rbf_dec_values_plot = mdl_cfg_file.replace('.cfg', '-rbf-dec.png') 
    rbf_dec_values_plot_title = 'Query #%d: RBF decision values' % query_id
    rbf_gamma = 0.05
        
    svm_dec_values_plot = mdl_cfg_file.replace('.cfg', '-svm-dec.png') 
    svm_dec_values_plot_title = 'Query #%d: SVM decision values' % query_id
    
    roc_labels = ['SVM classification', 'RBF Classification']
    rocs_file_name = mdl_cfg_file.replace('.cfg', '-svm-rbf-ROC.png') 
    rocs_img_title = '%s: SVM & RBF Classification ROC curves' % query_id
    
    # 201
    svm_C = 32
    svm_gamma = 0.5
    
    
    # 202 
    # svm_C = 32.0
    # svm_gamma = 0.5


    

    
    # Loads the classification data from the given topic model 
    
    class_ids, lda_theta, file_paths = get_tm_classification_dataset(mdl_cfg_file, positive_dir)
    
    import numpy as np 
    
    # SVM and RBF tesing on cross validation 
    
    K_fold_indices = get_symm_KFold_train_test(class_ids, num_folds)
    
    svm_decision_values, svm_true_class_ids, _, _, _ = svm_cv(K_fold_indices, class_ids, lda_theta, svm_C, svm_gamma)
    svm_roc_in = [(class_id, svm_decision_values[i]) for i, class_id in enumerate(svm_true_class_ids)]
    
    rbf_decision_values, rbf_true_class_ids, _ = rbf_cv(K_fold_indices, class_ids, lda_theta, rbf_gamma)
    rbf_roc_in = [(class_id, rbf_decision_values[i]) for i, class_id in enumerate(rbf_true_class_ids)]
    
    plot_tm_svm_decision_values(svm_true_class_ids, svm_decision_values, svm_dec_values_plot_title, svm_dec_values_plot)
    plot_tm_rbf_decision_values(rbf_true_class_ids, np.log(rbf_decision_values), rbf_dec_values_plot_title, rbf_dec_values_plot)
    
    
#    #-------------------------------------------------- Generate random test set
#    
#    test_y, test_x, train_y, train_x = get_random_train_test(class_ids, lda_theta, test_perc = 0.4)
#    
#    #------------------------------------ Generate ROC data from SVM  
#    
#    # SVM train 
#    
#    train_prob  = svm_problem(train_y.tolist(), train_x.tolist())
#    train_param = svm_parameter('-t 2 -c 0 -b 1 -c %f -g %f' % (svm_C, svm_gamma))
#    train_mdl = svm_train(train_prob, train_param)
#    
#    
#    
#    # SVM prediction and plots the decision values 
#    # of corresponding data points 
#    
#    p_label, p_acc, p_val = svm_predict(test_y.tolist(), test_x.tolist(), train_mdl, '-b 0')
#    p_val = [p_v[0] for p_v in p_val]
#    plot_tm_svm_decision_values(test_y.tolist(), p_val, svm_dec_values_plot_title, svm_dec_values_plot)
#    
#    
#    # Convert to the ROC format and generate ROCs 
#     
#    svm_roc_in = [(class_id, p_val[i]) for i, class_id in enumerate(test_y.tolist())]
#
#    
#    
#    #----------------------------------- Generate ROC data from the RBF network 
#    
#     
#    
#    # defines an exact RBFN
#    enet = pyrb.train_exact(train_x, train_y, rbf_gamma)
#    
#    # simulate
#    dec_values = enet.sim(test_x)
#    
#    # plot decision values 
#    plot_tm_rbf_decision_values(test_y, dec_values, rbf_dec_values_plot_title, rbf_dec_values_plot)
#    
#    # Convert to the ROC format and generate ROCs 
#    rbf_roc_in = [(class_id, dec_values[i]) for i, class_id in enumerate(test_y)]

    
    #------------------------------------------------------- Generate ROC curves
    
    results_list = [svm_roc_in, rbf_roc_in]
    plot_results_rocs(results_list, roc_labels, rocs_file_name, rocs_img_title)
    
    
    
    
    
    
    
    

