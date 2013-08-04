import re
import os
from lucene import BooleanClause
from lucenesearch.lucene_index_dir import search_lucene_index, get_indexed_file_details

from tm.process_query import load_lda_variables, load_dictionary, search_lda_model, search_lsi_model, load_lsi_variables, get_lda_topic_dist, print_topic_details
from utils.utils_file import read_config, load_file_paths_index, nexists
from PyROC.pyroc import ROCData, plot_multiple_roc
from utils.utils_email import parse_plain_text_email
import numpy as np 
from collections import defaultdict


METRICS_DICT =  {'SENS': 'Recall (Sensitivity)', 'SPEC': 'Specificity', 'ACC': 'Accuracy', 'EFF': 'Efficiency',
    'PPV': 'Precision (Positive Predictive Value)', 'NPV': 'Negative Predictive Value' , 'PHI':  'Phi Coefficient', 
    'F1': 'F1 Score', 'TN': 'True Negatives', 'TP': 'True Positives', 'FN': 'False Negatives', 'FP': 'False Positives' }

METRIC_COLORS = ['r', 'b', 'y', 'g', 'c', 'm', 'k', '#eeefff'] # *** depended on the number of metrics used *** 

def parse_query(query):
    
    queryText = query.strip() 

    query_words = []
    fields = []
    clauses = []
    filteredQuery = re.split(';', queryText)

    for l in filteredQuery:
        res = re.split(':', l )
        if len(res) > 1:
            fields.append(res[0])
            query_words.append(res[1])
            if res[2] is 'MUST':
                clauses.append(BooleanClause.Occur.MUST)
            elif res[2] is 'MUST_NOT':
                clauses.append(BooleanClause.Occur.MUST_NOT)
            else:
                clauses.append(BooleanClause.Occur.SHOULD)

    return (query_words, fields, clauses)




def search_li(query_list, limit, mdl_cfg):
    
    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']   

    rows = search_lucene_index(index_dir, query_list, limit)
    
    if len(rows) == 0: 
        print 'No documents found.'
        return 
    '''
    Sahil
    The first is maximum, considering this as the threshold
    normalizing scores and considering the score only above the threshold
    '''
    
    results = [[row[0], row[10]] for row in rows]
    
    return results


def search_tm(query_text, limit, mdl_cfg):   

    lda_dictionary, lda_mdl, lda_index, lda_file_path_index = load_tm(mdl_cfg)
    
    ts_results = search_lda_model(query_text, lda_dictionary, lda_mdl, lda_index, lda_file_path_index, limit)
    ## ts_results are in this format  [doc_id, doc_dir_path, doc_name, score] 
    
    # grabs the files details from the index 
    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']
    ts_results = get_indexed_file_details(ts_results, index_dir) 
    
    if len(ts_results) == 0: 
        print 'No documents found.'
        return 
        
    '''
    Sahil
    Considering documents that satisfy a certain condition
    '''
    results = [[row[0], ((float(row[10]) + 1.0) / 2.0)] for row in ts_results]
    
    return results


def search_tm_topics(topics_list, limit, mdl_cfg):   

    EPS = 1e-24
    lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']    
    lda_file_path_index = load_file_paths_index(path_index_file)    
    lda_theta = np.loadtxt(lda_theta_file, dtype=np.longdouble)
    num_docs, num_topics = lda_theta.shape
    
    print 'Number of documents: ', num_docs, ' number of topics: ', num_topics  
    
    unsel_topic_idx = [idx for idx in range(0, num_topics) if idx not in topics_list]
    

    sel = np.log(lda_theta[:, topics_list] + EPS)
    unsel = np.log(1.0 - lda_theta[:, unsel_topic_idx] + EPS)
    ln_score = sel.sum(axis=1) + unsel.sum(axis=1)  
    sorted_idx = ln_score.argsort(axis=0)[::-1]
    # score = np.exp(ln_score)
    
    ts_results = []
    min_ln_score = min(ln_score)
    n_ln_score = (1.0 - ln_score / min_ln_score)
    # n_ln_score = n_ln_score / max(n_ln_score)
    
    for i in range(0, min(limit, num_docs)):
        ts_results.append([lda_file_path_index[sorted_idx[i]][0], 
                          lda_file_path_index[sorted_idx[i]][1], 
                          lda_file_path_index[sorted_idx[i]][2], 
                          n_ln_score[sorted_idx[i]]])
        # print lda_file_path_index[sorted_idx[i]], ln_score[sorted_idx[i]], score[sorted_idx[i]] / max(score), n_ln_score[sorted_idx[i]] 
        

    # grabs the files details from the index 
    
    ts_results = get_indexed_file_details(ts_results, index_dir) 
    results = [[row[0], row[10]] for row in ts_results]
    
    return results


