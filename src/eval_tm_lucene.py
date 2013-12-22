import re
import os
from lucene import BooleanClause
from lucenesearch.lucene_index_dir import boolean_search_lucene_index, get_indexed_file_details

from tm.process_query import load_lda_variables, load_dictionary, search_lda_model, search_lsi_model, load_lsi_variables, get_dominant_query_topics, print_lda_topics_on_entropy
from utils.utils_file import read_config, load_file_paths_index, nexists
from PyROC.pyroc import ROCData, plot_multiple_roc
import numpy as np 
from collections import defaultdict
from utils.utils_email import lemmatize_tokens, stem_tokens, regex_tokenizer


METRICS_DICT =  {'SENS': 'Recall (Sensitivity)', 'SPEC': 'Specificity', 'ACC': 'Accuracy', 'EFF': 'Efficiency',
    'PPV': 'Precision (Positive Predictive Value)', 'NPV': 'Negative Predictive Value' , 'PHI':  'Phi Coefficient', 
    'F1': 'F1 Score', 'TN': 'True Negatives', 'TP': 'True Positives', 'FN': 'False Negatives', 'FP': 'False Positives' }

METRIC_COLORS = ['r', 'b', 'y', 'g', 'c', 'm', 'k', '#eeefff','#ffee00', '#ff00ee','#ccbbff'] # *** depended on the number of metrics used *** 




def search_li(query_string, limit, mdl_cfg):
    
    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']   

    rows = boolean_search_lucene_index(index_dir, query_string, limit)
    
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

    # Normalize the similarity scores 
    results = [[row[0], ((float(row[10]) + 1.0) / 2.0)] for row in ts_results]
    
    return results


def search_tm_topics(topics_list, limit, mdl_cfg):   
    '''
    Performs search on the topic model using relevant  
    topic indices 
    '''

    EPS = 1e-24 # a constant 
    lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']    
    lda_file_path_index = load_file_paths_index(path_index_file) # loads the file paths    
    lda_theta = np.loadtxt(lda_theta_file, dtype=np.longdouble) # loads the LDA theta from the model theta file 
    num_docs, num_topics = lda_theta.shape
    
    print 'LDA-theta is loaded: number of documents: ', num_docs, ' number of topics: ', num_topics  
    
    unsel_topic_idx = [idx for idx in range(0, num_topics) if idx not in topics_list]
    sel = np.log(lda_theta[:, topics_list] + EPS)
    unsel = np.log(1.0 - lda_theta[:, unsel_topic_idx] + EPS)
    ln_score = sel.sum(axis=1) + unsel.sum(axis=1)  
    sorted_idx = ln_score.argsort(axis=0)[::-1]
    # score = np.exp(ln_score)
    
    # Normalize the topic index search score 
    # TODO: this is an adhoc method right now. May come back later... 
    min_ln_score = min(ln_score)
    n_ln_score = (1.0 - ln_score / min_ln_score)

    ts_results = []
    for i in range(0, min(limit, num_docs)):
        ts_results.append([lda_file_path_index[sorted_idx[i]][0], # document id  
                          lda_file_path_index[sorted_idx[i]][1], # document directory path   
                          lda_file_path_index[sorted_idx[i]][2], # document name
                          n_ln_score[sorted_idx[i]]]) # similarity score 
        # print lda_file_path_index[sorted_idx[i]], ln_score[sorted_idx[i]], n_ln_score[sorted_idx[i]], score[sorted_idx[i]] 
        

    # grabs the files details from the index     
    ts_results = get_indexed_file_details(ts_results, index_dir) 
    
    results = [[row[0], float(row[10])] for row in ts_results] # Note: we need a float conversion because it's retrieving as string 
    
    return results

def search_tm_sel_topics_cos(topics_list, topics_prob, limit, mdl_cfg):   

    lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']    
    lda_file_path_index = load_file_paths_index(path_index_file)    
    lda_theta = np.loadtxt(lda_theta_file, dtype=np.longdouble)
    num_docs, num_topics = lda_theta.shape
    
    print 'Number of documents: ', num_docs, ' number of topics: ', num_topics  
    
    from scipy.spatial.distance import cosine 
    topics_prob = np.array(topics_prob)
    sel = lda_theta[:, topics_list]
    cos_scores = np.zeros(num_docs)
    for i in range(0, num_docs):
        cos_scores[i] = cosine(topics_prob, sel[i, :])

    sorted_idx = cos_scores.argsort(axis=0)[::-1]
    
    ts_results = []
    
    for i in range(0, min(limit, num_docs)):
        ts_results.append([lda_file_path_index[sorted_idx[i]][0], 
                          lda_file_path_index[sorted_idx[i]][1], 
                          lda_file_path_index[sorted_idx[i]][2], 
                          cos_scores[sorted_idx[i]]])
        print lda_file_path_index[sorted_idx[i]], cos_scores[sorted_idx[i]]
        

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

