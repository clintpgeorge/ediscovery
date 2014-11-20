'''
Created on Feb 6, 2014

@author: Clint
'''
import os

from tm.process_query import load_lda_variables, load_dictionary,\
    search_lda_model, search_lsi_model, load_lsi_variables, \
    get_dominant_query_topics, get_lda_query_td, search_lda_model2,\
    get_lda_query_td2, get_query_top_topic_idx
from utils.utils_file import read_config, load_file_paths_index, nexists
from PyROC.pyroc import ROCData, plot_multiple_roc
import numpy as np 
from utils.utils_email import lemmatize_tokens, regex_tokenizer, stem_tokens
from whoosh_index_dir import boolean_search_whoosh_index

METRICS_DICT =  {'SENS': 'Recall (Sensitivity)', 'SPEC': 'Specificity', 'ACC': 'Accuracy', 'EFF': 'Efficiency',
    'PPV': 'Precision (Positive Predictive Value)', 'NPV': 'Negative Predictive Value' , 'PHI':  'Phi Coefficient', 
    'F1': 'F1 Score', 'TN': 'True Negatives', 'TP': 'True Positives', 'FN': 'False Negatives', 'FP': 'False Positives' }

METRIC_COLORS = ['r', 'b', 'y', 'g', 'c', 'm', 'k', '#eeefff','#ffee00', '#ff00ee','#ccbbff'] # *** depended on the number of metrics used *** 

TOP_K_TOPICS = 5 # the number topics used for Topic-LDA 
RELEVANT_DIR_NAME = "1"


def search_whoosh_index(query_string, mdl_cfg):
    
    index_dir = mdl_cfg['WHOOSH']['whoosh_index_dir']   

    rows = boolean_search_whoosh_index(index_dir, query_string)
    
    if len(rows) == 0: 
        print 'No documents found.'
        return 

    results = [[row[0], row[10]] for row in rows]
    
    return results


def search_tm(query_text, limit, lda_dictionary, lda_mdl, lda_index, lda_file_path_index):   

    ts_results = search_lda_model(query_text, lda_dictionary, lda_mdl, lda_index, lda_file_path_index, limit)
    ## ts_results are in this format  [doc_id, doc_dir_path, doc_name, score] 
    
    if len(ts_results) == 0: 
        print 'No documents found.'
        return 
    
    # Note: we need a float conversion because 
    # it's retrieving as string
    results = [[row[2], ((float(row[3]) + 1.0) / 2.0)] 
               for row in ts_results]  
    
    return results


def search_tm2(query_td, lda_index, lda_file_path_index, limit):   

    ts_results = search_lda_model2(query_td, lda_index, lda_file_path_index, limit)
    ## ts_results are in this format  [doc_id, doc_dir_path, doc_name, score] 
    
    if len(ts_results) == 0: 
        print 'No documents found.'
        return 
    
    # Note: we need a float conversion because 
    # it's retrieving as string
    results = [[row[2], ((float(row[3]) + 1.0) / 2.0)] 
               for row in ts_results]  
    
    return results

def search_tm_topics(topics_list, limit, lda_file_path_index, lda_theta):   
    '''
    Performs search on the topic model using relevant  
    topic indices 
    '''

    EPS = 1e-8 # the smoothing constant, which is used to avoid the log(0) case  
    num_docs, num_topics = lda_theta.shape
    
    unsel_topic_idx = [idx for idx in range(0, num_topics) 
                       if idx not in topics_list]
    sel = np.log(lda_theta[:, topics_list] + EPS)
    unsel = np.log(1.0 - lda_theta[:, unsel_topic_idx] + EPS)
    ln_score = sel.sum(axis=1) + unsel.sum(axis=1)  
    sorted_idx = ln_score.argsort(axis=0)[::-1]
    
    # Normalize the topic index search score 
    # This is performed under the assumption 
    # that each element in ln_score <= 0.0 
    min_ln_score = min(ln_score)
    n_ln_score = (1.0 - ln_score / min_ln_score) 

    ts_results = []
    for i in range(0, min(limit, num_docs)):
        doc_id, doc_dir_path, doc_name = lda_file_path_index[sorted_idx[i]] # Gets document's details 
        ts_results.append([doc_id, # document id  
                          doc_dir_path, # document directory path   
                          doc_name, # document name
                          n_ln_score[sorted_idx[i]]]) # similarity score 
        # print ts_results[i]
    
    # Note: we need a float conversion because 
    # it's retrieving as string
    results = [[row[2], float(row[3])] 
               for row in ts_results]  

    return results

