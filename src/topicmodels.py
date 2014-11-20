'''
Created on May 28, 2014

@author: Clint
'''
import numpy as np
import gensim
CHUNK_SIZE = 10000


def run_tfidf(dictionary_file, ldac_file, tfidf_file):
    
    corpus = gensim.corpora.BleiCorpus(ldac_file)    
    tfidf = gensim.models.TfidfModel(corpus) 
    corpus_tfidf = tfidf[corpus]

    with open(tfidf_file, 'w') as fw:
        for doc_tfidf in corpus_tfidf:
            print >>fw, doc_tfidf  


def run_lda_estimation(dictionary_file, ldac_file, lda_mdl_file, lda_beta_file, 
                       lda_theta_file, lda_index_file, num_topics, num_passes):
    '''The main function that does the LDA estimation 
    process and saves all the model parameters and the 
    index created by the Gensim Similarity class.   
    '''

    # loads the corpus 
    
    corpus = gensim.corpora.BleiCorpus(ldac_file)
    id2word = gensim.corpora.Dictionary().load(dictionary_file)
    
    # runs the LDA inference 
    
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, 
                                          num_topics=num_topics, update_every=1, 
                                          chunksize=CHUNK_SIZE, 
                                          passes=num_passes)
    lda.save(lda_mdl_file)
    
    # saves the LDA beta 
    
    beta = lda.expElogbeta
    np.savetxt(lda_beta_file, beta)
    
    # Saves document topic distributions 
    
    # get topic probability distribution for a document
    doc_topics = lda[corpus] 
    num_docs = len(doc_topics)
    theta_matrix = np.zeros((num_docs, num_topics))
    count = 0
    for doc in doc_topics: 
        doc = dict(doc)
        theta_matrix[count, doc.keys()] = doc.values()
        count += 1 
    np.savetxt(lda_theta_file, theta_matrix)
    
    
    # Saves index 
    
    # Transforms corpus to LDA topic space and index it
    index = gensim.similarities.MatrixSimilarity(lda[corpus]) 
    index.save(lda_index_file)



if __name__ == '__main__':
    pass