#
#def lda_with_all_responsive(positive_dir, limit, mdl_cfg):
#    
#    import operator
#    from os import listdir
#    from os.path import isfile, join
#    from scipy.cluster.vq import kmeans, vq 
#    
#    index_dir = mdl_cfg['LUCENE']['lucene_index_dir']
#    num_topics = int(mdl_cfg['LDA']['num_topics'])
#    lda_dictionary, lda_mdl, lda_index, lda_file_path_index = load_tm(mdl_cfg)
#    num_clusters = 3     
#    
#    positive_files = [join(positive_dir,f) for f in listdir(positive_dir) if isfile(join(positive_dir,f))]
#    
#    seed_doc_texts = []
#    for fn in positive_files:
#        _, _, _, _, body_text, _, _ = parse_plain_text_email(fn)
#        seed_doc_texts.append(body_text)
#    
#    # Finds the centroid of the responsive documents 
#
#    doc_tds = get_lda_topic_dist(seed_doc_texts, lda_dictionary, lda_mdl, num_topics)
#    centroids, _ = kmeans(doc_tds, num_clusters, iter=100) # do k means 
#    idx,_ = vq(doc_tds, centroids) # assign each sample to a cluster
#    
#    tally = defaultdict(int)
#    for i in idx: tally[i] += 1
#    # print tally
#    max_idx = max(tally.iteritems(), key=operator.itemgetter(1))[0] # takes the centroid with max cardinality 
#    max_centroid_td = centroids[max_idx]    
#    query_td = [(i, value) for i, value in enumerate(max_centroid_td) if value > 1e-4] # converts to the gensim format 
#
#    # display details 
#    print_dominant_query_topics(query_td, lda_mdl)
#    # print 'Query distribution:', query_td
#    # print len(max_centroid_td), max_centroid_td
#    # print len(query_td), query_td
#    
#    # querying based on cosine distance from the centroid 
#    
#    sims = lda_index[query_td] # perform a similarity query against the corpus
#    sims = sorted(enumerate(sims), key=lambda item: -item[1])
#    
#    
#    ## Identifies responsive documents
#     
#    responsive_docs_idx = sims[0:limit]
#    
#    responsive_docs = [] 
#    for (doc_id, score) in responsive_docs_idx: 
#        doc = list(lda_file_path_index[doc_id]) # i.e., [doc_id, doc_dir_path, doc_name]
#        doc.append(score)
#        responsive_docs.append(doc)
#    
#    # grabs the files details from the index 
#    
#    ts_results = get_indexed_file_details(responsive_docs, index_dir) 
#    results = [[row[0], ((float(row[10]) + 1.0) / 2.0)] for row in ts_results]
#    
#    return results
#def lda_multiple_seeds(positive_dir, limit, mdl_cfg):
#    docs = search_tm(' '.join(query_words), limit, mdl_cfg)
#    seed_list = find_seed_list_document(docs, positive_dir)
#    results = dict() 
#    for doc in seed_list:
#        (_, _,_ ,_ , body_text, _, _) = parse_plain_text_email(os.path.join(positive_dir,doc[0]))
#        doc_text = body_text + u' ' + ' '.join(query_words) 
#        docs = search_tm(doc_text, limit, mdl_cfg)
#        results = add_to_final_list(results,docs)
#    return results
#
#def lsi_multiple_seeds(positive_dir, limit, mdl_cfg):
#    docs = search_lsi(' '.join(query_words), limit, mdl_cfg)
#    seed_list = find_seed_list_document(docs, positive_dir)
#    results = dict() 
#    for doc in seed_list:
#        (_, _,_ ,_ , body_text, _, _) = parse_plain_text_email(os.path.join(positive_dir,doc[0]))
#        doc_text = body_text + u' ' + ' '.join(query_words) 
#        docs = search_lsi(doc_text, limit, mdl_cfg)
#        results = add_to_final_list(results,docs)
#    return results
#
#def lda_multiple_seeds_lu(positive_dir, limit, mdl_cfg,query_list):
#      
#    docs = search_li(query_list, limit, mdl_cfg)
#    seed_list = find_seed_list_document(docs, positive_dir)
#    results = dict() 
#    for doc in seed_list:
#        (_, _,_ ,_ , body_text, _, _) = parse_plain_text_email(os.path.join(positive_dir,doc[0]))
#        doc_text = body_text + u' ' + ' '.join(query_words) 
#        docs = search_tm(doc_text, limit, mdl_cfg)
#        results = add_to_final_list(results,docs)
#    return results
#
#def lsi_multiple_seeds_lu(positive_dir, limit, mdl_cfg,query_list):
#      
#    docs = search_li(query_list, limit, mdl_cfg)
#    seed_list = find_seed_list_document(docs, positive_dir)
#    results = dict() 
#    for doc in seed_list:
#        (_, _,_ ,_ , body_text, _, _) = parse_plain_text_email(os.path.join(positive_dir,doc[0]))
#        doc_text = body_text + u' ' + ' '.join(query_words) 
#        docs = search_lsi(doc_text, limit, mdl_cfg)
#        results = add_to_final_list(results,docs)
#    return results
#
#
#def find_seed_list_document(docs, positive_dir):
#    i=0;
#    result = []
#    for doc in docs:
#        if os.path.exists(os.path.join(positive_dir,doc[0])):
#            result.append(doc)
#            i = i + 1
#            if i == NO_OF_SEED:
#                break;
#        
#    
#    return result

            
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