# 
# def search_lsi(query_text, limit, mdl_cfg):   
# 
#     lsi_dictionary, lsi_mdl, lsi_index, lsi_file_path_index = load_lsi_parameters(mdl_cfg)
#     
#     ts_results = search_lsi_model(query_text, 
#                                   lsi_dictionary, 
#                                   lsi_mdl, lsi_index, 
#                                   lsi_file_path_index, 
#                                   limit)
#     ## ts_results are in this format  [doc_id, doc_dir_path, doc_name, score] 
#     
#     # grabs the files details from the index 
#     index_dir = mdl_cfg['LUCENE']['lucene_index_dir']
#     ts_results = get_indexed_file_details(ts_results, index_dir) 
#     
#     if len(ts_results) == 0: 
#         print 'No documents found.'
#         return 
#         
#     results = [[row[0], ((float(row[10]) + 1.0) / 2.0)] for row in ts_results]
#     
#     return results
#
# def load_lsi_parameters(mdl_cfg):
#     
#     dictionary_file = mdl_cfg['CORPUS']['dict_file']
#     path_index_file = mdl_cfg['CORPUS']['path_index_file']
#     lsi_mdl_file = mdl_cfg['LSI']['lsi_model_file']
#     lsi_cos_index_file = mdl_cfg['LSI']['lsi_cos_index_file']
#     
#     if nexists(dictionary_file) and nexists(path_index_file):       
#         lsi_file_path_index = load_file_paths_index(path_index_file)
#         lsi_dictionary = load_dictionary(dictionary_file)
#         
#     if nexists(lsi_mdl_file) and nexists(lsi_cos_index_file): 
#         lsi_mdl, lsi_index = load_lsi_variables(lsi_mdl_file, lsi_cos_index_file)
#         
#     return lsi_dictionary, lsi_mdl, lsi_index, lsi_file_path_index

def load_lda_parameters(mdl_cfg):
    
    dictionary_file = mdl_cfg['CORPUS']['dict_file']
    path_index_file = mdl_cfg['CORPUS']['path_index_file']
    lda_mdl_file = mdl_cfg['LDA']['lda_model_file']
    lda_cos_index_file = mdl_cfg['LDA']['lda_cos_index_file']
    
    if nexists(dictionary_file) and nexists(path_index_file):       
        lda_file_path_index = load_file_paths_index(path_index_file)
        lda_dictionary = load_dictionary(dictionary_file)
        
    if nexists(lda_mdl_file) and nexists(lda_cos_index_file): 
        lda_mdl, lda_index = load_lda_variables(lda_mdl_file, lda_cos_index_file)
        
    lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
    lda_theta = np.loadtxt(lda_theta_file) # loads the LDA theta from the model theta file 
    num_docs, num_topics = lda_theta.shape
    min_lda_theta = np.min(np.min(lda_theta))
    print 'LDA-theta is loaded: # of documents:', num_docs, \
        '# of topics:', num_topics, 'min(Theta):', min_lda_theta  
    
    lda_beta_file = mdl_cfg['LDA']['lda_beta_file']
    lda_beta = np.loadtxt(lda_beta_file) # loads the LDA theta from the model theta file 
    num_topics, vocab_size = lda_beta.shape
    min_lda_beta = np.min(np.min(lda_beta))
    print 'LDA-beta is loaded: # of topics:', num_topics, \
        '# of terms in the vocabulary:', vocab_size, \
        'min(Bheta):', min_lda_beta
    print     
    
    return lda_dictionary, lda_mdl, lda_index, lda_file_path_index, lda_theta, lda_beta



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


     

