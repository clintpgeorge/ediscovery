import os 
import numpy as np 

# from libsvm.python.svmutil import *
# from libsvm.tools.grid import *
#from libsvm.python.svmutil import svm_problem, svm_parameter, svm_train, svm_predict
from eval_tm_datasets import get_tm_classification_dataset #, IRRELEVANT_CLASS_ID, RELEVANT_CLASS_ID
# from eval_tm_datasets import get_symm_KFold_train_test, get_KFold_train_test, get_stratified_KFold_train_test

import pylab as pl

from sklearn import svm
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold
# from scipy import interp
# from sklearn.grid_search import GridSearchCV
# from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split


 
def save_tm_svm_data(class_ids, lda_theta, file_name):
     
    with open(file_name, 'w') as fw: 
        for i, class_id in enumerate(class_ids):
            features = ' '.join([str(class_id), 
                                 ' '.join(['%d:%.24f' % (k, theta_dk) 
                                           for k, theta_dk in enumerate(lda_theta[i])])])
            print >>fw, features
             
# def plot_tm_svm_decision_values(class_ids, p_val, plot_title = '', plot_file = ''):
#     
#     import pylab as pl
#     from collections import defaultdict
#     
#     print 
#     true_class = defaultdict(list)
#     for i, class_id in enumerate(class_ids):
#         print '#%d true class: %d decision value: %.5f' % (i, class_id, p_val[i])
#         true_class[class_id] += [p_val[i]]
#     print 
#     
#     pl.clf()
#     pl.plot(true_class[IRRELEVANT_CLASS_ID], 'bo', label='Irrelevant')
#     x2 = range(len(true_class[IRRELEVANT_CLASS_ID]), len(class_ids))
#     pl.plot(x2, true_class[RELEVANT_CLASS_ID], 'r+', label='Relevant')
#     pl.axhline(0, color='black')
#     pl.xlabel('Documents')
#     pl.ylabel('Decision values')
#     pl.title(plot_title)
#     pl.legend(loc='lower right', prop={'size':9})
#     pl.grid(True)
#     
#     if (plot_file == ''):
#         pl.show()
#     else: 
#         pl.savefig(plot_file, dpi=300, bbox_inches='tight', pad_inches=0.1)
#     pl.close()
#     pl.clf()
# 
# 
# 
# def svm_cv(K_fold_indices, 
#            class_ids, 
#            lda_theta, 
#            svm_C = 1.0, 
#            svm_gamma = 0.05):     
#     
#     decision_values = [] # contains RBF output 
#     true_labels = []
#     features = []
#     pred_labels = []
#     
#     
#     for (test_indices, train_indices) in K_fold_indices:
# 
#         test_y, test_x = class_ids[test_indices], lda_theta[test_indices]
#         train_y, train_x = class_ids[train_indices], lda_theta[train_indices]
#         
#         train_prob  = svm_problem(train_y.tolist(), train_x.tolist())
#         train_param = svm_parameter('-s 0 -t 2 -b 1 -c %f -g %f -q' % (svm_C, svm_gamma))
#         train_mdl = svm_train(train_prob, train_param)
#         p_label, p_acc, p_val = svm_predict(test_y.tolist(), test_x.tolist(), 
#                                             train_mdl, '-b 0 -q')
#         
#         for i, dec_value in enumerate(p_val):
#             decision_values.append(dec_value[0])
#             true_labels.append(test_y[i])
#             features.append(test_x[i])
#             pred_labels.append(p_label[i])
#         
#     cv_acc = 0.0 
#     for i, true_label in enumerate(true_labels):
#         if true_label == pred_labels[i]:
#             cv_acc += 1.     
#     cv_acc /= len(true_labels)
#         
#     return (decision_values, true_labels, features, pred_labels, cv_acc) 



def plot_C_gamma_grid_search(grid, C_range, gamma_range, score):
    '''
    Plots the scores computed on a grid. 
    
    Arguments: 
        grid - the grid search object created using GridSearchCV()
        C_range - the C parameter range 
        gamma_range - the gamma parameter range 
        score - the scoring function  
        
    
    '''

    # grid_scores_ contains parameter settings and scores
    # We extract just the scores
    scores = [x[1] for x in grid.grid_scores_]
    scores = np.array(scores).reshape(len(C_range), len(gamma_range))
    
    # draw heatmap of accuracy as a function of gamma and C
    pl.figure(figsize=(8, 6))
    pl.subplots_adjust(left=0.05, right=0.95, bottom=0.15, top=0.95)
    pl.imshow(scores, interpolation='nearest', cmap=pl.cm.spectral)
    pl.title("Grid search on C and gamma for best %s" % score)
    pl.xlabel('gamma')
    pl.ylabel('C')
    pl.colorbar()
    pl.xticks(np.arange(len(gamma_range)), gamma_range, rotation=45)
    pl.yticks(np.arange(len(C_range)), C_range)
    
    pl.show()