def prepare_results_max(results,positive_dir):
    
    result = []
    for name in results:
        if os.path.exists(os.path.join(positive_dir, name))==True:    
            tuple_list = [name, np.max(results[name][1])]           
        else:
            tuple_list = [name, np.max(results[name][1])]
        result.append(tuple_list)
    result = sorted(result, key=lambda student: student[1])
    return result

def compare_true_retrieved_documents(m1_docs, m2_docs, positive_dir, score_thresholds, flag=False):
    
    m1_pos_results = []
    m2_pos_results = []
    for doc in m1_docs:
            if os.path.exists(os.path.join(positive_dir, doc[0])) and float(doc[1]) >= score_thresholds[0]:
                m1_pos_results.append(doc[0])
                print 's1', doc[0]

    if flag==False:
        m2_temp_docs=m2_docs
    else:
        m2_temp_docs = prepare_results_max(m2_docs,positive_dir)
    
    false_positive=0
    for doc in m2_temp_docs:
        if float(doc[1]) >= score_thresholds[1]:
            if os.path.exists(os.path.join(positive_dir, doc[0])) :
                m2_pos_results.append(doc[0])
                print 's2', doc[0]
            else:
                false_positive+=1
    print false_positive
    print len(m2_pos_results)
            
            
    m1_pos_set = set(m1_pos_results)
    m2_pos_set = set(m2_pos_results)
 
    print '\Set 1: \n'
    print len(m1_pos_set)
    
    print '\nset2: \n'
    print len(m2_pos_set)
 
    print '\nUnion files found: \n'
    print len(m1_pos_set.union(m2_pos_set))
 
    print '\nCommon files found: \n'
    print len(m1_pos_set.intersection(m2_pos_set))
 
    print '\nFiles found only in Set 1:'
    print len(m1_pos_set - m2_pos_set)
    
    print '\nFiles found only in Set 2:'
    print len(m2_pos_set - m1_pos_set)
    
def lu_append_nonresp(docs, root_dir):
    '''
    Used only for Lucene 
    '''
    
    result_dict = dict()
    result_list = []
    result = dict()
    score_list = []
    
    for doc in docs:
        result[doc[0]] = True
        result_list.append(doc)
        result_dict[doc[0]] = doc[1]
        score_list.append(doc[1])
    
    min_score = np.min(score_list) * 1e-5
    
    for _, _, files in os.walk(root_dir):
        for file_name in files:
            if file_name not in result:
                result_dict[file_name] = min_score
                result_list.append([file_name, min_score])
                
    return result_dict, result_list