def plot_doc_class_predictions(ranking_results, file_name, img_extension='.eps'):
    '''
    Plots the distribution of document ranking scores in a class
    
    Need to improve this function.   
    '''

    import pylab 

    pos_cls = [rank_score for (cls_id, rank_score) in ranking_results if cls_id == 1]   
    neg_cls = [rank_score for (cls_id, rank_score) in ranking_results if cls_id == 0] 
    
    w0 = np.ones_like(pos_cls) 
    # w0[:len(pos_cls)/2] = 1
    w1 = np.ones_like(neg_cls) * 2
    # w1[:len(neg_cls)/2] = 0.5
    
    pylab.figure(12)
    pylab.xlabel('Document ranking scores')
    pylab.ylabel('Number of documents')
    pylab.title('Distribution of Document Ranking Scores (in Relevant and Irrelevant classes)')
    pylab.hist( [pos_cls, neg_cls], 30, weights=[w0, w1], histtype='bar', color=['b', 'r'])
    pylab.savefig(file_name + img_extension, dpi=300, bbox_inches='tight', pad_inches=0.1)
    
    

# def eval_ranking_methods(file_prefix, config_file, 
#                          truth_dir, 
#                          tokens, 
#                          limit = 1000, 
#                          img_extension  = '.eps'):
#     
#     lucene_query = 'all:(%s)' % tokens # search in all fields 
#     print 'Lucene query:', lucene_query
#     print 'TM query:', tokens
#     positive_dir = os.path.join(truth_dir, "1") # TRUE positive documents 
#     TOP_K_TOPICS = 5 # the number topics used for Topic-LDA 
#     rocs_file_name = '%s-ROCs' % file_prefix + img_extension
#     rocs_img_title = '' # %s: ROC curves' % file_prefix 
#     roc_labels = ['Lucene ranking', 
#                   'Keyword-LDA ranking' , 
#                   'Keyword-LDA * Lucene ranking', 
#                   'Topic-LDA ranking' , 
#                   'Topic-LDA * Lucene Ranking',
#                   'Keyword-LSI ranking']
#     
#     line_styles = ['ro-','kx-','b+-','c^-','yv-.','gd-'] 
#     
#     
#     #---------------------------------------------- Reads the configuration file
#     
#     mdl_cfg = read_config(config_file)
#     
#     
#     #------------ Checks whether the keywords are there in the corpus dictionary
#     
#     dictionary = load_dictionary(mdl_cfg['CORPUS']['dict_file'])
#     valid_tokens  = 0 
#     for token in tokens.split():
#         if token.strip() not in dictionary.values():
#             print token, "is not in the corpus vocabulary. Hence, this word will be ignored from the topic search."
#         else: 
#             valid_tokens  += 1
#             
#     if valid_tokens  == 0:
#         print 'None of the tokens exist in the dictionary. Exiting topic search!'
#         exit()
#         
#         
#     #------------------------------------------------------------- Lucene search
# 
#     print 'Lucene ranking'
#     lu_docs = search_li(lucene_query, limit, mdl_cfg)
#     lu_docs_dict, lu_docs_list = lu_append_nonresp(lu_docs, truth_dir)
#     lu_res = convert_to_roc_format(lu_docs_list, positive_dir)
#     print 
#     
#     
#     #---------------------------------------------------------------- LDA search
#     
#     # Loads the LDA model 
#     lda_dictionary, lda_mdl, lda_index, lda_file_path_index, lda_theta, lda_beta = load_lda_parameters(mdl_cfg)
#     
#     # To display the LDA model topics based on the 
#     # increasing order of entropy   
#     # print_lda_topics_on_entropy(lda_mdl, file_name='%s-topic-words.csv' % file_prefix, topn=50) 
#     
#     # Gets the dominant topics from the LDA model 
#     dominant_topics = get_dominant_query_topics(tokens, lda_dictionary, lda_mdl, TOP_K_TOPICS)
#     dominant_topics_idx = [idx for (idx, _) in dominant_topics] # get the topic indices 
#     
#     
#     print 'LDA (w/ keywords) ranking'
#     lda_docs = search_tm(tokens, limit, lda_dictionary, lda_mdl, lda_index, lda_file_path_index)
#     lda_res = convert_to_roc_format(lda_docs, positive_dir)
#     
#     # plot_doc_class_predictions(lda_res, '%s-Keyword-LDA' % file_prefix, img_extension)
#     
#     
#     print 'LDA (w/ keywords) * Lucene ranking'
#     lu_tm_docs = fuse_lucene_tm_scores(lu_docs_dict, lda_docs)
#     lda_lu_res = convert_to_roc_format(lu_tm_docs, positive_dir)
#     
#     # plot_doc_class_predictions(lda_lu_res, '%s-Keyword-LDA-Lucene' % file_prefix, img_extension)
#     
#     
#     print 'LDA (w/ query topics) ranking'
#     lda_tts_docs = search_tm_topics(dominant_topics_idx, limit, lda_file_path_index, lda_theta) 
#     lda_tts_res = convert_to_roc_format(lda_tts_docs, positive_dir)
#     
#     # plot_doc_class_predictions(lda_tts_res, '%s-Topic-LDA' % file_prefix, img_extension)
#     
#     print 'LDA (w/ query topics) * Lucene Ranking'
#     final_docs_tts = fuse_lucene_tm_scores(lu_docs_dict, lda_tts_docs)
#     lda_tts_lu_res = convert_to_roc_format(final_docs_tts, positive_dir)
#     
#     # plot_doc_class_predictions(lda_tts_lu_res, '%s-Topic-LDA-Lucene' % file_prefix, img_extension)
#     
#     
#     
#     #---------------------------------------------------------------- LSI search
#     
#     print 'LSI (w/ keywords) ranking'
#     lsi_docs = search_lsi(tokens, limit, mdl_cfg)
#     lsi_res = convert_to_roc_format(lsi_docs, positive_dir)
# 
#     
#     
#     ## Plot ROC curves  
# 
#     results_list = [lu_res, 
#                     lda_res, lda_lu_res, 
#                     lda_tts_res, lda_tts_lu_res, 
#                     lsi_res]
#     
#     roc_data_list = [ROCData(result, linestyle=line_styles[idx]) 
#                      for idx, result in enumerate(results_list)]
#     plot_multiple_roc(roc_data_list, title=rocs_img_title, 
#                       labels=roc_labels, include_baseline=True, 
#                       file_name=rocs_file_name)



