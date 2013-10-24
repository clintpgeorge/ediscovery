import pyradbas.pyradbas as pyrb
from eval_tm_datasets import *  


def plot_tm_rbf_decision_values(class_ids, dec_values, plot_title = '', plot_file = ''):
    
    import pylab as pl
    from collections import defaultdict
    
    print 
    true_class = defaultdict(list)
    for i, class_id in enumerate(class_ids):
        print '#%d true class: %d decision value: %.5f' % (i, class_id, dec_values[i])
        true_class[class_id] += [dec_values[i]]
    print 
    
    pl.clf()
    pl.plot(true_class[IRRELEVANT_CLASS_ID], 'bo', label='Irrelevant')
    x2 = range(len(true_class[IRRELEVANT_CLASS_ID]), len(class_ids))
    pl.plot(x2, true_class[RELEVANT_CLASS_ID], 'r+', label='Relevant')
    pl.axhline(0, color='black')
    pl.xlabel('Documents')
    pl.ylabel('Decision values')
    pl.title(plot_title)
    pl.legend(loc='lower right', prop={'size':9})
    pl.grid(True)

    if (plot_file == ''):
        pl.show()
    else: 
        pl.savefig(plot_file, dpi=300, bbox_inches='tight', pad_inches=0.1)
    pl.close()
    pl.clf()


def rbf_cv(K_fold_indices, class_ids, lda_theta, rbf_gamma = 0.05):     
    
    rbf_out = [] # contains RBF output 
    true_class_ids = []
    features = []
    for (test_indices, train_indices) in K_fold_indices:
        
        # print k, test_indices, train_indices
        test_y, test_x = class_ids[test_indices], lda_theta[test_indices]
        train_y, train_x = class_ids[train_indices], lda_theta[train_indices]
    
        # defines an exact RBFN on train 
        enet = pyrb.train_exact(train_x, train_y, rbf_gamma)
        
        # simulate on test 
        dec_values = enet.sim(test_x)
        for i, dec_value in enumerate(dec_values):
            rbf_out.append(dec_value)
            true_class_ids.append(test_y[i])
            features.append(test_x[i])
        
    return (rbf_out, true_class_ids, features) 


def calc_rbf_acc(true_class_ids, decision_values, decision_cut_off = 0.4): 
    '''
    compute the classification accuracy based on a cut-off    
    '''
    
    num_samples = len(true_class_ids)
    total_num_acc = 0.0
    
    for i, true_class_id in enumerate(true_class_ids):
        if decision_values[i] > decision_cut_off:
            predicted_class_id = IRRELEVANT_CLASS_ID
        else: 
            predicted_class_id = RELEVANT_CLASS_ID
            
        if predicted_class_id == true_class_id: 
            total_num_acc += 1.0

    return total_num_acc / num_samples


if __name__ == '__main__':
    
    query_id = 201
    mdl_cfg_file = "project-%d.cfg" % query_id # configuration file 
    test_directory = "F:\\Research\\datasets\\trec2010\\%d" %  query_id # the directory where we keep the training set (TRUE negatives and TRUE positives) 
    positive_dir = os.path.normpath(os.path.join(test_directory, "1")) # TRUE positive documents 
    dec_values_file = mdl_cfg_file.replace('.cfg', '-rbf-dec.png') 
    roc_img_title = mdl_cfg_file.replace('.cfg', '-rbf')
    roc_values_file = mdl_cfg_file.replace('.cfg', '-rbf-roc.png')  
    dec_values_plot_title = 'Query #%d: RBF decision values' % query_id
    rbf_gamma = 0.05 
    
    # Loads the RBF dataset from the given topic model 
    class_ids, lda_theta, file_paths = get_tm_classification_dataset(mdl_cfg_file, positive_dir)
    
    
    
#    test_y, test_x, train_y, train_x = get_random_train_test(class_ids, lda_theta, test_perc = 0.4)
#
#    # defines an exact RBFN on train 
#    enet = pyrb.train_exact(train_x, train_y, rbf_gamma)
#    
#    # simulate on test 
#    dec_values = enet.sim(test_x)
#    
#    # plot decision values 
#    plot_tm_rbf_decision_values(test_y, dec_values, dec_values_plot_title)
#    
#    # plot ROC curve 
#    from PyROC.pyroc import ROCData
#    roc_in = [(test_y[i], dec_value) for i, dec_value in enumerate(dec_values)]
#    roc_data = ROCData(roc_in)
#    roc_data.plot(roc_img_title)
    
    
    
    
    # K-fold cross validation 
    num_folds = 5
    decision_cut_off = 0.40000000001
    
    K_fold_indices = get_symm_KFold_train_test(class_ids, num_folds)
    
    
#    K_fold_indices = get_KFold_train_test(class_ids, num_folds)
#    
#    
    cv_results = {}
    
    for rbf_gamma in np.arange(0.1, 20, 0.5):
        print 'gamma:', rbf_gamma, 
        
        cv_results[rbf_gamma] = rbf_cv(K_fold_indices, class_ids, lda_theta, rbf_gamma)
        
        (decision_values, true_class_ids, _) = cv_results[rbf_gamma]
        print 'CV accuracy:', calc_rbf_acc(true_class_ids, decision_values, decision_cut_off)
#
#        
#    k_keys_sorted = sorted(cv_results.keys(), key=lambda k:cv_results[k][0], reverse=True)[:10]
#    
#    for key in k_keys_sorted:
#        print key, cv_results[key][0]
        
        
    
    
        
                
                
                
        
        
        
        
        