def search_lsi(query_text, limit, mdl_cfg):   

    lsi_dictionary, lsi_mdl, lsi_index, lsi_file_path_index = load_lsi(mdl_cfg)
    
    ts_results = search_lsi_model(query_text, lsi_dictionary, lsi_mdl, lsi_index, lsi_file_path_index, limit)
    ## ts_results are in this format  [doc_id, doc_dir_path, doc_name, score] 
    
    # grabs the files details from the index 
    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']
    ts_results = get_indexed_file_details(ts_results, index_dir) 
    
    if len(ts_results) == 0: 
        print 'No documents found.'
        return 
        
    '''
    Sahil
    Considering documents that satisfy a certain condition
    '''
    results = [[row[0], ((float(row[10]) + 1.0) / 2.0)] for row in ts_results]
    
    return results

def load_lsi(mdl_cfg):
    
    dictionary_file = mdl_cfg['CORPUS']['dict_file']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']
    lsi_mdl_file = mdl_cfg['LSI']['lsi_model_file']
    lsi_cos_index_file = mdl_cfg['LSI']['lsi_cos_index_file']
    
    if nexists(dictionary_file) and nexists(path_index_file):       
        lsi_file_path_index = load_file_paths_index(path_index_file)
        lsi_dictionary = load_dictionary(dictionary_file)
        
    if nexists(lsi_mdl_file) and nexists(lsi_cos_index_file): 
        lsi_mdl, lsi_index = load_lsi_variables(lsi_mdl_file, lsi_cos_index_file)
        
    return lsi_dictionary, lsi_mdl, lsi_index, lsi_file_path_index

def load_tm(mdl_cfg):
    
    dictionary_file = mdl_cfg['CORPUS']['dict_file']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']
    lda_mdl_file = mdl_cfg['LDA']['lda_model_file']
    lda_cos_index_file = mdl_cfg['LDA']['lda_cos_index_file']
    
    if nexists(dictionary_file) and nexists(path_index_file):       
        lda_file_path_index = load_file_paths_index(path_index_file)
        lda_dictionary = load_dictionary(dictionary_file)
        
    if nexists(lda_mdl_file) and nexists(lda_cos_index_file): 
        lda_mdl, lda_index = load_lda_variables(lda_mdl_file, lda_cos_index_file)
        
    return lda_dictionary, lda_mdl, lda_index, lda_file_path_index


def eval_results(positive_dir, negative_dir, responsive_docs, unresponsive_docs):
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    exceptions = 0
    
    for doc in responsive_docs:
        if os.path.exists(os.path.join(positive_dir, doc[0])) == True:
            true_positives += 1
            print 1, doc
        elif os.path.exists(os.path.join(negative_dir, doc[0])) == True:
            false_positives += 1
            print 0, doc
        else:
            exceptions += 1
            
    for doc in unresponsive_docs:
        if os.path.exists(os.path.join(positive_dir, doc[0])) == True:
            false_negatives += 1
        elif os.path.exists(os.path.join(negative_dir, doc[0])) == True:
            true_negatives += 1
        else:
            exceptions += 1
            
    print "True Positive:", true_positives
    print "True Negative:", true_negatives
    print "False Positive:", false_positives
    print "False Negative:", false_negatives
    print "Exceptions:", exceptions
    
    precision=float(true_positives)/(true_positives+false_positives)
    recall=float(true_positives)/(true_positives+false_negatives)
    accuracy=float(true_positives+true_negatives)/(true_positives+true_negatives+false_negatives+false_positives)
    print "Precision "+ str(precision)
    print "Recall "+ str(recall)
    print "Accuracy "+ str(accuracy) 
    return true_positives, true_negatives, false_positives, false_negatives, exceptions
     
