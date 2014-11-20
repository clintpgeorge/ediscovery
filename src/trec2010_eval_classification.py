#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script is for evaluating the classification capability of the topic 
models that are created using variational methods and Gibbs sampling 
methods and with different number of topics (K). This script is tested 
on the TREC 2010 seed sets.    

Created on July 3, 2014

@author: Clint P. George 

'''
import time 
import os 
import logging
# import gensim
import numpy as np

from os.path import join, normpath, exists
from index_data_whoosh import LOG_FORMAT, TM_FOLDER_NAME#, WHOOSH_FOLDER_NAME

# from tm.process_query import load_lda_variables, load_dictionary
from libsvm.tools.grid import *
from libsvm.python.svmutil import svm_problem, svm_parameter, svm_train, svm_predict
from eval_tm_svm import find_optimal_RBF_C_gamma, save_tm_svm_data
from sklearn import svm
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold

NOTREVIEWED_CLASS_ID = -99
NEUTRAL_CLASS_ID = 0
RESPONSIVE_CLASS_ID = 1
UNRESPONSIVE_CLASS_ID = -1
RELEVANT_DIR_NAME = "1"
SEED = 1983 
DEFAULT_SVM_C = 32 
DEFAULT_SVM_g = 0.5 



def seed_docs_random_selection(corpus_doc_paths, num_seed_docs=100):
    '''
    Selecting seed documents randomly from the initial ranking results
    '''
    num_corpus_docs = len(corpus_doc_paths)
    req_num_seeds = min(num_seed_docs, num_corpus_docs)
    indices = range(0, num_corpus_docs)
    np.random.shuffle(indices)
    selected_random_indices = indices[0:req_num_seeds]

    seed_docs_ids = [corpus_doc_paths[random_index][0] 
                     for random_index in selected_random_indices]

    return seed_docs_ids

def sksvm_train_and_predict(doc_true_class_ids, features, seed_doc_ids, 
                          test_doc_ids, SVM_C=None, SVM_g=None):
    
    
    seed_docs_theta = [features[doc_id] for doc_id in seed_doc_ids] 
    seed_docs_cls = [doc_true_class_ids[doc_id] for doc_id in seed_doc_ids] 
    test_docs_features = [features[doc_id] for doc_id in test_doc_ids]
     
     
    if (SVM_C is None) or (SVM_g is None): # Parameter Grid search using seeds
        try: 
            C_g_dict = find_optimal_RBF_C_gamma(seed_docs_theta, seed_docs_cls, 
                                           random_state=SEED)
        except Exception, e:
            print e
            # use the default one 
            C_g_dict = {'C':DEFAULT_SVM_C, 'gamma':DEFAULT_SVM_g}
    else:
        C_g_dict = {'C':SVM_C, 'gamma':SVM_g}
    
    # --------------------------------------------------------------------------
    # SVM train (using sklearn)
    classifier = svm.SVC(kernel='rbf', probability=True, random_state=SEED, 
                        C=C_g_dict['C'], gamma=C_g_dict['gamma'])
    cf = classifier.fit(seed_docs_theta, seed_docs_cls)

    X_test = np.array(test_docs_features) # np.array(features)
    pred_prob = cf.predict_proba(X_test) 
    pred_labels = cf.predict(X_test)


    svm_prediction = [[doc_id, pred_labels[0], prob[1]] 
                      for doc_id, prob in enumerate(pred_prob)] 

    return C_g_dict, svm_prediction # [doc_id, svm_class_label, svm_decision_value]


def libsvm_train_and_predict(doc_true_class_ids, features, seed_doc_ids, 
                          test_doc_ids, SVM_C=None, SVM_g=None):

    
    
    seed_docs_theta = [features[doc_id] for doc_id in seed_doc_ids] 
    seed_docs_cls = [doc_true_class_ids[doc_id] for doc_id in seed_doc_ids] 
    test_docs_features = [features[doc_id] for doc_id in test_doc_ids]
     
     
    if (SVM_C is None) or (SVM_g is None): # Parameter Grid search using seeds
        try: 
#             C_g_dict = find_optimal_RBF_C_gamma(seed_docs_theta, seed_docs_cls, 
#                                            random_state=SEED)
            '''
            --------------------------------------------------- 
            This is using the grid search function in LIBSVM 
            TODO: This grid search has issues. Hence, 
            commenting this on July 04, 2014  
            ---------------------------------------------------     
            '''
            from tempfile import NamedTemporaryFile
            svm_data_file = ''
            with NamedTemporaryFile(delete=False) as fw: 
                svm_data_file = fw.name 
                for i, class_id in enumerate(seed_docs_cls):
                    features = ' '.join([str(class_id), 
                                         ' '.join(['%d:%.24f' % (k, theta_dk) 
                                                   for k, theta_dk in enumerate(seed_docs_theta[i])])])
                    print >>fw, features
            rate, param = find_parameters(svm_data_file, '-s 0 -t 2 -log2c -1,10,1 -log2g 3,-15,-2 -v 5 -gnuplot null')
            os.remove(svm_data_file)
            C_g_dict = {'C':param['c'], 'gamma':param['g'], 'Rate': rate}
        except Exception, e:
            print e
            # use the default one 
            C_g_dict = {'C':DEFAULT_SVM_C, 'gamma':DEFAULT_SVM_g}
    else:
        C_g_dict = {'C':SVM_C, 'gamma':SVM_g}
    
    # --------------------------------------------------------------------------
    # SVM train (using LIBSVM) 
    train_param = svm_parameter('-t 2 -s 0 -b 1 -c %f -g %f -q' % (C_g_dict['C'], C_g_dict['gamma']))
    train_prob  = svm_problem(seed_docs_cls, seed_docs_theta)
    seed_docs_svm_mdl = svm_train(train_prob, train_param)
     
#     # SVM prediction for all the documents in the corpus 
#     num_corpus_docs = len(features) 
#     svm_labels, _, svm_decision_values = svm_predict([0]*num_corpus_docs, 
#                                                      features, seed_docs_svm_mdl, 
#                                                      '-b 0 -q')
#     svm_prediction = [[doc_id, svm_label, svm_decision_values[doc_id][0]] 
#                       for doc_id, svm_label in enumerate(svm_labels)] 
    

    # SVM prediction only for the test documents
    num_test_docs = len(test_doc_ids)
    svm_labels, _, svm_decision_values = svm_predict([0]*num_test_docs, 
                                                     test_docs_features, 
                                                     seed_docs_svm_mdl, 
                                                     '-b 0 -q')
    
    svm_prediction = [[doc_id, svm_labels[i], svm_decision_values[i][0]] 
                      for i, doc_id in enumerate(test_doc_ids)] 



    return C_g_dict, svm_prediction # [doc_id, svm_class_label, svm_decision_value]



def eval_prediction(doc_true_class_ids, doc_prediction):
    '''
    doc_prediction: doc_id, predicted_class, prediction_score
    '''
    
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0 
    true_class_ids = []
    pred_probs = []
    
    for doc in doc_prediction:
        doc_id, predicted_cls, pred_prob = doc
        true_cls = doc_true_class_ids[doc_id]
        true_class_ids.append(true_cls)
        pred_probs.append(pred_prob) 
        
        if predicted_cls == RESPONSIVE_CLASS_ID: 
            if predicted_cls == true_cls: 
                true_positives += 1
            else: 
                false_positives += 1
        elif predicted_cls == UNRESPONSIVE_CLASS_ID:
            if predicted_cls == true_cls: 
                true_negatives += 1
            else: 
                false_negatives += 1
                
    fpr, tpr, _ = roc_curve(true_class_ids, pred_probs)
    roc_auc = auc(fpr, tpr) * 100.
            
    accuracy = ((true_positives + true_negatives) * 100.0 / 
                (true_positives + true_negatives + false_positives + false_negatives))
    
    if (true_positives + false_positives) == 0: 
        precision = -1
    else: 
        precision = true_positives * 100.0 / (true_positives + false_positives)
    
    if (true_positives + false_negatives) == 0: 
        recall = -1 
    else: 
        recall = true_positives * 100.0 / (true_positives + false_negatives)
    
    # print true_positives, true_negatives, false_positives, false_negatives, roc_auc
    
    return {'TP':true_positives, 'TN':true_negatives, 'FP':false_positives, 
            'FN':false_negatives, 'Accuracy':round(accuracy, 2), 
            'Recall':round(recall, 2), 'Precision':round(precision, 2), 
            'AUC':round(roc_auc, 2)}

def load_file_paths_index(index_file):
    '''
    Reads the file paths index file 
    and stores into a list 
    
    Returns: 
        file_path_tuples - list of (idx, root, file_name) 
    Arguments: 
        index_file - the index file name 
    ''' 
    file_path_tuples = []
    
    with open(index_file) as fp:
        for line in fp: 
            (idx, root, file_name) = line.strip().split(";") # ";"
            file_path_tuples.append((int(idx), os.path.normpath(root), 
                                     file_name))
    
    return file_path_tuples

def eval_classification(data_folder, output_folder, project_name, num_topics):

    # Checks whether the project folder exists 
    project_folder = join(output_folder, project_name)
    tm_folder = join(project_folder, TM_FOLDER_NAME)
#     whoosh_folder = join(project_folder, WHOOSH_FOLDER_NAME)
#     dict_file = join(tm_folder, project_name + '.dict')
#     ldac_file = join(tm_folder, project_name + '.ldac')
    path_index_file_name = join(tm_folder, project_name + '.path.index')    
    corpus_doc_paths = load_file_paths_index(path_index_file_name)
    
    doc_true_class_ids = {}
    class_ids = []
    positive_dir = normpath(join(data_folder, RELEVANT_DIR_NAME)) # TRUE positive documents  
    for doc_id, dirname, _ in corpus_doc_paths:
        if dirname == positive_dir:
            doc_true_class_ids[doc_id] = RESPONSIVE_CLASS_ID 
        else: 
            doc_true_class_ids[doc_id] = UNRESPONSIVE_CLASS_ID
        class_ids.append(doc_true_class_ids[doc_id])
    
    num_corpus_docs = len(corpus_doc_paths)
    seed_doc_ids = seed_docs_random_selection(corpus_doc_paths, 
                                              num_seed_docs=100)
    test_doc_ids = [doc_id for doc_id in range(0, num_corpus_docs) 
                    if doc_id not in seed_doc_ids]

    results = []
    for k in num_topics:
#         lda_model_file = join(tm_folder, project_name + '-K%d-VB.lda' % k)
#         lda_beta_file = join(tm_folder, project_name + '-K%d-VB.lda.beta' % k)
#         lda_cos_index_file = join(tm_folder, project_name + '-K%d-VB.lda.cos.index' % k)
#         dictionary = load_dictionary(dict_file)
#         vocabulary_size = len(dictionary)    
#         lda_mdl = gensim.models.ldamodel.LdaModel.load(lda_model_file)

        lda_theta_file = join(tm_folder, project_name + '-K%d-VB.lda.theta' % k)
        lda_theta = np.loadtxt(lda_theta_file) # loads the LDA theta from the model theta file 
        C_g_dict, svm_prediction = libsvm_train_and_predict(doc_true_class_ids, 
                                                          lda_theta.tolist(), 
                                                          seed_doc_ids, 
                                                          test_doc_ids)#, DEFAULT_SVM_C,  DEFAULT_SVM_g)
        svm_results = eval_prediction(doc_true_class_ids, svm_prediction)        
        svm_results = dict(svm_results.items() + C_g_dict.items()) 

        lda_theta_file2 = join(tm_folder, project_name + '-K%d-Gibbs.lda.theta' % k)
        lda_theta2 = np.loadtxt(lda_theta_file2) # loads the LDA theta from the model theta file 
        C_g_dict2, svm_prediction2 = libsvm_train_and_predict(doc_true_class_ids, 
                                                          lda_theta2.tolist(), 
                                                          seed_doc_ids, 
                                                          test_doc_ids, DEFAULT_SVM_C,  DEFAULT_SVM_g)
        svm_results2 = eval_prediction(doc_true_class_ids, svm_prediction2)
        svm_results2 = dict(svm_results2.items() + C_g_dict2.items()) 
        
        results.append({"K":k, "VB": svm_results, "Gibbs": svm_results2})
        
#     tfidf_theta_file = join(tm_folder, project_name + '.tfidf.theta')
    return results 

def eval_classification_cv(data_folder, output_folder, project_name, num_topics):

    # Checks whether the project folder exists 
    project_folder = join(output_folder, project_name)
    tm_folder = join(project_folder, TM_FOLDER_NAME)
    path_index_file_name = join(tm_folder, project_name + '.path.index')    
    corpus_doc_paths = load_file_paths_index(path_index_file_name)
    
    doc_true_class_ids = {}
    class_ids = []
    positive_dir = normpath(join(data_folder, RELEVANT_DIR_NAME)) # TRUE positive documents  
    for doc_id, dirname, _ in corpus_doc_paths:
        if dirname == positive_dir:
            doc_true_class_ids[doc_id] = RESPONSIVE_CLASS_ID 
        else: 
            doc_true_class_ids[doc_id] = UNRESPONSIVE_CLASS_ID
        class_ids.append(doc_true_class_ids[doc_id])
    
    cv_iterator = StratifiedKFold(class_ids, n_folds=5)
    for i, (test_doc_ids, seed_doc_ids) in enumerate(cv_iterator):
        print i, "test doc #", len(test_doc_ids), "seed doc #", len(seed_doc_ids)

    results = []
    for k in num_topics:
        lda_theta_file = join(tm_folder, project_name + '-K%d-VB.lda.theta' % k)
        lda_theta_file2 = join(tm_folder, project_name + '-K%d-Gibbs.lda.theta' % k)
        lda_theta = np.loadtxt(lda_theta_file).tolist() 
        lda_theta2 = np.loadtxt(lda_theta_file2).tolist() 
        
        svm_results = {}
        for i, (test_doc_ids, seed_doc_ids) in enumerate(cv_iterator):
            _, svm_prediction = libsvm_train_and_predict(doc_true_class_ids, 
                                                              lda_theta, 
                                                              seed_doc_ids, 
                                                              test_doc_ids) #, DEFAULT_SVM_C,  DEFAULT_SVM_g)
            eval_rs = eval_prediction(doc_true_class_ids, svm_prediction) 
            for sn in eval_rs.keys(): # online avg.
                if sn in svm_results:
                    svm_results[sn] = (i * svm_results[sn] + eval_rs[sn]) / (i+1.0) 
                else:
                    svm_results[sn] = eval_rs[sn]


        svm_results2 = {}
        for i, (test_doc_ids, seed_doc_ids) in enumerate(cv_iterator):
            _, svm_prediction2 = libsvm_train_and_predict(doc_true_class_ids, 
                                                              lda_theta2, 
                                                              seed_doc_ids, 
                                                              test_doc_ids) #, DEFAULT_SVM_C,  DEFAULT_SVM_g)
            eval_rs = eval_prediction(doc_true_class_ids, svm_prediction2)
            for sn in eval_rs.keys(): # online avg.
                if sn in svm_results2:
                    svm_results2[sn] = (i * svm_results2[sn] + eval_rs[sn]) / (i+1.0)
                else:
                    svm_results2[sn] = eval_rs[sn]
        
        results.append({"K":k, "VB": svm_results, "Gibbs": svm_results2})
        
#     tfidf_theta_file = join(tm_folder, project_name + '.tfidf.theta')
    return results 



#########################################################
## Hard coded values. Should be edited/checked before 
## running this script  
#########################################################
 
data_folder = "E:\\E-Discovery\\trec2010seeds-wa"
output_folder = "E:\\E-Discovery\\trec2010index-wa"
query_ids = [207] # [201, 202, 203, 207]
topic_counts = [5, 10, 15, 20, 30, 40, 50, 60, 70, 80]
#########################################################

#  
# print "Indexing documents...."
#  
# start_time = time.time()
     


import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages

pdf = PdfPages(os.path.join(output_folder, 'classification-results.pdf'))

for query_id in query_ids:
    query_data_folder = "%s\%d" % (data_folder, query_id)
    print "Query:", query_id
        
    # With stemmed tokens 
    project_name = "Q%d-S" % query_id
    sr = eval_classification_cv(query_data_folder, output_folder, project_name, topic_counts)
    
    print "Completed %s" % project_name
    
    # With raw tokens 
    project_name = "Q%d-R" % query_id
    rr = eval_classification_cv(query_data_folder, output_folder, project_name, topic_counts)

    print "Completed %s" % project_name
         
    
    font0 = FontProperties()
    axis_font = font0.copy()
    axis_font.set_family('arial')
    axis_font.set_size(12)
    title_font = font0.copy()
    title_font.set_family('arial')
    title_font.set_size(12)
    
    # To make a single figure with multiple sub plots 
    score_names = ['Accuracy', 'Precision', 'Recall', 'AUC'] 
    line_styles = ['ro-', 'kx-', 'c^-', 'gv-', 'bd-', 'y+-'] # for each model 
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    axl = [ax1, ax2, ax3, ax4]

    for i, mn in enumerate(score_names): # for each score  
        # For topic modeling with stems 
        topic_counts = []
        vb_scores = []
        gibbs_scores = [] 
        for trow in sr:
            topic_counts.append(trow["K"])
            vb_scores.append(trow["VB"][mn])
            gibbs_scores.append(trow["Gibbs"][mn])
        axl[i].plot(topic_counts, vb_scores, line_styles[0], label="VB: stems")
        axl[i].plot(topic_counts, gibbs_scores, line_styles[1], label="Gibbs: stems")
        y_min = min(vb_scores + gibbs_scores)
        y_max = max(vb_scores + gibbs_scores)

        # for topic modeling with raw tokens 
        vb_scores = []
        gibbs_scores = [] 
        for trow in rr:
            vb_scores.append(trow["VB"][mn])
            gibbs_scores.append(trow["Gibbs"][mn])
        axl[i].plot(topic_counts, vb_scores, line_styles[2], label="VB: raw")
        axl[i].plot(topic_counts, gibbs_scores, line_styles[3], label="Gibbs: raw")
        y_min = min(y_min, min(vb_scores + gibbs_scores))
        y_max = max(y_max, max(vb_scores + gibbs_scores))
            
        # configures the plot properties 
        axl[i].set_xlim(0., max(topic_counts) + 5)
        axl[i].set_ylim(y_min - 5, y_max + 5)
        axl[i].set_title(mn, fontproperties=title_font)  
        axl[i].set_xlabel('Number of Topics', fontproperties=axis_font) 
        axl[i].set_ylabel(mn, fontproperties=axis_font) 
        axl[i].legend(loc='lower right', prop={'size':12, 'family':'arial'})
    
    plt.subplots_adjust(left=.05, bottom=.05, right=.95, top=.95, wspace=.1, 
                        hspace=.25)
    plt.tight_layout()
    plt.show()
    pdf.savefig(fig)
    
pdf.close()
# print '\nIndexing time:', time.time() - start_time, 'seconds'        