def eval_keywordlda_topiclda_lucene_ranking(file_prefix, config_file, 
                                    truth_dir, tokens, 
                                    limit = 1000, 
                                    img_extension  = '.eps',
                                    output_dir = ''):
    
    lucene_query = 'all:(%s)' % tokens # search in all fields 
    
    print 
    print 'Processing', file_prefix
    print 'Lucene query:', lucene_query
    print 'TM query:', tokens
    
    positive_dir = os.path.join(truth_dir, RELEVANT_DIR_NAME) # TRUE positive documents 
    
    rocs_file_name = os.path.join(output_dir, 
                                  '%s-keywordlda-topiclda-lucene-ranking-ROCs' \
                                   % file_prefix + img_extension)
    rocs_img_title = '' # %s: ROC curves' % file_prefix 
    roc_labels = ['Lucene ranking', 
                  'Keyword-LDA ranking' , 
                  'Topic-LDA ranking',
                  'Topic-LDA-2 ranking',
                  'Keyword-LDA-2 ranking']
    line_styles = ['ro-','kx-','b+-','c^-','yv-.'] 
    
    #---------------------------------------------- Reads the configuration file
    
    mdl_cfg = read_config(config_file)
    
    # Loads the LDA model 
    (lda_dictionary, lda_mdl, lda_index, 
     lda_file_path_index, lda_theta, 
     lda_beta) = load_lda_parameters(mdl_cfg)
    
    
    # Checks whether the keywords are there in the corpus dictionary

    valid_tokens  = 0 
    for token in tokens.split():
        if token.strip() not in lda_dictionary.values():
            print token, "is not in the corpus vocabulary. "
        else: 
            valid_tokens  += 1
            
    if valid_tokens  == 0:
        print 'None of the tokens exist in the dictionary. Exiting search!'
        exit()
