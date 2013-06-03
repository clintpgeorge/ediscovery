#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This script process any given text query  
and finds similar documents from a learned 
topic model.  

Dependency: 
    Gensim package
        
Created On: May 21, 2013
Created By: Clint P. George 
'''


import logging, gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def load_dictionary(dictionary_file):
    '''This function loads the corpus dictionary 
    
    Returns: 
        a tuple of dictionary
    Arguments:
        dictionary_file - the dictionary file name 

    '''

    return gensim.corpora.Dictionary().load(dictionary_file)


'''
************************ LDA ****************************
'''    

def load_lda_variables(lda_mdl_file, lda_index_file):
    '''This function loads all the LDA model variables
    
    Returns: 
        lda model, and lda index
    Arguments:
        lda_mdl_file - the LDA model file 
        lda_index_file - the LDA index file 
    '''

    lda = gensim.models.ldamodel.LdaModel.load(lda_mdl_file)
    index = gensim.similarities.MatrixSimilarity.load(lda_index_file)

    return (lda, index)


def search_lda_model(query_text, lda_dictionary, lda_mdl, lda_index, lda_file_path_index, limit):
    '''Tokenize the input query and finds topically 
    similar documents (responsive) using the LDA based 
    document search. 
    
    Returns:
        a lists of lists of responsive documents in 
        this format [doc_id, doc_dir_path, doc_name, score] 
    Arguments:
        query_text - the query in text format 
        lda_dictionary - the dictionary object 
        lda_mdl - the LDA model object 
        lda_index - the index object 
        lda_file_path_index - the list of file details 
        limit - the limit on the number of responsive records 
    
    '''

    # process the query 
    
    query_vec = lda_dictionary.doc2bow(query_text.lower().split())
    
    if len(query_vec) == 0: 
        logging.exception('Query words are not in the dictionary. Exiting topic search!')
        return [] 
    else: 
        logging.info('%d query words are in the dictionary.', len(query_vec))
    
    query_td = lda_mdl[query_vec]
    
    # querying based on cosine distance
    
    sims = lda_index[query_td] # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    ## Identifies responsive documents
     
    responsive_docs_idx = sims[0:limit]
    responsive_docs = [] 
    for (doc_id, score) in responsive_docs_idx: 
        doc = list(lda_file_path_index[doc_id]) # i.e., [doc_id, doc_dir_path, doc_name]
        doc.append(score)
        responsive_docs.append(doc)
    
    return responsive_docs
    
    
    
'''
************************ LSA ****************************
'''   


def load_lsi_variables(lsi_mdl_file, lsi_index_file):
    '''This function loads all the lsi model variables
    
    Returns: 
        lsi model, and lsi index
    Arguments:
        lsi_mdl_file - the LSI model file 
        lsi_index_file - the LSI index file 
    '''

    lsi = gensim.models.lsimodel.LsiModel.load(lsi_mdl_file)
    index = gensim.similarities.MatrixSimilarity.load(lsi_index_file)

    return (lsi, index)



def search_lsi_model(query, dictionary, lsi, index, files_info, limit=5):
    '''Tokenize the input query and finds topically 
    similar documents (responsive) using lsi based 
    document search. 
    
    Returns:
        a lists of lists of responsive document details,
        i.e., [doc_id, doc_dir_path, doc_name, score] 
    Arguments:
        query - the query in text format 
        dictionary - the dictionary object 
        lsi - the lsi model object 
        index - the index object 
        files_info - the list of file details 
        limit - the limit on the number of responsive records 
    
    '''

    # process the query 
    
    query_vec = dictionary.doc2bow(query.lower().split())
    if len(query_vec) == 0: 
        logging.exception('Query words are not in the dictionary. Exiting topic search!')
        return [] 
    else: 
        logging.info('%d query words are in the dictionary.', len(query_vec)) 
    
    
    query_td = lsi[query_vec]
    
    # querying based on cosine distance
    
    sims = index[query_td] # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    ## Identifies responsive and non-responsive documents
     
    responsive_docs_idx = sims[0:limit]
    
    responsive_docs = [] 
    for (doc_id, score) in responsive_docs_idx: 
        doc = list(files_info[doc_id]) # i.e., [doc_id, doc_dir_path, doc_name]
        doc.append(score)
        responsive_docs.append(doc)
    
    return responsive_docs




'''
************************ MAIN ****************************
'''   

if __name__ == '__main__':
    pass