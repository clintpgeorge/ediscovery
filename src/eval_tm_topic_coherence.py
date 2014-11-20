'''This script is used to compute topic coherence score mentioned in 
Optimizing semantic coherence in topic models by Mimno et al. (2011) 

    - http://dl.acm.org/citation.cfm?id=2145462



Created on June 04, 2014

@author: Clint P. George 
'''
import os 
import math 
import numpy as np 
import gensim 

from collections import namedtuple
from scipy.spatial.distance import cityblock, euclidean
from utils.utils_file import read_config, nexists

# def document_frequency(u):
#     if u in document_frequencies:
#         return document_frequencies[u]
#     else: 
#         count = 0
#         for doc in lda_corpus: 
#             if vocab[u] in dict(doc):
#                 count += 1
#         document_frequencies[u] = count 
#         return count
# 
# def co_document_frequency(u, v):
#     key = CDF(u, v)
#     if key in co_document_frequencies:
#         return co_document_frequencies[key]
#     else: 
#         count = 0
#         for doc in lda_corpus: 
#             doc_dict = dict(doc)
#             if vocab[u] in doc_dict and vocab[v] in doc_dict:
#                 count += 1
#         co_document_frequencies[key] = count 
#         return count


def calc_Mimno_topic_coherence(lda_corpus, lda_mdl, vocab, M=20):
    
    CDF = namedtuple("CDF", ["u", "v"])
    co_document_frequencies = {}
    document_frequencies = {}
    
    most_prob_words = lda_mdl.show_topics(topics=-1, topn=M, formatted=False)
    
    for topic_words in most_prob_words:
        for m in range(1, M):
            for l in range(0, m):
                _, u = topic_words[m]
                _, v = topic_words[l]    
                document_frequencies[u] = 0
                document_frequencies[v] = 0
                co_document_frequencies[CDF(u, v)] = 0    
    for doc in lda_corpus: 
        if len(doc) == 0: continue 
        doc_dict = dict(doc)
        for word in document_frequencies.keys():
            if vocab[word] in doc_dict:
                document_frequencies[word] += 1                
        for key in co_document_frequencies.keys():
            if (vocab[key.u] in doc_dict 
                and vocab[key.v] in doc_dict):
                co_document_frequencies[key] += 1
    
    coherence_scores = []
    for topic_words in most_prob_words:
        cs = 0
        for m in range(1, M):
            for l in range(0, m):
                u_prob, u = topic_words[m]
                v_prob, v = topic_words[l]  
                key = CDF(u, v)           
                cs += math.log((float(co_document_frequencies[key]) + 1.0) / 
                               float(document_frequencies[u]))
        coherence_scores.append(cs)
    
    return coherence_scores
                
            
def calc_topic_entropy(lda_mdl):
    
    beta = lda_mdl.expElogbeta
    topic_entropies = [-np.sum(beta[j, :] * np.log(beta[j, :])) 
                       for j in range(0, lda_mdl.num_topics)]
    
    return topic_entropies
        
    
def calc_topic_distance_matrix(lda_mdl):
    
    beta = lda_mdl.expElogbeta    
    tdm = np.zeros((lda_mdl.num_topics, lda_mdl.num_topics))
    for j in range(1, lda_mdl.num_topics):
        for k in range(0, j):
            tdm[j, k] = tdm[k, j] = euclidean(beta[j, :], beta[k, :])
    return tdm  
        
    
    
    

# 
# if __name__ == '__main__':
    
config_file = "E:\\E-Discovery\\edrmv2txt-a-b-index-t50-s\\edrmv2txt-a-b-index-t50-s.cfg"
M = 30 # number of terms used in coherence score 
topic_words_file = "top%d-topics-words.txt" % M
# topic_similarites_file = "topics-sim-M%d.txt" % M 


mdl_cfg = read_config(config_file)

# Loads the vocabulary 
vocab_file = mdl_cfg['CORPUS']['vocab_file']
vocab = dict()
with open(vocab_file) as fp:
    for vocab_id, token in enumerate(fp):
        vocab[token.strip()] = vocab_id 
lda_mdl_file = mdl_cfg['LDA']['lda_model_file']        
if nexists(lda_mdl_file): 
    lda_mdl = gensim.models.ldamodel.LdaModel.load(lda_mdl_file)


# Loads the corpus 
ldac_file = mdl_cfg['CORPUS']['blei_corpus_file']
lda_corpus = gensim.corpora.BleiCorpus(ldac_file)

print 'Computing Mimno score...'

coherence_scores = calc_Mimno_topic_coherence(lda_corpus, lda_mdl, vocab, M)
sort_index = np.argsort(coherence_scores)[::-1] # desc order of coherence scores 

# print 'Computing topic entropy scores'
# topic_entropies = calc_topic_entropy(lda_mdl)

# print 'Computing topic distances'
# tdm = calc_topic_distance_matrix(lda_mdl)
# 
# out_file = os.path.join(mdl_cfg['DATA']['project_dir'], topic_similarites_file)
# with open(out_file, "w") as fw:
#     for i in range(0, lda_mdl.num_topics):
#         for idx in np.argsort(tdm[i, :]): 
#             print >>fw, idx, 
#         print >>fw  


most_prob_words = lda_mdl.show_topics(topics=-1, topn=M, formatted=False)

out_file = os.path.join(mdl_cfg['DATA']['project_dir'], topic_words_file)
with open(out_file, "w") as fw:
    for i in sort_index:
        print >>fw, i, # the topic index 
        print >>fw, coherence_scores[i], 
#         print >>fw, topic_entropies[i],
        for (prob, word) in most_prob_words[i]: 
            print >>fw, "%s(%.4f)" % (word, prob), 
        print >>fw 
        
    
        