#
#    query_vec = lda_dictionary.doc2bow(tokens.split())
#    query_term_theta2 = np.array([lda_beta[:,vocab_id] for (vocab_id, _) in query_vec]).sum(axis=0)
#    query_term_theta2 /= sum(query_term_theta2.tolist())
#    dominant_topics_idx2 = np.argsort(query_term_theta2)[::-1][:TOP_K_TOPICS]
#    
#    query_td2 = [(idx, val) for idx, val in enumerate(query_term_theta2)] 
#    
#    
    # Gets the query topic distribution from the LDA beta  
    print 'Estimated topic dist. from the LDA beta:'
    query_td2 = get_lda_query_td2(tokens, lda_dictionary, lda_beta)
    dominant_topics_idx2 = get_query_top_topic_idx(query_td2, lda_mdl, TOP_K_TOPICS)
    
    # Gets the query topic distribution from the LDA model 
    print 'Estimated topic dist. from the LDA model:'
    query_td = get_lda_query_td(tokens, lda_dictionary, lda_mdl) 
    dominant_topics_idx = get_query_top_topic_idx(query_td, lda_mdl, TOP_K_TOPICS)
    
    #------------------------------------------------------------- Lucene search

    print 'Lucene ranking'
    # lu_docs = search_li(lucene_query, limit, mdl_cfg)
    lu_docs = search_whoosh_index(lucene_query, mdl_cfg)
    _, lu_docs_list = lu_append_nonresp(lu_docs, truth_dir)
    lu_res = convert_to_roc_format(lu_docs_list, positive_dir)
    
    
    #---------------------------------------------------------------- LDA search
    
    # To display the LDA model topics based on the 
    # increasing order of entropy   
    # print_lda_topics_on_entropy(lda_mdl, file_name='%s-topic-words.csv' % file_prefix, topn=50) 
    
#    # Gets the dominant topics from the LDA model 
#    dominant_topics = get_dominant_query_topics(tokens, lda_dictionary, lda_mdl, TOP_K_TOPICS)
#    dominant_topics_idx = [idx for (idx, _) in dominant_topics] # get the topic indices 
    
    print 'LDA (w/ keywords) ranking'
    lda_docs = search_tm2(query_td, lda_index, lda_file_path_index, limit)
    lda_res = convert_to_roc_format(lda_docs, positive_dir)

    print 'LDA (w/ keywords) method-2 ranking'
    lda_docs2 = search_tm2(query_td2, lda_index, lda_file_path_index, limit)
    lda_res2 = convert_to_roc_format(lda_docs2, positive_dir)
        
    
    print 'LDA (w/ query topics) ranking'
    lda_tts_docs = search_tm_topics(dominant_topics_idx, limit, 
                                    lda_file_path_index, lda_theta) 
    lda_tts_res = convert_to_roc_format(lda_tts_docs, positive_dir)
    
    print 'LDA (w/ query topics) method-2 ranking'
    lda_tts_docs2 = search_tm_topics(dominant_topics_idx2, limit, 
                                     lda_file_path_index, lda_theta) 
    lda_tts_res2 = convert_to_roc_format(lda_tts_docs2, positive_dir)
        
    
    ## Plot ROC curves  

    results_list = [lu_res, 
                    lda_res, 
                    lda_tts_res, 
                    lda_tts_res2,
                    lda_res2]

    roc_data_list = [ROCData(result, linestyle=line_styles[idx]) 
                     for idx, result in enumerate(results_list)]
    
    plot_multiple_roc(roc_data_list, title=rocs_img_title, 
                      labels=roc_labels, include_baseline=True, 
                      file_name=rocs_file_name)
     
    
    print 'The ROCs are stored in this path', rocs_file_name
    print 