def plot_cv_rocs(classifier, X, y, cv_iterator, draw=True):
    '''
    Run "classifier" on different cross-validation folds 
    and plot their ROC curves. This method also computes 
    the composite ROC using all CV folds. 
    
    Arguments: 
        classifier - the classifier object created using 
                     sklean toolkit
                     e.g., svm.SVC(kernel='linear', probability=True, random_state=0)
        X          - the training features  
        y          - the training set's labels 
        cv_iterator- the CV iterator object created using 
                     sklean toolkit   
        draw       - True: plot the ROCs, False: return composite AUC   
    
    '''
 
#     mean_tpr = 0.0
#     mean_fpr = np.linspace(0, 1, 100)
    
    cls_ids = []
    pred_probs = []
      
    for i, (train, test) in enumerate(cv_iterator):
         
        probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
        
         
        # Compute ROC curve and area the curve
        fpr, tpr, _ = roc_curve(y[test], probas_[:, 1])
        cls_ids += y[test].tolist()
        pred_probs += probas_[:, 1].tolist()
#         mean_tpr += interp(mean_fpr, fpr, tpr)
#         mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        if draw: 
            pl.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
      
    
     
#     mean_tpr /= len(cv_iterator)
#     mean_tpr[-1] = 1.0
#     mean_auc = auc(mean_fpr, mean_tpr)
    
    # Computes the composite ROC from all CV folds and not mean ROC 
    cfpr, ctpr, _ = roc_curve(cls_ids, pred_probs)
    composite_auc = auc(cfpr, ctpr)

    
    if draw:         
        pl.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
        pl.plot(cfpr, ctpr, 'k--', label='Mean ROC (area = %0.2f)' % composite_auc, lw=2)     
        pl.xlim([-0.05, 1.05])
        pl.ylim([-0.05, 1.05])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver Operating Characteristic')
        pl.legend(loc="lower right")
        pl.show()
    
    return composite_auc

def find_optimal_RBF_C_gamma(X_train, y_train, num_folds=5, 
                             log2gamma=np.arange(-10, 2, 1), 
                             log2c = np.arange(-1, 10, 1), 
                             random_state=1983):
    '''
    Grid search on the C-gamma grid (optimizing AUC)
    '''
    
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    # Generate stratified cross validation folds 
    cv = StratifiedKFold(y_train, n_folds=num_folds)     
    
    C_range = 2. ** log2c # np.exp(log2c * np.log(2))
    gamma_range = 2. ** log2gamma # np.exp(log2gamma * np.log(2))    
    
    grid_search_scores = [] 
    for svm_C in C_range: 
        for svm_gamma in gamma_range:           
            classifier = svm.SVC(kernel='rbf', probability=True, 
                                 random_state=random_state, C=svm_C, 
                                 gamma=svm_gamma)
            composite_auc = plot_cv_rocs(classifier, X_train, y_train, cv, 
                                         False)
            ret = dict(C=svm_C, gamma=svm_gamma, cv_auc=composite_auc)
            grid_search_scores.append(ret)
       
    newlist = sorted(grid_search_scores, key=lambda k: -k['cv_auc']) 
    
    return newlist[0]


    
def eval_SVC_classifier(X_train, X_test, y_train, y_test, cf):
    
    test_prob_ = cf.predict_proba(X_test)
    train_prob_ = cf.predict_proba(X_train)
    
     
    # Compute ROC curve and area the curve
    fpr, tpr, _ = roc_curve(y_test, test_prob_[:, 1])
    roc_auc = auc(fpr, tpr)
    pl.plot(fpr, tpr, lw=1, label='Test set ROC  (AUC = %0.2f)' % roc_auc)
    
    fpr, tpr, _ = roc_curve(y_train, train_prob_[:, 1])
    roc_auc = auc(fpr, tpr)
    pl.plot(fpr, tpr, lw=1, label='Train set ROC  (AUC = %0.2f)' % roc_auc)
    
    
    pl.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Random Choice')
    pl.xlim([-0.05, 1.05])
    pl.ylim([-0.05, 1.05])
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('Receiver Operating Characteristic')
    pl.legend(loc="lower right")
    pl.show()
    
  

if __name__ == '__main__':
    
    NUM_CV_FOLDS = 5
    RELEVANT_DIR_NAME = "1"
    RANDOM_STATE = 1983 
    data_dir = "E:\\E-Discovery\\trec2010dataset"
    output_dir = "E:\\E-Discovery\\trec2010index"
    
    # Testing on the query 201 data 
     
    query_id = 201
    num_topics = 30 # it's fixed 
    
    # the directory which contains the training set 
    # (TRUE negatives and TRUE positives)
    truth_dir = "%s\\%d" % (data_dir, query_id)  
    
    # Using unormalized keywords  
    project_name = "Q%d-LW-%dT" % (query_id, num_topics)
    config_file = "%s\\%s.cfg" % (output_dir, project_name) 
    positive_dir = os.path.join(truth_dir, RELEVANT_DIR_NAME) # TRUE positive documents 

    svm_data_file = config_file.replace('.cfg', '-libsvm.data') 
    svm_dec_values_file = config_file.replace('.cfg', '-svm-dec.png') 
    svm_dec_values_title = 'Query #%d: SVM decision values' % query_id
    
    # Loads the SVM data from the given topic model 
    
    class_ids, lda_theta, file_paths = get_tm_classification_dataset(config_file, positive_dir)
    

    # Crossvalidation and Grid search to find optimal C and gamma 
    X_train, X_test, y_train, y_test = train_test_split(lda_theta, 
                                                        class_ids, test_size=0.7, 
                                                        random_state=RANDOM_STATE)
    
    ret = find_optimal_RBF_C_gamma(X_train, y_train, random_state=RANDOM_STATE)

    print "Optimal value:", ret
    
    # Train the optimal classifier 
    classifier = svm.SVC(kernel='rbf', probability=True, 
                         random_state=RANDOM_STATE, 
                         C=ret['C'], gamma=ret['gamma'])
    cf = classifier.fit(X_train, y_train)
    
    eval_SVC_classifier(X_train, X_test, y_train, y_test, cf)
    
    