def enhanced_evaluation(positive_dir,negative_dir,true_positives,false_positives):
    total_positives=0
    total_negatives=0
    for _, _, files in os.walk(positive_dir):
        for _ in files:
            total_positives+=1
            
    for _, _, files in os.walk(negative_dir):
        for _ in files:
            total_negatives+=1
            
    '''
    Total Positives = True Positive + False Negative
    Total Negatives = True Negative + False Positive
    '''
    
    true_negatives = total_negatives - false_positives
    false_negatives = total_positives - true_positives
    
    print "True Positive:", true_positives
    print "Actual True Negative:", true_negatives
    print "False Positive:", false_positives
    print "Actual False Negative:", false_negatives
    
    precision=float(true_positives)/(true_positives+false_positives)
    recall=float(true_positives)/(true_positives+false_negatives)
    accuracy=float(true_positives+true_negatives)/(true_positives+true_negatives+false_negatives+false_positives)
        
    print "Precision "+ str(precision)
    print "Recall "+ str(recall)
    print "Accuracy "+ str(accuracy)    
    

def normalize_lucene_score(docs):
    max_val = docs[0][1]
    for doc in docs:
        doc[1] = doc[1] / max_val
    return docs

def classify_docs(docs, threshold):
    responsive = []
    unresponsive = []
    for doc in docs:
        if float(doc[1]) >= threshold:
            responsive.append(doc)
        else:
            unresponsive.append(doc)
    return responsive, unresponsive

def convert_to_roc_format(docs, positive_dir):
    results = []
    for doc in docs:
        if os.path.exists(os.path.join(positive_dir, doc[0])):
            tuple_list = (1, doc[1])
            # print 1, doc
        else:
            tuple_list = (0, doc[1])
            # print 0, doc
        results.append(tuple_list)
    return results

def compare_true_retrieved_documents(m1_docs, m2_docs, positive_dir, score_thresholds):
    
    m1_pos_results = []
    m2_pos_results = []
    for doc in m1_docs:
        if os.path.exists(os.path.join(positive_dir, doc[0])) and float(doc[1]) >= score_thresholds[0]:
            m1_pos_results.append(doc[0])
            # print 's1', doc[0]

    for doc in m2_docs:
        if os.path.exists(os.path.join(positive_dir, doc[0])) and float(doc[1]) >= score_thresholds[1]:
            m2_pos_results.append(doc[0])
            # print 's2', doc[0]
            
    m1_pos_set = set(m1_pos_results)
    m2_pos_set = set(m2_pos_results)
 
    print '\nCommon files found: \n'
    print m1_pos_set.intersection(m2_pos_set)
 
    print '\nFiles found only in Set 1:'
    print m1_pos_set - m2_pos_set
    
    print '\nFiles found only in Set 2:'
    print m2_pos_set - m1_pos_set
    


def plot_roc_and_print_metrics(roc_result, roc_title='ROC Curve', file_name='ROC_plot.png', score_threshold=0.5):
    #Example instance labels (first index) with the decision function , score (second index)
    #-- positive class should be +1 and negative 0.

    roc = ROCData(roc_result)  #Create the ROC Object
    roc.auc() #get the area under the curve
    roc.plot(title=roc_title, file_name=file_name) #Create a plot of the ROC curve
    
    # prints confusion matrix 
    roc.confusion_matrix(score_threshold, True)
    
    # prints the evaluation metrics 
    roc.evaluateMetrics(roc.confusion_matrix(score_threshold), do_print=True)


def plot_results_rocs(results, labels, file_name, img_title): 
    
    roc_data_list = [ROCData(result) for result in results]
    plot_multiple_roc(roc_data_list, title=img_title, labels=labels, include_baseline=True, file_name=file_name)
    
    return roc_data_list


