from libsvm.python.svmutil import svm_problem, svm_parameter, svm_train, svm_predict
from eval_tm_datasets import get_tm_classification_dataset, IRRELEVANT_CLASS_ID, RELEVANT_CLASS_ID

def save_tm_svm_data(class_ids, lda_theta, file_name):
    
    with open(file_name, 'w') as fw: 
        for i, class_id in enumerate(class_ids):
            features = ' '.join([str(class_id), ' '.join(['%d:%.24f' % (k, theta_dk) for k, theta_dk in enumerate(lda_theta[i])])])
            print >>fw, features
            
def plot_tm_svm_decision_values(class_ids, p_val, plot_title = '', plot_file = ''):
    
    import pylab as pl
    from collections import defaultdict
    
    print 
    true_class = defaultdict(list)
    for i, class_id in enumerate(class_ids):
        print '#%d true class: %d decision value: %.5f' % (i, class_id, p_val[i])
        true_class[class_id] += [p_val[i]]
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



def svm_cv(K_fold_indices, class_ids, lda_theta, svm_C = 1.0, svm_gamma = 0.05):     
    
    decision_values = [] # contains RBF output 
    true_class_ids = []
    features = []
    predicted_class_ids = []
    cv_acc = 0.0 
    
    for (test_indices, train_indices) in K_fold_indices:
        
        # print k, test_indices, train_indices
        test_y, test_x = class_ids[test_indices], lda_theta[test_indices]
        train_y, train_x = class_ids[train_indices], lda_theta[train_indices]
    
        # SVM train 
        
        train_prob  = svm_problem(train_y.tolist(), train_x.tolist())
        train_param = svm_parameter('-t 2 -c 0 -b 1 -c %f -g %f' % (svm_C, svm_gamma))
        train_mdl = svm_train(train_prob, train_param)

        
        # SVM prediction 
        
        p_label, p_acc, p_val = svm_predict(test_y.tolist(), test_x.tolist(), train_mdl, '-b 0')

        for i, dec_value in enumerate(p_val):
            decision_values.append(dec_value[0])
            true_class_ids.append(test_y[i])
            features.append(test_x[i])
            predicted_class_ids.append(p_label[i])
        
        cv_acc += p_acc[0] / len(K_fold_indices)
        
    return (decision_values, true_class_ids, features, predicted_class_ids, cv_acc) 



if __name__ == '__main__':
    
    from libsvm.python.svmutil import *
    from libsvm.tools.grid import *
    
    
        
    query_id = 201
    mdl_cfg_file = "project-%d.cfg" % query_id # configuration file 
    test_directory = "F:\\Research\\datasets\\trec2010\\%d" %  query_id # the directory where we keep the training set (TRUE negatives and TRUE positives) 
    positive_dir = os.path.normpath(os.path.join(test_directory, "1")) # TRUE positive documents 
    svm_data_file = mdl_cfg_file.replace('.cfg', '-libsvm.data') 
    svm_dec_values_file = mdl_cfg_file.replace('.cfg', '-svm-dec.png') 
    svm_dec_values_title = 'Query #%d: SVM decision values' % query_id
    
    # Loads the SVM data from the given topic model 
    
    class_ids, lda_theta, file_paths = get_tm_classification_dataset(mdl_cfg_file, positive_dir)
    
    ## Grid search for selecting C and g 
    #
    #save_tm_svm_data(class_ids, lda_theta, svm_data_file)
    #rate, param = find_parameters(svm_data_file, '-log2c -10,20,1 -v 5')
    #
    #C = param['c']
    #g = param['g']
    
    # 201
    C = 32
    g = 0.5
    
    # 202 
    # C = 32.0
    # g = 0.5
    
    print 'CV results: C = %f g = %f' % (C, g)
    
    # SVM train 
    
    train_prob  = svm_problem(class_ids.tolist(), lda_theta.tolist())
    train_param = svm_parameter('-t 2 -c 0 -b 1 -c %f -g %f' % (C, g))
    train_mdl = svm_train(train_prob, train_param)
    
    
    
    # SVM prediction and plots the decision values 
    # of corresponding data points 
    
    p_label, p_acc, p_val = svm_predict(class_ids.tolist(), lda_theta.tolist(), train_mdl, '-b 0')
    p_val = [p_v[0] for p_v in p_val]
    plot_tm_svm_decision_values(class_ids.tolist(), p_val, svm_dec_values_title, svm_dec_values_file)
    
    
    # Convert to the ROC format and generate ROCs 
     
    svm_roc_in = [(class_id, p_val[i]) for i, class_id in enumerate(class_ids.tolist())]
    
    
    #from PyROC.pyroc import ROCData
    #roc_data = ROCData(svm_roc_in)
    #roc_data.plot(rocs_img_title, file_name=rocs_file_name)

    

