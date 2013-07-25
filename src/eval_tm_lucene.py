import re
import os
from lucene import BooleanClause
from lucenesearch.lucene_index_dir import search_lucene_index, get_indexed_file_details

from tm.process_query import load_lda_variables, load_dictionary, search_lda_model, search_lsi_model, load_lsi_variables
from utils.utils_file import read_config, load_file_paths_index, nexists
from PyROC.pyroc import random_mixture_model, ROCData

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

def prepare_roc_format(docs, positive_dir):
    results = []
    for doc in docs:
        if os.path.exists(os.path.join(positive_dir, doc[0])):
            tuple_list = (1, doc[1])
        else:
            tuple_list = (0, doc[1])
        results.append(tuple_list)
    return results
     


     
#===============================================================================
# '''
# TEST SCRIPTS 
# 
# '''
#===============================================================================

# Initialize variables here 

config_file = "gui/project201.cfg" # configuration file, created using the SMARTeR GUI 
#201
query = "all:pre-pay:May;all:swap:May"
#202
#"all:FAS:May;all:transaction:May;all:swap:May;all:trust:May;all:Transferor:May;all:Transferee:May"
#203
#query = "all:forecast:May;all:earnings:May;all:profit:May;all:quarter:May;all:balance sheet:May"
#204
#query = "all:retention:May;all:compliance:May;all:preserve:May;all:discard:May;all:destroy:May;all:delete:May;all:clean:May;all:eliminate:May;all:shred:May;all:schedule:May;all:period:May;all:documents:May;all:file:May;all:policy:May;all:e-mail:May"
#205
#query = "all:electricity:May;all:electric:May;all:loads:May;all:hydro:May;all:generator:May;all:power:May"
#206 
#query = "all:analyst:May;all:credit:May;all:rating:May;all:grade:May"
#207     
#query = "all:football:May;all:Eric Bass:May" 
test_directory = "F:\\topicModelingDataSet\\201" # the directory where we keep the training set (TRUE negatives and TRUE positives) 
positive_dir = os.path.join(test_directory, "1") # TRUE positive documents 
negative_dir = os.path.join(test_directory, "0") # TRUE negative documents 
score_threshold = 0.51
limit = 1000
file_name = os.path.join(positive_dir, '3.268398.LL1NPOBL5XGYBSSMNJVQCF4TWXJQZ03WB.txt') 




#===============================================================================
# Reads the configuration file and parses the user query  
#===============================================================================

mdl_cfg = read_config(config_file)
query_words, fields, clauses = parse_query(query)

print query_words, fields


#===============================================================================
# Here, we perform Lucene search based on a given query. 
# We also classify and evaluate the retrieved documents  
#===============================================================================

print "\nLucene Search:\n"

docs = search_li([query_words, fields, clauses], limit, mdl_cfg)
docs = normalize_lucene_score(docs)
#responsive_docs, unresponsive_docs = classify_docs(docs, score_threshold)
#true_positives, true_negatives, false_positives, false_negatives, exceptions = eval_results(positive_dir, negative_dir, responsive_docs, unresponsive_docs)
#enhanced_evaluation(positive_dir, negative_dir, true_positives, false_positives)
roc_result = prepare_roc_format(docs,positive_dir)

#Example instance labels (first index) with the decision function , score (second index)
#-- positive class should be +1 and negative 0.
roc = ROCData(roc_result)  #Create the ROC Object
roc.auc() #get the area under the curve
roc.plot(title='ROC Curve') #Create a plot of the ROC curve
roc.confusion_matrix(score_threshold, True)
print roc.evaluateMetrics(roc.confusion_matrix(score_threshold, True))

#===============================================================================
# Here, we perform topic search based on a given query. 
# We also classify and evaluate the retrieved documents  
#===============================================================================

    
print "\nTopic Search:\n"

docs = search_tm(' '.join(query_words), limit, mdl_cfg)
#responsive_docs, unresponsive_docs = classify_docs(docs, score_threshold)
#eval_results(positive_dir, negative_dir, responsive_docs, unresponsive_docs)
roc_result = prepare_roc_format(docs,positive_dir)    
#Example instance labels (first index) with the decision function , score (second index)
#-- positive class should be +1 and negative 0.
roc = ROCData(roc_result)  #Create the ROC Object
roc.auc() #get the area under the curve
roc.plot(title='ROC Curve') #Create a plot of the ROC curve
roc.confusion_matrix(score_threshold, True)
print roc.evaluateMetrics(roc.confusion_matrix(score_threshold, True))
    
print "\nLSI Search:\n"

docs = search_lsi(' '.join(query_words), limit, mdl_cfg)
#responsive_docs, unresponsive_docs = classify_docs(docs, score_threshold)
#eval_results(positive_dir, negative_dir, responsive_docs, unresponsive_docs)
roc_result = prepare_roc_format(docs,positive_dir)
#Example instance labels (first index) with the decision function , score (second index)
#-- positive class should be +1 and negative 0.
roc = ROCData(roc_result)  #Create the ROC Object
roc.auc() #get the area under the curve
roc.plot(title='ROC Curve') #Create a plot of the ROC curve
roc.confusion_matrix(score_threshold, True)
print roc.evaluateMetrics(roc.confusion_matrix(score_threshold, True))
    

#===============================================================================
# Here we consider a relevant document as a query and 
# perform topic search  
#===============================================================================


with open(file_name) as fp:
    doc_text = fp.read()
doc_text = u' '.join(doc_text.split())

print "\nTopic Search (using a document):\n"

docs = search_tm(doc_text, limit, mdl_cfg)
#responsive_docs, unresponsive_docs = classify_docs(docs, score_threshold)
#eval_results(positive_dir, negative_dir, responsive_docs, unresponsive_docs)
roc_result = prepare_roc_format(docs,positive_dir)
    
print "\nLSI Search  (using a document):\n"

docs = search_lsi(' '.join(query_words), limit, mdl_cfg)
#responsive_docs, unresponsive_docs = classify_docs(docs, score_threshold)
#eval_results(positive_dir, negative_dir, responsive_docs, unresponsive_docs)
roc_result = prepare_roc_format(docs,positive_dir)
#Example instance labels (first index) with the decision function , score (second index)
#-- positive class should be +1 and negative 0.
roc = ROCData(roc_result)  #Create the ROC Object
roc.auc() #get the area under the curve
roc.plot(title='ROC Curve') #Create a plot of the ROC curve
roc.confusion_matrix(score_threshold, True)
print roc.evaluateMetrics(roc.confusion_matrix(score_threshold, True))