def print_results_eval_metrics(roc_data_list, labels, score_thresholds):
    
    roc_evals = []
    
    for i, roc_data in enumerate(roc_data_list):
        print '----------------------------------------------------------------------------------'
        print labels[i]
        print 
        print 'AUC:', roc_data.auc()
        print 
        
        # prints confusion matrix 
        roc_data.confusion_matrix(score_thresholds[i], True)
        
        # prints the evaluation metrics 
        roc_evals.append(roc_data.evaluateMetrics(roc_data.confusion_matrix(score_thresholds[i]), do_print=True))
        print '----------------------------------------------------------------------------------'
    
    return roc_evals


def plot_search_on_eval_metrics(roc_data_list, labels, query_id='Query'):
    import pylab
    
    roc_search_em = []
    score_thresholds = np.arange(0.0, 1.0, 0.05)
    print '----------------------------------------------------------------------------------'
    for i, roc_data in enumerate(roc_data_list):
        
        print labels[i], '( AUC:', roc_data.auc(), ')'
        print 
        
        eval_dict = defaultdict(list)
        for score_threshold in score_thresholds:
            cm = roc_data.confusion_matrix(score_threshold)
            em = roc_data.evaluateMetrics(cm)
            for key, value in dict(cm.items() + em.items()).iteritems():
                if key in eval_dict: 
                    eval_dict[key] += [value]
                else: 
                    eval_dict[key] = [value]

        roc_search_em.append(eval_dict)
        

    for score_key in ['ACC', 'PPV', 'SENS', 'F1', 'TN', 'TP']: # METRICS_DICT.keys():
        eval_file_name = '%s_%s.png' % (query_id, METRICS_DICT[score_key])
        
        pylab.clf()
        pylab.xlim((0, 1))
        pylab.xticks(pylab.arange(0,1.1,.1))
        if score_key not in ['TN', 'TP']:
            pylab.ylim((-0.5, 1))
            pylab.yticks(pylab.arange(0,1.1,.1))
        pylab.grid(True)
        pylab.xlabel('Score Thresholds')
        pylab.ylabel(METRICS_DICT[score_key])
        pylab.title(METRICS_DICT[score_key])
        
        for ix, eval_dict in enumerate(roc_search_em):
            pylab.plot(score_thresholds, eval_dict[score_key], linewidth=2, label=labels[ix], color=METRIC_COLORS[ix])
        
        if labels:
            pylab.legend(loc='lower left', prop={'size':9})
        
        pylab.savefig(eval_file_name, dpi=300, bbox_inches='tight', pad_inches=0.1)
    
        print 'Saved figure: ', eval_file_name
        
    print '----------------------------------------------------------------------------------'
    
    return (roc_search_em, score_thresholds)


def multi_plot_search_on_eval_metrics(roc_search_em, score_thresholds, labels, metrics, line_styles, query_id='Query'):
    import pylab
    
    pylab.clf()
    pylab.xlim((0, 1))
    pylab.xticks(pylab.arange(0,1.1,.1))
    pylab.ylim((-0.5, 1))
    pylab.yticks(pylab.arange(0,1.1,.1))
    pylab.grid(True)
    pylab.xlabel('Score Thresholds')
    
    for iix, score_key in enumerate(metrics): 
        for ix, eval_dict in enumerate(roc_search_em):
            pylab.plot(score_thresholds, eval_dict[score_key], 
                       linewidth=2, label=labels[ix] + '(%s)' % score_key, 
                       color=METRIC_COLORS[ix], linestyle=line_styles[iix])
        
    pylab.ylabel(' '.join(METRICS_DICT[score_key] for score_key in metrics))
    pylab.title(' '.join(METRICS_DICT[score_key] for score_key in metrics))
    
    if labels: pylab.legend(loc='lower left', prop={'size':9})

    eval_file_name = '%s_%s.png' % (query_id, '_'.join(METRICS_DICT[score_key] for score_key in metrics))
    pylab.savefig(eval_file_name, dpi=300, bbox_inches='tight', pad_inches=0.1)

    print 'Saved figure: ', eval_file_name
        
    print '----------------------------------------------------------------------------------'
    