#     
#     # Set the parameters by cross-validation
#     tuned_parameters = [{'kernel': ['rbf'], 'gamma': gamma_range, 'C': C_range}, {'kernel': ['linear'], 'C': C_range}]  
#                        
#     
#     scores = ['accuracy'] # 'roc_auc'
#     
#     
#     for score in scores:
#         print "# Tuning hyper-parameters for %s" % score
#         print
#     
#         grid = GridSearchCV(svm.SVC(C=1), tuned_parameters, cv=cv, scoring=score)
#         grid.fit(X_train, y_train)
#     
#         print "Best parameters set found on development set:"
#         print 
#         print grid.best_params_, grid.best_score_
#         print
#         print "Grid scores on development set:"
#         print
#         for params, mean_score, scores in grid.grid_scores_:
#             print "%s: %0.3f (+/-%0.03f) for %r" % (score, mean_score, scores.std() / 2, params)
#         print
#         
#         print "Detailed classification report:"
#         print
#         print "The model is trained on the full development set."
#         print "The scores are computed on the full evaluation set."
#         print 
#         y_true, y_pred = y_test, grid.predict(X_test)
#         print classification_report(y_true, y_pred) 
#         print 
#         
#         # plot_C_gamma_grid_search(grid, C_range, gamma_range, score)
#     


#     '''
#     --------------------------------------------------- 
#     Grid search for selecting C and g 
#     This is using the grid search function in LIBSVM 
#     ---------------------------------------------------     
#     '''
#     save_tm_svm_data(class_ids, lda_theta, svm_data_file)
#     rate, param = find_parameters(svm_data_file, '-s 0 -t 2 -log2c -1,5,1 -log2g 2,-2,-2 -v 5')
#     
#     C = param['c']
#     g = param['g']
#    
#     print 'CV results: C = %f g = %f ACC = %f' % (C, g, rate)

    
    # 201
    # C = 32
    # g = 0.5
    
    # 202 
    # C = 32.0
    # g = 0.5
    
 
     
#     # SVM on cross validation 
#      
#     # K_fold_indices = get_KFold_train_test(class_ids, NUM_CV_FOLDS) # 
#     # K_fold_indices = get_symm_KFold_train_test(y_train, NUM_CV_FOLDS)
#     K_fold_indices = get_stratified_KFold_train_test(class_ids, NUM_CV_FOLDS) 
#                  
#     opt_values = (0., 0., 0.)
#      
#        
#     for svm_C in C_range: 
#         for svm_gamma in gamma_range:
#           
#             svm_decision_values, svm_true_class_ids, _, _, cv_acc = svm_cv(cv, y_train, X_train, svm_C, svm_gamma)
#               
#             print "C =", svm_C, "g =", svm_gamma, "ACC =", cv_acc
#               
#             if cv_acc > opt_values[2]:
#                 opt_values = (svm_C, svm_gamma, cv_acc) 
#       
#     print "Optimal values:", opt_values
    
    
    
              
             
#      
#      
#     svm_roc_in = [(class_id, svm_decision_values[i]) for i, class_id in enumerate(svm_true_class_ids)]
#     
#     
#     # SVM train 
#     
#     train_prob  = svm_problem(class_ids.tolist(), lda_theta.tolist())
#     train_param = svm_parameter('-t 2 -c 0 -b 1 -c %f -g %f' % (C, g))
#     train_mdl = svm_train(train_prob, train_param)
#     
#     
#     
#     # SVM prediction and plots the decision values 
#     # of corresponding data points 
#     
#     p_label, p_acc, p_val = svm_predict(class_ids.tolist(), lda_theta.tolist(), train_mdl, '-b 0')
#     p_val = [p_v[0] for p_v in p_val]
#     plot_tm_svm_decision_values(class_ids.tolist(), p_val, svm_dec_values_title, svm_dec_values_file)
#     
#     
#     # Convert to the ROC format and generate ROCs 
#      
#     svm_roc_in = [(class_id, p_val[i]) for i, class_id in enumerate(class_ids.tolist())]
#     
#     
    #from PyROC.pyroc import ROCData
    #roc_data = ROCData(svm_roc_in)
    #roc_data.plot(rocs_img_title, file_name=rocs_file_name)

    