def eval_ranking_varying_topics(query_id, data_dir, 
                                 keywords, 
                                 limit = 1000, 
                                 img_extension  = '.eps'):
    
    tokens = ' '.join( lemmatize_tokens( regex_tokenizer(keywords) ) ) # Lemmatization 
    lucene_query = 'all:(%s)' % tokens # search in all fields 
    print 'Lucene query:', lucene_query
    print 'TM query:', tokens

    truth_dir = "%s%d" % (data_dir, query_id)
    positive_dir = os.path.join(truth_dir, RELEVANT_DIR_NAME) # TRUE positive documents 

    topiclda_rocs_file_name = '%d-LW-Topic-LDA-VaryingTopics-ROCs' % query_id + img_extension
    topiclda_rocs_img_title = 'Q%d (Topic-LDA): Varying # of LDA Topics and Lemmas' % query_id  
    keywordlda_rocs_file_name = '%d-LW-Keyword-LDA-VaryingTopics-ROCs' % query_id + img_extension
    keywordlda_rocs_img_title = 'Q%d (Keyword-LDA): Varying # of LDA Topics and Lemmas' % query_id  
    topics = [5, 10, 15, 20, 30, 40, 50, 60, 70]
    roc_labels = []
    roc_topiclda_list = []
    roc_keywordlda_list = []

    for idx, num_topics in enumerate(topics): 

        print '------------------------------------------------------------------------------------------'
        #---------------------------------------------- Reads the configuration file
        
        config_file = "%sQ%d-LW-%dT.cfg" % (data_dir, query_id, num_topics)  # configuration file, created using the SMARTeR GUI 
        mdl_cfg = read_config(config_file)
        
        # Loads the LDA model 
        (lda_dictionary, lda_mdl, lda_index, 
         lda_file_path_index, lda_theta, 
         lda_beta) = load_lda_parameters(mdl_cfg)
        
        
        #------------ Checks whether the keywords are there in the corpus dictionary
    
        valid_tokens  = 0 
        for token in tokens.split():
            if token.strip() not in lda_dictionary.values():
                print token, "is not in the corpus vocabulary."
            else: 
                valid_tokens  += 1
                
        if valid_tokens  == 0:
            print 'None of the tokens exist in the dictionary. Exiting topic search!'
            exit()
            
        # Gets the query topic distribution from the LDA beta  
        print 'Estimated topic dist. from the LDA beta:'
        query_td2 = get_lda_query_td2(tokens, lda_dictionary, lda_beta)
        dominant_topics_idx2 = get_query_top_topic_idx(query_td2, lda_mdl, TOP_K_TOPICS)
        
        # Gets the query topic distribution from the LDA model 
        print 'Estimated topic dist. from the LDA model:'
        query_td = get_lda_query_td(tokens, lda_dictionary, lda_mdl) 
        dominant_topics_idx = get_query_top_topic_idx(query_td, lda_mdl, TOP_K_TOPICS)
    
        #------------------------------------------------------------- Lucene search
    
        if idx == 0: # the first Lucene ranking is added as a reference 
            print 'Lucene ranking'
            # lu_docs = search_li(lucene_query, limit, mdl_cfg)
            lu_docs = search_whoosh_index(lucene_query, mdl_cfg)
            _, lu_docs_list = lu_append_nonresp(lu_docs, truth_dir)
            lu_res = convert_to_roc_format(lu_docs_list, positive_dir)
            roc_topiclda_list.append(ROCData(lu_res))
            roc_keywordlda_list.append(ROCData(lu_res))
            roc_labels.append('Lucene')
        
        #---------------------------------------------------------------- LDA search
        