def plot_roc_evals(roc_evals, roc_labels, score_thresholds, eval_file_name):
    import matplotlib.pyplot as plt

    
    # METRIC_COLORS = ['r', 'b', 'y', 'g', 'c', 'm', 'k', '#eeefff'] # *** depended on the number of metrics used *** 
    COLOR_BAR_WIDTH = 0.09       # the width of the bars
    
    def autolabel(rects):
        '''
        attach text labels to each rectangle 
        '''
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.03 * height, 
                    '%.2f' % float(height), ha='center', 
                    va='bottom', rotation=90, fontsize=6)
    
    
    
    N = len(roc_evals)
    
    metrics = defaultdict(list)
    for roc_eval in roc_evals:
        for key, value in roc_eval.iteritems():
            if key in metrics: 
                metrics[key] += [value]
            else: 
                metrics[key] = [value]
    

    x_axis_labels  = np.arange(N)  # the x locations for the groups

    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects = []
    i = 0
    labels = []
    for key, value in metrics.iteritems():
        rects.append(ax.bar(x_axis_labels +COLOR_BAR_WIDTH*i, value, COLOR_BAR_WIDTH, color=METRIC_COLORS[i]))
        labels.append(key)
        i += 1
    
    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Different Evaluation Metrics')
    ax.set_xticks( x_axis_labels  + N * COLOR_BAR_WIDTH )
    ax.set_xticklabels( roc_labels, rotation=25, fontsize=8 )
    # ax.legend( tuple(rects), tuple(labels))
    ax.legend(tuple(rects), tuple(labels), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size':8})
    
    for rect in rects: 
        autolabel(rect)
    
    fig.savefig(eval_file_name, dpi=300, bbox_inches='tight', pad_inches=0.1)



def find_seed_document(docs, positive_dir):
    for doc in docs:
        if os.path.exists(os.path.join(positive_dir,doc[0]))==True:
            return os.path.join(positive_dir,doc[0])
    return ""

def append_negative_docs(docs, test_directory):
    '''
    Used only for Lucene 
    '''
    
    result_dict = dict()
    result = []
    
    for doc in docs:
        result.append(doc)
        result_dict[doc[0]] = True
    
    for _, _, files in os.walk(test_directory):
        for file_name in files:
            if file_name not in result_dict:
                result.append([file_name, 0.0])
                
    return result        


def lda_with_all_responsive(positive_dir, limit, mdl_cfg):
    
    import operator
    from os import listdir
    from os.path import isfile, join
    from scipy.cluster.vq import kmeans, vq 
    
    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']
    num_topics = int(mdl_cfg['LDA']['num_topics'])
    lda_dictionary, lda_mdl, lda_index, lda_file_path_index = load_tm(mdl_cfg)
    num_clusters = 3     
    
    positive_files = [join(positive_dir,f) for f in listdir(positive_dir) if isfile(join(positive_dir,f))]
    
    seed_doc_texts = []
    for fn in positive_files:
        _, _, _, _, body_text, _, _ = parse_plain_text_email(fn)
        seed_doc_texts.append(body_text)
    
    # Finds the centroid of the responsive documents 

    doc_tds = get_lda_topic_dist(seed_doc_texts, lda_dictionary, lda_mdl, num_topics)
    centroids, _ = kmeans(doc_tds, num_clusters, iter=100) # do k means 
    idx,_ = vq(doc_tds, centroids) # assign each sample to a cluster
    
    tally = defaultdict(int)
    for i in idx: tally[i] += 1
    # print tally
    max_idx = max(tally.iteritems(), key=operator.itemgetter(1))[0] # takes the centroid with max cardinality 
    max_centroid_td = centroids[max_idx]    
    query_td = [(i, value) for i, value in enumerate(max_centroid_td) if value > 1e-4] # converts to the gensim format 

    # display details 
    print_topic_details(query_td, lda_mdl)
    # print 'Query distribution:', query_td
    # print len(max_centroid_td), max_centroid_td
    # print len(query_td), query_td
    
    # querying based on cosine distance from the centroid 
    
    sims = lda_index[query_td] # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    
    ## Identifies responsive documents
     
    responsive_docs_idx = sims[0:limit]
    
    responsive_docs = [] 
    for (doc_id, score) in responsive_docs_idx: 
        doc = list(lda_file_path_index[doc_id]) # i.e., [doc_id, doc_dir_path, doc_name]
        doc.append(score)
        responsive_docs.append(doc)
    
    # grabs the files details from the index 
    
    ts_results = get_indexed_file_details(responsive_docs, index_dir) 
    results = [[row[0], ((float(row[10]) + 1.0) / 2.0)] for row in ts_results]
    
    return results

def lda_multiple_seeds(positive_dir, limit, mdl_cfg):
    docs = search_tm(' '.join(query_words), limit, mdl_cfg)
    seed_list = find_seed_list_document(docs, positive_dir)
    results = dict() 
    for doc in seed_list:
        (_, _,_ ,_ , body_text, _, _) = parse_plain_text_email(os.path.join(positive_dir,doc[0]))
        doc_text = body_text + u' ' + ' '.join(query_words) 
        docs = search_tm(doc_text, limit, mdl_cfg)
        results = add_to_final_list(results,docs)
    return results

def lsi_multiple_seeds(positive_dir, limit, mdl_cfg):
    docs = search_lsi(' '.join(query_words), limit, mdl_cfg)
    seed_list = find_seed_list_document(docs, positive_dir)
    results = dict() 
    for doc in seed_list:
        (_, _,_ ,_ , body_text, _, _) = parse_plain_text_email(os.path.join(positive_dir,doc[0]))
        doc_text = body_text + u' ' + ' '.join(query_words) 
        docs = search_lsi(doc_text, limit, mdl_cfg)
        results = add_to_final_list(results,docs)
    return results


def find_seed_list_document(docs, positive_dir):
    i=0;
    result = []
    for doc in docs:
        if os.path.exists(os.path.join(positive_dir,doc[0])):
            result.append(doc)
            i = i + 1
            if i == NO_OF_SEED:
                break;
        
    
    return result

            
def add_to_final_list(results,docs):
    rank = 1
    for doc in docs:
        if doc[0] in results:
            doc_object = results[doc[0]]
            doc_object[0].append(rank)
            doc_object[1].append(float(doc[1]))
            results[doc[0]] = doc_object
        else:
            doc_object = []
            rank_list = []
            rank_list.append(rank)
            score_list = []
            score_list.append(float(doc[1]))
            doc_object.append(rank_list)
            doc_object.append(score_list)
            results[doc[0]] = doc_object
            
        rank = rank + 1
    return results

def prepare_results_roc_max(results,positive_dir):
    
    result = []
    for name in results:
        
        if os.path.exists(os.path.join(positive_dir, name))==True:    
            tuple_list = (1, np.max(results[name][1]))            
        else:
            tuple_list = (0, np.max(results[name][1]))
        result.append(tuple_list)
        
    return result


     
#===============================================================================
# '''
# TEST SCRIPTS 
# 
# '''
#===============================================================================

# ************************************************************************************
# ****** DO ALL HARD-CODINGS HERE ****************************************************
# ************************************************************************************


## ***** BEGIN change the following each query *********

query_id = 201
config_file = "gui/project1.cfg" # configuration file, created using the SMARTeR GUI 
test_directory = "F:\\Research\\datasets\\trec2010\\Enron\\201"# the directory where we keep the training set (TRUE negatives and TRUE positives) 
positive_dir = os.path.join(test_directory, "1") # TRUE positive documents 
negative_dir = os.path.join(test_directory, "0") # TRUE negative documents 

#201
query = "all:pre-pay:May;all:swap:May"
seed_doc_name = os.path.join(positive_dir, '3.215558.MUQRZJDAZEC5GAZM0JG5K2HCKBZQA1TEB.txt') # query specific seed document
#202
#query = "all:FAS:May;all:transaction:May;all:swap:May;all:trust:May;all:Transferor:May;all:Transferee:May"
#seed_doc_name = os.path.join(positive_dir, '3.347.FXJYYKNIL4HGYJ4O5M3XWQS13XPQA2DBA.txt') # query specific seed document
#203
#seed_doc_name = os.path.join(positive_dir, '3.61439.MP1MJADJGZCPXM4LTCWDOCJDCL20JRYEB.txt') # query specific seed document
#query = "all:forecast:May;all:earnings:May;all:profit:May;all:quarter:May;all:balance sheet:May"
#204
#seed_doc_name = os.path.join(positive_dir, '3.76893.LECLWOBIZDO00GYS41VBF3KKWFL1G2RJA.txt') # query specific seed document
#query = "all:retention:May;all:compliance:May;all:preserve:May;all:discard:May;all:destroy:May;all:delete:May;all:clean:May;all:eliminate:May;all:shred:May;all:schedule:May;all:period:May;all:documents:May;all:file:May;all:policy:May;all:e-mail:May"
#205
#query = "all:electricity:May;all:electric:May;all:loads:May;all:hydro:May;all:generator:May;all:power:May"
#seed_doc_name = os.path.join(positive_dir, '3.24517.JQ2KBXZBBQ1YGHFCC30JOU2QUANNINE2B.txt') # query specific seed document
#206 
#query = "all:analyst:May;all:credit:May;all:rating:May;all:grade:May"
#seed_doc_name = os.path.join(positive_dir, '3.272223.IJVCMQKKAFUIQ3VDIUKIRUEMO2H4EOKNA.txt') # query specific seed document
#207     
#query = "all:football:May;all:Eric Bass:May" 
#seed_doc_name = os.path.join(positive_dir, '3.16296.KD0CXPYOCOXT15ZTVIGVF44AUNQD2I23B.txt') # query specific seed document 

## ***** END change this each query *********

limit = 1000
img_extension  = '.png'


eval_file_name = '%s_eval_bars' % query_id + img_extension
roc_file_names = ['LS_ROC', 'LDA_ROC_KW', 'LSI_ROC_KW', 'LDA_ROC_SEED', 'LSI_ROC_SEED'] 
score_thresholds = [0.51, 0.7, 0.51, 0.51, 0.8, 0.52,0.51,0.8]
NO_OF_SEED = 5

# ************************************************************************************



#===============================================================================
# Reads the configuration file 
# Parses the user query  
# Combines the query with a seed 
#===============================================================================

mdl_cfg = read_config(config_file)
query_words, fields, clauses = parse_query(query)
print query_words, fields

query_text = ' '.join(query_words)

(receiver, sender, cc, subject, body_text, bcc, date) = parse_plain_text_email(seed_doc_name)
seed_doc_text = body_text + u' ' + query_text 

print query_text
print seed_doc_text

#===============================================================================
# Here, we perform Lucene, LDA, and LSI search based on a given query. 
#===============================================================================

print "\nLucene Search:\n"
 
docs = search_li([query_words, fields, clauses], limit, mdl_cfg)
docs = normalize_lucene_score(docs)
docs1 = append_negative_docs(docs, test_directory)
r1 = convert_to_roc_format(docs1, positive_dir)
# plot_roc_and_print_metrics(r1, roc_labels[0], roc_file_names[0] + img_extension, score_thresholds[0])

print "\nLDA Search (with keywords):\n"

docs2 = search_tm(query_text, limit, mdl_cfg)
r2 = convert_to_roc_format(docs2, positive_dir)    
# plot_roc_and_print_metrics(r2, roc_labels[1], roc_file_names[1] + img_extension, score_thresholds[1])


compare_true_retrieved_documents(docs1, docs2, positive_dir, [0.51, .7])

print "\nLDA Search on topics:\n"
docs = search_tm_topics([7, 29, 0, 24, 6], limit, mdl_cfg) # the topic indices should changed according to each query 
r10 = convert_to_roc_format(docs, positive_dir)
print r10


print "\nLDA Search (using a seed doc):\n"
docs = search_tm(seed_doc_text, limit, mdl_cfg)
r4 = convert_to_roc_format(docs, positive_dir)

print "\nLDA Search  (using the centroid of all responsive docs):\n"
docs = lda_with_all_responsive(positive_dir, limit, mdl_cfg)
r6 = convert_to_roc_format(docs, positive_dir)

print "\nLDA Search (with multiple seeds):\n"
results = lda_multiple_seeds(positive_dir, limit, mdl_cfg)
r7 = prepare_results_roc_max(results,positive_dir)


print "\nLSI Search (with keywords):\n"

docs = search_lsi(query_text, limit, mdl_cfg)
r3 = convert_to_roc_format(docs, positive_dir)
# plot_roc_and_print_metrics(r3, roc_labels[2], roc_file_names[2] + img_extension, score_thresholds[2])

print "\nLSI Search  (using a seed doc):\n"
docs = search_lsi(seed_doc_text, limit, mdl_cfg)
r5 = convert_to_roc_format(docs, positive_dir)

print "\nLSI Search (with multiple seeds):\n"
results = lsi_multiple_seeds(positive_dir, limit, mdl_cfg)
r8 = prepare_results_roc_max(results,positive_dir)



#===============================================================================
# # plot ROCs for all different methods 
#===============================================================================
rocs_file_name = '%s_ROC_plots' % query_id + img_extension
rocs_img_title = 'Query %s: ROCs of all methods' % query_id 
roc_labels = ['Lucene: with keywords', 'LDA: with keywords', 'LSI: with keywords', 'LDA: with a seed doc', 'LSI: with a seed doc', 'LDA: with the centroid of resp.', 'LDA: with multiple seeds.', 'LSI: with multiple seeds.']
results_list = [r1, r2, r3, r4, r5, r6, r7, r8]
roc_data_list = plot_results_rocs(results_list, roc_labels, rocs_file_name, rocs_img_title)
print 

roc_search_em, score_thresholds = plot_search_on_eval_metrics(roc_data_list, roc_labels, str(query_id))

metrics = ['PPV', 'SENS']
line_styles = ["-",":"]
multi_plot_search_on_eval_metrics(roc_search_em, score_thresholds, roc_labels, metrics, line_styles, str(query_id))

#===============================================================================
# # LDA methods 
#===============================================================================


rocs_file_name = '%s_LDA_ROC_plots' % query_id + img_extension
rocs_img_title = 'Query %s: ROCs of LDA methods' % query_id 
roc_labels = ['Lucene: with keywords', 'LDA: with keywords', 'LDA: with a seed doc', 
              'LDA: with the centroid of resp.', 'LDA: with multiple seeds.', 
              'LDA: Search on topics']
results_list = [r1, r2, r4, r6, r7, r10]
roc_data_list = plot_results_rocs(results_list, roc_labels, rocs_file_name, rocs_img_title)
print 

roc_search_em, score_thresholds = plot_search_on_eval_metrics(roc_data_list, roc_labels, str(query_id) + '_LDA')

metrics = ['PPV', 'SENS']
line_styles = ["-",":"]
multi_plot_search_on_eval_metrics(roc_search_em, score_thresholds, roc_labels, metrics, line_styles, str(query_id) + '_LDA')


#===============================================================================
# # LSI methods 
#===============================================================================

rocs_file_name = '%s_LSI_ROC_plots' % query_id + img_extension
rocs_img_title = 'Query %s: ROCs of LSI methods' % query_id 
roc_labels = ['Lucene: with keywords', 'LSI: with keywords', 'LSI: with a seed doc', 'LSI: with multiple seeds.']
results_list = [r1, r3, r5, r8]
roc_data_list = plot_results_rocs(results_list, roc_labels, rocs_file_name, rocs_img_title)
print 

roc_search_em, score_thresholds = plot_search_on_eval_metrics(roc_data_list, roc_labels, str(query_id) + '_LSI')

metrics = ['PPV', 'SENS']
line_styles = ["-",":"]
multi_plot_search_on_eval_metrics(roc_search_em, score_thresholds, roc_labels, metrics, line_styles, str(query_id) + '_LSI')


#===============================================================================
# # Best methods 
#===============================================================================


##===============================================================================
## # plot evaluation metrics for all different methods 
##===============================================================================
#
#roc_evals = print_results_eval_metrics(roc_data_list, roc_labels, score_thresholds)
#plot_roc_evals(roc_evals, roc_labels, score_thresholds, eval_file_name)