def fuse_lucene_tm_scores(results_lucene, results_tm):
    '''
    This method fuse document relevancy scores from 
    Lucene with topic modeling based ranking scores. 
    Currently, it's based on Geometric mean of both 
    scores. 
    '''
    
    result = []
    for res_tm in results_tm:
        lu_score = results_lucene[res_tm[0]]
        mult_score = float(lu_score) * float(res_tm[1]) 
        result.append([res_tm[0], mult_score])

    result = sorted(result, key=lambda student: student[1])
    
    return result


def lu_normalize_scores_wrt_tm_scores(docs1,docs2):
    rank_list = []
    temp_score = 100
    for doc in docs2:
        if temp_score > doc[1]:
            temp_score = doc[1]
            rank_list.append(doc[1])
    rank_len=len(rank_list)
    i = 0
    docs_new = []
    temp_score=100
    for doc in docs1:
        if temp_score > doc[1]:
            temp_score = doc[1]
            i += 1
        if(i < rank_len):
            docs_new.append([doc[0],rank_list[i]])
        else:
            docs_new.append([doc[0],rank_list[rank_len-1]])
    
    return docs_new

     

def plot_doc_class_predictions(lda_res, file_name, img_extension='.eps'):
    '''
    Plots the distribution of document class assignments 
    '''

    import pylab 

    pos_cls = [rank_score for (cls_id, rank_score) in lda_res if cls_id == 1]   
    neg_cls = [rank_score for (cls_id, rank_score) in lda_res if cls_id == 0] 
    # print 'Class 1:', pos_cls
    # print 'Class 2:', neg_cls
    
    
#    pylab.figure(11)
#    pylab.xlabel('Rank scores')
#    pylab.ylabel('Classes')
#    pylab.title('Document class assignments')
#    pylab.ylim((0.5,1.3))
#    pylab.xlim((0.0,1.0))
#    pylab.plot(pos_cls, np.ones(len(pos_cls)) , 'g+', linewidth=2)
#    pylab.plot(neg_cls, np.ones(len(neg_cls)) - 0.2, 'ro', linewidth=2)
#    pylab.savefig(file_name + '-cls' + img_extension, dpi=300, bbox_inches='tight', pad_inches=0.1)

    # and exercise the weights option by arbitrarily giving the first half
    # of each series only half the weight of the others:
    
    w0 = np.ones_like(pos_cls)
    w0[:len(pos_cls)/2] = 0.5
    w1 = np.ones_like(neg_cls)
    w1[:len(neg_cls)/2] = 0.5
    
    pylab.figure(12)
    pylab.xlabel('Rank scores')
    pylab.ylabel('Number of documents')
    pylab.title('Distribution of Document Class Assignments')
    pylab.hist( [pos_cls, neg_cls], 25, weights=[w0, w1], histtype='bar', color=['g', 'r'])
    pylab.savefig(file_name + '-hist' + img_extension, dpi=300, bbox_inches='tight', pad_inches=0.1)
    
    