#        # Gets the dominant topics from the LDA model 
#        dominant_topics = get_dominant_query_topics(tokens, lda_dictionary, lda_mdl, TOP_K_TOPICS)
#        dominant_topics_idx = [idx for (idx, _) in dominant_topics] # get the topic indices 
        
        
        print 'LDA (w/ keywords) ranking'
        lda_docs = search_tm2(query_td, lda_index, lda_file_path_index, limit)
        lda_res = convert_to_roc_format(lda_docs, positive_dir)
    
        print 'LDA (w/ keywords) method-2 ranking'
        lda_docs2 = search_tm2(query_td2, lda_index, lda_file_path_index, limit)
        lda_res2 = convert_to_roc_format(lda_docs2, positive_dir)
            
        
        print 'LDA (w/ query topics) ranking'
        lda_tts_docs = search_tm_topics(dominant_topics_idx, limit, lda_file_path_index, lda_theta) 
        lda_tts_res = convert_to_roc_format(lda_tts_docs, positive_dir)
        
        print 'LDA (w/ query topics) method-2 ranking'
        lda_tts_docs2 = search_tm_topics(dominant_topics_idx2, limit, lda_file_path_index, lda_theta) 
        lda_tts_res2 = convert_to_roc_format(lda_tts_docs2, positive_dir)
    
        
        roc_topiclda_list.append(ROCData(lda_tts_res))
        roc_keywordlda_list.append(ROCData(lda_res))
        roc_labels.append('%d topics' % num_topics)

        roc_topiclda_list.append(ROCData(lda_tts_res2))
        roc_keywordlda_list.append(ROCData(lda_res2))
        roc_labels.append('%d topics (method-2)' % num_topics)    
        
        print '------------------------------------------------------------------------------------------'    
    
    ## Plot ROC curves  
    
    plot_multiple_roc(roc_topiclda_list, title=topiclda_rocs_img_title, 
                      labels=roc_labels, include_baseline=True, 
                      file_name=topiclda_rocs_file_name)
     
    plot_multiple_roc(roc_keywordlda_list, title=keywordlda_rocs_img_title, 
                      labels=roc_labels, include_baseline=True, 
                      file_name=keywordlda_rocs_file_name)
         

def gen_ranking_rocs(data_dir, output_dir, query_id, num_topics, keywords):
    
    # the directory which contains the training set 
    # (TRUE negatives and TRUE positives)
    truth_dir = "%s\\%d" % (data_dir, query_id)  
    
    # Using unormalized keywords  
    project_name = "Q%d-UNW-%dT" % (query_id, num_topics)
    config_file = "%s\\%s.cfg" % (output_dir, project_name) 
    norm_tokens = keywords 
    try: 
        eval_keywordlda_topiclda_lucene_ranking(project_name, 
                                                config_file, 
                                                truth_dir, 
                                                norm_tokens, 
                                                output_dir=output_dir)
    except:
        print 'Execption in processing', project_name
    
    # Using lemmatized keywords  
    project_name = "Q%d-LW-%dT" % (query_id, num_topics)
    config_file = "%s\\%s.cfg" % (output_dir, project_name)
    norm_tokens = ' '.join( lemmatize_tokens( regex_tokenizer(keywords) ) ) 
    try: 
        eval_keywordlda_topiclda_lucene_ranking(project_name, 
                                                config_file, 
                                                truth_dir, 
                                                norm_tokens, 
                                                output_dir=output_dir)
    except:
        print 'Execption in processing', project_name
 
         
    # Using Stemming and Lemmatization
    project_name = "Q%d-LSW-%dT" % (query_id, num_topics)
    config_file = "%s\\%s.cfg" % (output_dir, project_name)  
    norm_tokens = ' '.join( stem_tokens( lemmatize_tokens( regex_tokenizer(keywords) ) ) ) #  
    try: 
        eval_keywordlda_topiclda_lucene_ranking(project_name, 
                                                config_file, 
                                                truth_dir, 
                                                norm_tokens, 
                                                output_dir=output_dir)
    except:
        print 'Execption in processing', project_name

    
    
    



if __name__ == '__main__':

    
    ''' 
    Evaluates different ranking models for documents 
    based on their ability to classify them as relevant 
    and irrelevant. The document and word indexes are 
    created based  RAW (UNW), LEMMATIZED (LW), LEMMATIZED 
    and STEMMED (LSW) words in the corpus.    
    
    We assume the input files are created using 
    index_trec2010_data.py 
    
    This script may work only in Windows due to the path 
    incompatibility issues  
    
    '''
    
    data_dir = "E:\\E-Discovery\\trec2010dataset\\seeds-a"
    output_dir = "E:\\E-Discovery\\trec2010index-a"

    
    # Testing on the query 201 data 
     
    query_id = 201
    num_topics = 50 # it's fixed 
    keywords = 'prepay swap'
    gen_ranking_rocs(data_dir, output_dir, query_id, num_topics, keywords)
 
 
#     # Testing on the query 202 data 
#      
#     query_id = 202
#     num_topics = 30 # it's fixed 
#     keywords = 'FAS transaction swap trust Transferor Transferee'
#     gen_ranking_rocs(data_dir, output_dir, query_id, num_topics, keywords)
#  
#  
#     # Testing on the query 203 data 
#      
#     query_id = 203
#     num_topics = 30 # it's fixed 
#     keywords = 'forecast earnings profit quarter balance sheet'
#     gen_ranking_rocs(data_dir, output_dir, query_id, num_topics, keywords)
#      
#      
#     # Testing on the query 204 data 
#      
#     query_id = 204
#     num_topics = 30 # it's fixed 
#     keywords = 'retention compliance preserve discard destroy delete clean eliminate shred schedule period documents file policy e-mail'
#     gen_ranking_rocs(data_dir, output_dir, query_id, num_topics, keywords)
#      
#      
#     # Testing on the query 205 data 
#      
#     query_id = 205
#     num_topics = 30 # it's fixed 
#     keywords = 'electricity electric loads hydro generator power'
#     gen_ranking_rocs(data_dir, output_dir, query_id, num_topics, keywords)
# 
#     # Testing on the query 206 data 
#     
#     query_id = 206
#     num_topics = 30 # it's fixed 
#     keywords = 'analyst credit rating grade'
#     gen_ranking_rocs(data_dir, output_dir, query_id, num_topics, keywords)
# 
#     
#     # Testing on the query 207 data 
#      
#     query_id = 207
#     num_topics = 30 # it's fixed 
#     keywords = 'football Eric Bass'
#     gen_ranking_rocs(data_dir, output_dir, query_id, num_topics, keywords)
#         
#     # ---------------------------------------------------------------------------------------------------------------  
    
    # ---------------------------------------------------------------------------------------------------------------  
    # Evaluate Topic-lDA with varying number of topics 
    # and using Lemmatized tokens 
    
    
#    query_id = 201
#    data_dir = "F:\\Research\\datasets\\trec2010\\"
#    keywords = 'pre-pay swap transactions transaction prepay'
#    eval_ranking_varying_topics(query_id, data_dir, keywords)
#    
#    query_id = 207
#    data_dir = "F:\\Research\\datasets\\trec2010\\"
#    keywords = 'football Eric Bass'
#    eval_ranking_varying_topics(query_id, data_dir, keywords)
    
    # ---------------------------------------------------------------------------------------------------------------  
    