def eval_ranking_methods(file_prefix, config_file, 
                         test_directory, 
                         tm_query, 
                         limit = 1000, 
                         img_extension  = '.eps'):
    
    lucene_query = 'all:(%s)' % tm_query # search in all fields 
    print 'Lucene query:', lucene_query
    print 'TM query:', tm_query
    positive_dir = os.path.join(test_directory, "1") # TRUE positive documents 
    TOP_K_TOPICS = 5 # the number topics used for Topic-LDA 
    rocs_file_name = '%s-ROCs' % file_prefix + img_extension
    rocs_img_title = '' # %s: ROC curves' % file_prefix 
    roc_labels = ['Lucene ranking', 
                  'Keyword-LDA ranking' , 
                  'Keyword-LDA * Lucene ranking', 
                  'Topic-LDA ranking' , 
                  'Topic-LDA * Lucene Ranking',
                  'Keyword-LSI ranking',
                  'LSI (w/ keywords) * Lucene ranking']
    
    line_styles = ['ro-','kx-','b+-','c^-','yv-.','gd-', 'bd-'] 
    
    
    #---------------------------------------------- Reads the configuration file
    
    mdl_cfg = read_config(config_file)
    
    
    #------------ Checks whether the keywords are there in the corpus dictionary
    
    dictionary = load_dictionary(mdl_cfg['CORPUS']['dict_file'])
    valid_tokens  = 0 
    for token in tm_query.split():
        if token.strip() not in dictionary.values():
            print token, "is not in the corpus vocabulary. Hence, this word will be ignored from the topic search."
        else: 
            valid_tokens  += 1
            
    if valid_tokens  == 0:
        print 'None of the tokens exist in the dictionary. Exiting topic search!'
        exit()
        
        
    #------------------------------------------------------------- Lucene search

    print 'Lucene ranking'
    lu_docs = search_li(lucene_query, limit, mdl_cfg)
    lu_docs_dict, lu_docs_list = lu_append_nonresp(lu_docs, test_directory)
    lu_res = convert_to_roc_format(lu_docs_list, positive_dir)
    print 
    
    
    #---------------------------------------------------------------- LDA search
    
    # Loads the LDA model 
    lda_dictionary, lda_mdl, _, _ = load_tm(mdl_cfg)
    
    # To display the LDA model topics based on the 
    # increasing order of entropy   
    # print_lda_topics_on_entropy(lda_mdl, file_name='%s-topic-words.csv' % file_prefix, topn=50) 
    
    # Gets the dominant topics from the LDA model 
    dominant_topics = get_dominant_query_topics(tm_query, lda_dictionary, lda_mdl, TOP_K_TOPICS)
    dominant_topics_idx = [idx for (idx, _) in dominant_topics] # get the topic indices 
    
    
    print 'LDA (w/ keywords) ranking'
    lda_docs = search_tm(tm_query, limit, mdl_cfg)
    lda_res = convert_to_roc_format(lda_docs, positive_dir)
    
    # plot_doc_class_predictions(lda_res, '%s-Keyword-LDA' % file_prefix, img_extension)
    
    
    print 'LDA (w/ keywords) * Lucene ranking'
    lu_tm_docs = fuse_lucene_tm_scores(lu_docs_dict, lda_docs)
    lda_lu_res = convert_to_roc_format(lu_tm_docs, positive_dir)
    
    # plot_doc_class_predictions(lda_lu_res, '%s-Keyword-LDA-Lucene' % file_prefix, img_extension)
    
    
    print 'LDA (w/ query topics) ranking'
    lda_tts_docs = search_tm_topics(dominant_topics_idx, limit, mdl_cfg) 
    lda_tts_res = convert_to_roc_format(lda_tts_docs, positive_dir)
    
    # plot_doc_class_predictions(lda_tts_res, '%s-Topic-LDA' % file_prefix, img_extension)
    
    print 'LDA (w/ query topics) * Lucene Ranking'
    final_docs_tts = fuse_lucene_tm_scores(lu_docs_dict, lda_tts_docs)
    lda_tts_lu_res = convert_to_roc_format(final_docs_tts, positive_dir)
    
    # plot_doc_class_predictions(lda_tts_lu_res, '%s-Topic-LDA-Lucene' % file_prefix, img_extension)
    
    
    
    #---------------------------------------------------------------- LSI search
    
    print 'LSI (w/ keywords) ranking'
    lsi_docs = search_lsi(tm_query, limit, mdl_cfg)
    lsi_res = convert_to_roc_format(lsi_docs, positive_dir)
    
    print 'LSI (w/ keywords) * Lucene ranking'
    lsi_lu_docs = fuse_lucene_tm_scores(lu_docs_dict, lsi_docs)
    lsi_lu_res = convert_to_roc_format(lsi_lu_docs, positive_dir)
    
    
    ## Plot ROC curves  

    results_list = [lu_res, 
                    lda_res, lda_lu_res, 
                    lda_tts_res, lda_tts_lu_res, 
                    lsi_res, lsi_lu_res]
    
    roc_data_list = [ROCData(result, linestyle=line_styles[idx]) 
                     for idx, result in enumerate(results_list)]
    plot_multiple_roc(roc_data_list, title=rocs_img_title, 
                      labels=roc_labels, include_baseline=True, 
                      file_name=rocs_file_name)



def eval_keywordlda_topiclda_lucene(file_prefix, config_file, 
                                    test_directory, tm_query, 
                                    limit = 1000, 
                                    img_extension  = '.eps'):
    
    lucene_query = 'all:(%s)' % tm_query # search in all fields 
    print 'Lucene query:', lucene_query
    print 'TM query:', tm_query
    
    positive_dir = os.path.join(test_directory, "1") # TRUE positive documents 
    TOP_K_TOPICS = 5 # the number topics used for Topic-LDA 
    rocs_file_name = '%s-ROCs' % file_prefix + img_extension
    rocs_img_title = '' # %s: ROC curves' % file_prefix 
    roc_labels = ['Lucene ranking', 
                  'Keyword-LDA ranking' , 
                  'Topic-LDA ranking']
    line_styles = ['ro-','kx-','b+-'] 
    
    #---------------------------------------------- Reads the configuration file
    
    mdl_cfg = read_config(config_file)
    
    # Loads the LDA model 
    lda_dictionary, lda_mdl, _, _ = load_tm(mdl_cfg)
    
    
    #------------ Checks whether the keywords are there in the corpus dictionary

    valid_tokens  = 0 
    for token in tm_query.split():
        if token.strip() not in lda_dictionary.values():
            print token, "is not in the corpus vocabulary. Hence, this word will be ignored from the topic search."
        else: 
            valid_tokens  += 1
            
    if valid_tokens  == 0:
        print 'None of the tokens exist in the dictionary. Exiting topic search!'
        exit()
        
        
    #------------------------------------------------------------- Lucene search

    print 'Lucene ranking'
    lu_docs = search_li(lucene_query, limit, mdl_cfg)
    _, lu_docs_list = lu_append_nonresp(lu_docs, test_directory)
    lu_res = convert_to_roc_format(lu_docs_list, positive_dir)
    
    
    #---------------------------------------------------------------- LDA search
    
    # To display the LDA model topics based on the 
    # increasing order of entropy   
    # print_lda_topics_on_entropy(lda_mdl, file_name='%s-topic-words.csv' % file_prefix, topn=50) 
    
    # Gets the dominant topics from the LDA model 
    dominant_topics = get_dominant_query_topics(tm_query, lda_dictionary, lda_mdl, TOP_K_TOPICS)
    dominant_topics_idx = [idx for (idx, _) in dominant_topics] # get the topic indices 
    
    
    print 'LDA (w/ keywords) ranking'
    lda_docs = search_tm(tm_query, limit, mdl_cfg)
    lda_res = convert_to_roc_format(lda_docs, positive_dir)
    
    
    print 'LDA (w/ query topics) ranking'
    lda_tts_docs = search_tm_topics(dominant_topics_idx, limit, mdl_cfg) 
    lda_tts_res = convert_to_roc_format(lda_tts_docs, positive_dir)
    
    
    ## Plot ROC curves  

    results_list = [lu_res, 
                    lda_res, 
                    lda_tts_res]

    roc_data_list = [ROCData(result, linestyle=line_styles[idx]) 
                     for idx, result in enumerate(results_list)]
    
    plot_multiple_roc(roc_data_list, title=rocs_img_title, 
                      labels=roc_labels, include_baseline=True, 
                      file_name=rocs_file_name)
     
     

def eval_ranking_varying_topics(query_id, dir_path, 
                                 keywords, 
                                 limit = 1000, 
                                 img_extension  = '.eps'):
    
    tm_query = ' '.join( lemmatize_tokens( regex_tokenizer(keywords)  ) ) # Lemmatization 
    lucene_query = 'all:(%s)' % tm_query # search in all fields 
    print 'Lucene query:', lucene_query
    print 'TM query:', tm_query

    test_directory = "%s%d" % (dir_path, query_id)
    positive_dir = os.path.join(test_directory, "1") # TRUE positive documents 

    TOP_K_TOPICS = 5 # the number topics used for Topic-LDA 
    topiclda_rocs_file_name = '%d-LT-Topic-LDA-VaryingTopics-ROCs' % query_id + img_extension
    topiclda_rocs_img_title = 'Q%d Topic-LDA with Varying Number of Topics' % query_id  
    keywordlda_rocs_file_name = '%d-LT-Keyword-LDA-VaryingTopics-ROCs' % query_id + img_extension
    keywordlda_rocs_img_title = 'Q%d Keyword-LDA with Varying Number of Topics' % query_id  
    topics = [5, 10, 15, 20, 30, 40, 50, 60, 70, 80]
    roc_labels = []
    roc_topiclda_list = []
    roc_keywordlda_list = []

    for idx, num_topics in enumerate(topics): 

        #---------------------------------------------- Reads the configuration file
        
        config_file = "%sQ%d-LT-%dT.cfg" % (dir_path, query_id, num_topics)  # configuration file, created using the SMARTeR GUI 
        mdl_cfg = read_config(config_file)
        
        # Loads the LDA model 
        lda_dictionary, lda_mdl, _, _ = load_tm(mdl_cfg)
        
        
        #------------ Checks whether the keywords are there in the corpus dictionary
    
        valid_tokens  = 0 
        for token in tm_query.split():
            if token.strip() not in lda_dictionary.values():
                print token, "is not in the corpus vocabulary. Hence, this word will be ignored from the topic search."
            else: 
                valid_tokens  += 1
                
        if valid_tokens  == 0:
            print 'None of the tokens exist in the dictionary. Exiting topic search!'
            exit()
            
            
        #------------------------------------------------------------- Lucene search
    
        if idx == 0: # the first Lucene ranking is added as a reference 
            print 'Lucene ranking'
            lu_docs = search_li(lucene_query, limit, mdl_cfg)
            _, lu_docs_list = lu_append_nonresp(lu_docs, test_directory)
            lu_res = convert_to_roc_format(lu_docs_list, positive_dir)
            roc_topiclda_list.append(ROCData(lu_res))
            roc_keywordlda_list.append(ROCData(lu_res))
            roc_labels.append('Lucene')
        
        #---------------------------------------------------------------- LDA search
        
        # Gets the dominant topics from the LDA model 
        dominant_topics = get_dominant_query_topics(tm_query, lda_dictionary, lda_mdl, TOP_K_TOPICS)
        dominant_topics_idx = [idx for (idx, _) in dominant_topics] # get the topic indices 
        
        
        print 'LDA (w/ keywords) ranking'
        lda_docs = search_tm(tm_query, limit, mdl_cfg)
        lda_res = convert_to_roc_format(lda_docs, positive_dir)
        
        
        print 'LDA (w/ query topics) ranking'
        lda_tts_docs = search_tm_topics(dominant_topics_idx, limit, mdl_cfg) 
        lda_tts_res = convert_to_roc_format(lda_tts_docs, positive_dir)
    
        
        roc_topiclda_list.append(ROCData(lda_tts_res))
        roc_keywordlda_list.append(ROCData(lda_res))
        roc_labels.append('%d topics' % num_topics)
        
    
    ## Plot ROC curves  
    
    plot_multiple_roc(roc_topiclda_list, title=topiclda_rocs_img_title, 
                      labels=roc_labels, include_baseline=True, 
                      file_name=topiclda_rocs_file_name)
     
    plot_multiple_roc(roc_keywordlda_list, title=keywordlda_rocs_img_title, 
                      labels=roc_labels, include_baseline=True, 
                      file_name=keywordlda_rocs_file_name)
         
#===============================================================================
# '''
# TEST SCRIPTS 
# 
# '''
#===============================================================================
if __name__ == '__main__':
    
    # ************************************************************************************
    # ****** DO ALL HARD-CODINGS HERE ****************************************************
    # ************************************************************************************
    
    
    
    ## ***** BEGIN change the following each query *********
    
    ## ***** BEGIN change the following each query *********
    
#    query_id = 201
#    file_prefix = '%d' % query_id
#    config_file = "project4.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\201"# the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    lucene_query = 'all:(pre-pay swap)'
#    tm_query = 'pre-pay swap'
#    
#

#    query_id = 202
#    file_prefix = '%d-raw' % query_id
#    config_file = "project-202-raw.cfg" # "gui/project3.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\202"# the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    lucene_query = 'all:(FAS transaction swap trust Transferor Transferee)'
#    tm_query = 'FAS transaction swap trust Transferor Transferee'
#
#
#    query_id = 202
#    file_prefix = '%d-LT' % query_id
#    config_file = "F:\\Research\\datasets\\trec2010\\Q202-LT-30T.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\202" # the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    keywords = 'FAS transaction swap trust Transferor Transferee'
#    norm_tokens = ' '.join( lemmatize_tokens( regex_tokenizer(keywords) ) ) # Lemmatization 

#    
#    query_id = 202
#    file_prefix = '%d-LST' % query_id
#    config_file = "F:\\Research\\datasets\\trec2010\\Q202-LST-30T.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\202" # the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    keywords = 'FAS transaction swap trust Transferor Transferee'
#    norm_tokens = ' '.join( stem_tokens( lemmatize_tokens( regex_tokenizer(keywords) ) ) ) # Stemming and Lemmatization 


    
#    query_id = 204
#    config_file = "project-204-raw.cfg" # "gui/project3.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\204"# the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    lucene_query = 'all:(retention compliance preserve discard destroy delete clean eliminate shred schedule period documents file policy e-mail)'
#    tm_query = 'retention compliance preserve discard destroy delete clean eliminate shred schedule period documents file policy e-mail'
    
   
#    # ---------------------------------------------------------------------------------------------------------------  
#    # Evaluates differnent Ranking models using 
#    # RAW (UNT), LEMMATIZED (LT), LEMMATIZED and STEMMED (LST) 
#    # word tokens   
#    
#    query_id = 201
#    file_prefix = '%d-UNT' % query_id
#    config_file = "F:\\Research\\datasets\\trec2010\\Q201-UNT-30T.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\201"# the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    keywords = 'pre-pay swap'
#    norm_tokens = keywords # Unnormalized keywords 
#    eval_keywordlda_topiclda_lucene(file_prefix, config_file, test_directory, 
#                                    norm_tokens, limit = 1000, img_extension = '.eps')
#    query_id = 201
#    file_prefix = '%d-LT' % query_id
#    config_file = "F:\\Research\\datasets\\trec2010\\Q201-LT-30T.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\201" # the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    keywords = 'pre-pay swap'
#    norm_tokens = ' '.join( lemmatize_tokens( regex_tokenizer(keywords) ) ) # Lemmatization 
#    eval_keywordlda_topiclda_lucene(file_prefix, config_file, test_directory, 
#                                    norm_tokens, limit = 1000, img_extension = '.eps')
#    query_id = 201
#    file_prefix = '%d-LST' % query_id
#    config_file = "F:\\Research\\datasets\\trec2010\\Q201-LST-30T.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\201"# the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    keywords = 'pre-pay swap'
#    norm_tokens = ' '.join( stem_tokens( lemmatize_tokens( regex_tokenizer(keywords) ) ) ) # Stemming and Lemmatization 
#    eval_keywordlda_topiclda_lucene(file_prefix, config_file, test_directory, 
#                                    norm_tokens, limit = 1000, img_extension = '.eps')
#    
#    query_id = 207
#    file_prefix = '%d-LT' % query_id
#    config_file = "F:\\Research\\datasets\\trec2010\\Q207-LT-5T.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\207" # the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    keywords = 'football Eric Bass'
#    norm_tokens = ' '.join( lemmatize_tokens( regex_tokenizer(keywords)  ) ) # Lemmatization 
#    eval_keywordlda_topiclda_lucene(file_prefix, config_file, test_directory, 
#                                    norm_tokens, limit = 1000, img_extension = '.eps')
#    
#    query_id = 207
#    file_prefix = '%d-LST' % query_id
#    config_file = "F:\\Research\\datasets\\trec2010\\Q207-LST-5T.cfg" # configuration file, created using the SMARTeR GUI 
#    test_directory = "F:\\Research\\datasets\\trec2010\\207" # the directory where we keep the training set (TRUE negatives and TRUE positives) 
#    keywords = 'football Eric Bass'
#    norm_tokens = ' '.join( stem_tokens( lemmatize_tokens( regex_tokenizer(keywords) ) ) ) # Stemming and Lemmatization
#    eval_keywordlda_topiclda_lucene(file_prefix, config_file, test_directory, 
#                                    norm_tokens, limit = 1000, img_extension = '.eps')
#        
#    # ---------------------------------------------------------------------------------------------------------------  
#    
    # ---------------------------------------------------------------------------------------------------------------  
    # Evaluate Topic-lDA with varying number of topics 
    # and using Lemmatized tokens 
    
    
    query_id = 201
    dir_path = "F:\\Research\\datasets\\trec2010\\"
    keywords = 'pre-pay swap'
    eval_ranking_varying_topics(query_id, dir_path, keywords)
    
    query_id = 207
    dir_path = "F:\\Research\\datasets\\trec2010\\"
    keywords = 'football Eric Bass'
    eval_ranking_varying_topics(query_id, dir_path, keywords)

    # ---------------------------------------------------------------------------------------------------------------  
    

