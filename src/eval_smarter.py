'''
Created on Nov 21, 2013

@author: Clint
'''
import os 
import numpy as np 
import random 
import pandas as pd
import math 
import heapq

from operator import itemgetter
from scipy.cluster.vq import kmeans, vq, whiten
from collections import Counter, defaultdict
from libsvm.python.svmutil import svm_problem, svm_parameter, svm_train, svm_predict
from libsvm.tools.grid import find_parameters

from utils.utils_file import read_config, load_file_paths_index, nexists
from utils.utils_email import lemmatize_tokens, stem_tokens, regex_tokenizer, whitespace_tokenize 
from tm.process_query import load_lda_variables, load_dictionary, load_lsi_variables, get_dominant_query_topics
from lucenesearch.lucene_index_dir import boolean_search_lucene_index, get_doc_details
from eval_tm_svm import save_tm_svm_data
from PCA import PCA, Center 

SEED = 1983 
np.random.seed(seed=SEED)


class SMARTeRTest: 
    
    def __init__(self, model_cfg_file):
        
        self.NOTREVIEWED_CLASS_ID = -99
        self.NEUTRAL_CLASS_ID = 0
        self.RESPONSIVE_CLASS_ID = 1
        self.UNRESPONSIVE_CLASS_ID = -1
        self.TOP_K_TOPICS = 5 
        
        self._doc_true_class_ids = {}
        
        self.__load_model(model_cfg_file)
        
        # To find high entropy topics 
        self._topic_entropy = [-sum((p * math.log(p)) 
                                    for p in self._lda_theta[:, topic_idx] if p > 0.) 
                                        for topic_idx in range(0, self._lda_num_topics)] 

        print 'Entropy of topics:',
        print sorted(enumerate(self._topic_entropy), key=lambda x: -x[1])
        print
         
         
        # Do PCA on LDA theta matrix 
        self._pc_fraction = .95 # get principal components that account for 90 % of the total variance 
        # X = np.copy(self._lda_theta)
        # Center(X, axis=0, scale=False, verbose=0) # Center data 
        # p = PCA(X, fraction=fraction)
        # p.npc: number of principal components,
        #    e.g. 2 if the top 2 eigenvalues are >= `fraction` of the total.
        #    It's ok to change this; methods use the current value.
        # print 'Number of principle components that account for %.2f of the total variance: %d' % (fraction * 100., p.npc)
        # p.eigen: the eigenvalues of A*A, in decreasing order (p.d**2).
        #    eigen[j] / eigen.sum() is variable j's fraction of the total variance;
        #    look at the first few eigen[] to see how many PCs get to 90 %, 95 % ...
        # print 'The eigenvalues of the covariance matrix:'
        # print p.eigen  
        # print
        
        from numpy import linalg as LA
        cv_matrix = np.cov(self._lda_theta)
        eigen_values, _ = LA.eig(cv_matrix)
        sort_index = np.argsort(eigen_values)[::-1]
        eigen_values = eigen_values[sort_index]
        sum_variance = np.cumsum(eigen_values) # do cumulative sum 
        sum_variance /= sum_variance[-1] # divide the total of all elements 
        self._theta_npc = np.searchsorted( sum_variance, self._pc_fraction, side='right' ) 
        
    def __load_model(self, model_cfg_file):
        '''
        Loads the models specified in the model configuration file  
        
        Arguments: 
            model_cfg_file - the model configuration file  
        
        '''
        
        self._mdl_cfg = read_config(model_cfg_file)
        self._data_dir_path = self._mdl_cfg['DATA']['root_dir']
        
        # Retrieve topic model file names 
        
        dictionary_file = self._mdl_cfg['CORPUS']['dict_file']
        path_index_file = self._mdl_cfg['CORPUS']['path_index_file']
        lda_mdl_file = self._mdl_cfg['LDA']['lda_model_file']
        lda_cos_index_file = self._mdl_cfg['LDA']['lda_cos_index_file']
        lda_num_topics = self._mdl_cfg['LDA']['num_topics']
        lda_theta_file = self._mdl_cfg['LDA']['lda_theta_file']
        lsi_mdl_file = self._mdl_cfg['LSI']['lsi_model_file']
        lsi_cos_index_file = self._mdl_cfg['LSI']['lsi_cos_index_file']
        lsi_theta_file = self._mdl_cfg['LSI']['lsi_theta_file']
        tfidf_file = self._mdl_cfg['TFIDF']['tfidf_file']

        # Loads learned topic models and file details 
        if nexists(dictionary_file) and nexists(path_index_file):
                
            self._corpus_doc_paths = load_file_paths_index(path_index_file)
            self._dictionary = load_dictionary(dictionary_file)
            self._num_corpus_docs = len(self._corpus_doc_paths)
            self._vocabulary_size = len(self._dictionary)    
                
            
            # Loads documents' TRUE classes
            # TODO: hard coding for the TRUTH data. This needs to be removed from the final version 
            if os.path.exists(os.path.join(self._data_dir_path, "1")):
                positive_dir = os.path.normpath(os.path.join(self._data_dir_path, "1")) # TRUE positive documents  
                for doc_id, dirname, _ in self._corpus_doc_paths:
                    if dirname == positive_dir:
                        self._doc_true_class_ids[doc_id] = self.RESPONSIVE_CLASS_ID 
                    else: 
                        self._doc_true_class_ids[doc_id] = self.UNRESPONSIVE_CLASS_ID
            else: 
                for doc_id, _, _ in self._corpus_doc_paths:
                    self._doc_true_class_ids[doc_id] = self.NOTREVIEWED_CLASS_ID
            
            
            # loads LDA model details 
            if nexists(lda_mdl_file) and nexists(lda_cos_index_file): 
                self._lda_mdl, self._lda_index = load_lda_variables(lda_mdl_file, lda_cos_index_file)
                self._lda_num_topics = int(lda_num_topics)
                self._is_tm_index_available = True 
                self._lda_theta = np.loadtxt(lda_theta_file) # loads the LDA theta from the model theta file 
                # print 'LDA: number of documents: ', self._num_corpus_docs, ' number of topics: ', self._lda_num_topics  
                    
            # loads LSI model details 
            if nexists(lsi_mdl_file) and nexists(lsi_cos_index_file):
                self.lsi_mdl, self.lsi_index = load_lsi_variables(lsi_mdl_file, lsi_cos_index_file)
                self._is_tm_index_available = True  
                self._lsi_theta = np.loadtxt(lsi_theta_file) # loads the LSI theta from the model theta file 
                lsi_num_docs, self._lsi_num_topics = self._lsi_theta.shape 
                # print 'LSI: number of documents: ', lsi_num_docs, ' number of topics: ', self._lsi_num_topics   
                
                # Loads the TFIDF file 
                self._doc_tfidf = []
                with open(tfidf_file) as fp:
                    for line in fp:
                        self._doc_tfidf.append(eval(line))
                # print 'TFIDF is loaded.'                    

        # Loads Lucene index files 
        self._lucene_index_dir_path = self._mdl_cfg['LUCENE']['lucene_index_dir']
        self._is_lucene_index_available = nexists(self._lucene_index_dir_path)  
        
        print 

    def __search_tm_topics(self, topics_list, limit):   
        '''
        Performs search on the topic model using relevant  
        topic indices 
        
        Return:
            a list of [doc_id, doc_path, doc_name, doc_score]
        
        '''
        EPS = 1e-24 # a constant 
        unsel_topic_idx = [idx for idx in range(0, self._lda_num_topics) if idx not in topics_list]
        sel = np.log(self._lda_theta[:, topics_list] + EPS)
        unsel = np.log(1.0 - self._lda_theta[:, unsel_topic_idx] + EPS)
        ln_score = sel.sum(axis=1) + unsel.sum(axis=1)  
        sorted_idx = ln_score.argsort(axis=0)[::-1]
        
        # Normalize the topic index search score 
        # TODO: this is an adhoc method right now. May come back later... 
        min_ln_score = min(ln_score)
        n_ln_score = (1.0 - ln_score / min_ln_score)
    
        ts_results = []
        for i in range(0, limit):
            ts_results.append([self._corpus_doc_paths[sorted_idx[i]][0], # document id  
                              os.path.normpath(os.path.join(self._corpus_doc_paths[sorted_idx[i]][1], self._corpus_doc_paths[sorted_idx[i]][2])), # document path   
                              self._corpus_doc_paths[sorted_idx[i]][2], # document name
                              n_ln_score[sorted_idx[i]]]) # similarity score 
            # print lda_file_path_index[sorted_idx[i]], ln_score[sorted_idx[i]], n_ln_score[sorted_idx[i]], score[sorted_idx[i]] 
            
    
        # grabs the files details from the index     
        # ts_results = get_indexed_file_details(ts_results, self.lucene_index_dir) 
        # results = [[row[0], int(row[9]), float(row[10])] for row in ts_results] # Note: we need a float conversion because it's retrieving as string 
        
        return ts_results # [doc_id, doc_path, doc_name, doc_score]
    
    def __seed_docs_random_selection(self, num_seed_docs=100):
        '''
        Selecting seed documents randomly from the initial ranking results
        '''
       
        req_num_seeds = min(num_seed_docs, self._num_corpus_docs)
        indices = range(0, self._num_corpus_docs)
        np.random.shuffle(indices)
        selected_random_indices = indices[0:req_num_seeds]
 
        seed_docs_ids = [self._corpus_doc_paths[random_index][0] for random_index in selected_random_indices]

        return seed_docs_ids
    

    def __seed_docs_Kmeans_selection(self, num_seed_docs=100, num_clusters=5):
        '''
        Selecting seed documents from K-means clusters of LDA 
        document topic proportions (theta_d) 
        '''

        
        # K-means clustering on the LDA theta 
        
        if np.isnan(np.min(self._lda_theta)):
            print "Cannot perform k-means because one of the elements of the document THETA matrix is NAN."
            exit()

        
        whitened = whiten(self._lda_theta + 1e-15)
        codebook, _ = kmeans(whitened, num_clusters)
        doc_labels, _ = vq(whitened, codebook)
        

#        import Pycluster
#        doc_labels, error, nfound = Pycluster.kcluster(self._lda_theta, num_clusters)
#        print error # The within-cluster sum of distances for the optimal clustering solution.
#        print nfound # The number of times the optimal solution was found.

        
        # Gets class elements' document id 
        cluster_docs_dict = defaultdict(list)
        for doc_id, doc_label in enumerate(doc_labels):
            cluster_docs_dict[doc_label] += [doc_id] 
            
        for class_id in cluster_docs_dict.keys():
            np.random.shuffle(cluster_docs_dict[class_id])
            
        cnt = 0
        seed_doc_ids = []
        req_num_seeds = min(num_seed_docs, self._num_corpus_docs)
        
        cluster_counts = Counter(doc_labels).items() # to get cluster counts 
        cluster_counts.sort(key=lambda item:-item[1]) # to get cluster id's in the descending order of counts 
        
        while cnt < req_num_seeds:
            for class_id, _ in cluster_counts:
                if len(cluster_docs_dict[class_id]) > 0:
                    seed_doc_ids.append(cluster_docs_dict[class_id].pop()) 
                    cnt += 1
                if cnt == req_num_seeds: break 
        
        return seed_doc_ids
            
            
    def __seed_docs_Kmeans_proportional_selection(self, num_seed_docs=100, num_clusters=5):
        '''
        Selecting seed documents from K-means clusters of LDA 
        document topic proportions (theta_d) 
        '''
        
        # K-means clustering on the LDA theta 
        
        if np.isnan(np.min(self._lda_theta)):
            print "Cannot perform k-means because one of the elements of the document THETA matrix is NAN."
            exit()
        
        whitened = whiten(self._lda_theta + 1e-15)
        codebook, _ = kmeans(whitened, num_clusters)
        doc_labels, _ = vq(whitened, codebook)
        
        # Gets class elements' document id 
        cluster_docs_dict = defaultdict(list)
        for doc_id, doc_label in enumerate(doc_labels):
            cluster_docs_dict[doc_label] += [doc_id] 
            
        for cluster_id in cluster_docs_dict.keys():
            np.random.shuffle(cluster_docs_dict[cluster_id])
            
        seed_doc_ids = []
        req_num_seeds = min(num_seed_docs, self._num_corpus_docs)
        cluster_counts = Counter(doc_labels).items() # to get cluster counts 
        
        for cluster_id, cluster_count in cluster_counts:
            cluster_prop = float(cluster_count) / float(self._num_corpus_docs) 
            cluster_sample_size = min(math.ceil(cluster_prop * float(req_num_seeds)), cluster_count)
            seed_doc_ids += cluster_docs_dict[cluster_id][0:int(cluster_sample_size)]

        print 
        print 'k-Means proportional sampling, seed count:', len(seed_doc_ids)
        print 
        
        return seed_doc_ids

    



    def _smart_classify(self, lucene_query, topic_query, 
                        SVM_C=32, SVM_g=0.5, 
                        num_seeds=100, 
                        include_ldafeatures_alone=True, 
                        include_lsi_features=False):
        """
        Actions to be done when the "Run Query" button is clicked

        """
        
        def eval_prediction(doc_prediction):
            '''
            doc_prediction: doc_id, predicted_class, prediction_score
            '''
            
            true_positives = 0
            true_negatives = 0
            false_positives = 0
            false_negatives = 0 
            
            for doc in doc_prediction:
                doc_id, predicted_cls, _ = doc
                true_cls = self._doc_true_class_ids[doc_id]
                
                if predicted_cls == self.RESPONSIVE_CLASS_ID: 
                    if predicted_cls == true_cls: true_positives += 1
                    else: false_positives += 1
                elif predicted_cls == self.UNRESPONSIVE_CLASS_ID:
                    if predicted_cls == true_cls: true_negatives += 1
                    else: false_negatives += 1
                    
            accuracy = (true_positives + true_negatives) * 100.0 / (true_positives + true_negatives + false_positives + false_negatives)
            
            if (true_positives + false_positives) == 0: precision = -1
            else: precision = true_positives * 100.0 / (true_positives + false_positives)
            
            if (true_positives + false_negatives) == 0: recall = -1 
            else: recall = true_positives * 100.0 / (true_positives + false_negatives)
            
            return {'TP':true_positives, 'TN':true_negatives, 'FP':false_positives, 'FN':false_negatives, 'Accuracy':accuracy, 'Recall':recall, 'Precision':precision}

        def svm_pred(features, seed_docs, SVM_C, SVM_g):

            seed_docs_theta = [features[doc_id] for doc_id in seed_docs] 
            seed_docs_cls = [self._doc_true_class_ids[doc_id] for doc_id in seed_docs] 
            
            
            # SVM train 

            train_prob  = svm_problem(seed_docs_cls, seed_docs_theta)
            train_param = svm_parameter('-t 2 -c 0 -b 1 -c %f -g %f -q' % (SVM_C, SVM_g))
            seed_docs_svm_mdl = svm_train(train_prob, train_param)
            
            # SVM prediction for all the documents in the results 
            
            svm_labels, _, svm_decision_values = svm_predict([0]*self._num_corpus_docs, features, seed_docs_svm_mdl, '-b 0')
            svm_prediction = [[doc_id, svm_label, svm_decision_values[doc_id][0]] for doc_id, svm_label in enumerate(svm_labels)] # [doc_id, lucene_cls, lucene_score]

            return svm_prediction
        
        
        # Document Lucene and topic modeling-based ranking
        
        # dominant_topics = get_dominant_query_topics(topic_query, self._dictionary, self._lda_mdl, self.TOP_K_TOPICS)
        # dominant_topics_idx = [idx for (idx, _) in dominant_topics] # gets the topic indices
        
        lucene_search_results = boolean_search_lucene_index(self._lucene_index_dir_path, lucene_query, self._num_corpus_docs) # lucene search 
        # lda_search_results = self.__search_tm_topics(dominant_topics_idx, self._num_documents) # returns [doc_id, doc_path, doc_name, doc_score] 
            
        self._lucene_score_dict = dict((int(doc[9]), doc[10]) for doc in lucene_search_results)

            
        self._lucene_prediction = [] # [doc_id, lucene_cls, lucene_score]
        min_lucene_score = min(self._lucene_score_dict.values())
        for doc_details in self._corpus_doc_paths:
            doc_id, _, _ = doc_details
            if doc_id in self._lucene_score_dict:
                self._lucene_prediction.append([doc_id, self.RESPONSIVE_CLASS_ID, self._lucene_score_dict[doc_id]]) 
            else: 
                self._lucene_prediction.append([doc_id, self.UNRESPONSIVE_CLASS_ID, min_lucene_score * 1e-15]) 
            
        


        # Include the Lucene scores as the last element  
        # This improves the accuracy by 7% on TREC2010:Query-201 

        
        corpus_docs_features = [(theta_d + [self._lucene_prediction[doc_id][2]]) for doc_id, theta_d in enumerate((self._lda_theta + 1e-24).tolist())]                
        
        # corpus_docs_features = whiten(corpus_docs_features).tolist()
                
        # Selecting seed documents using k-Means 
        
        kmeans_seed_docs = self.__seed_docs_Kmeans_proportional_selection(num_seeds) 
        kmeans_svm_prediction = svm_pred(corpus_docs_features, kmeans_seed_docs, SVM_C, SVM_g)
        kmeans_svm_results = eval_prediction(kmeans_svm_prediction)


        # Selecting seed documents by random selection 
        
        random_seed_docs = self.__seed_docs_random_selection(num_seeds) 
        random_svm_prediction = svm_pred(corpus_docs_features, random_seed_docs, SVM_C, SVM_g)
        random_svm_results = eval_prediction(random_svm_prediction)

        lucene_results = eval_prediction(self._lucene_prediction)
        
        eval_results = {'SVM(k-Means, LDA+LS)':kmeans_svm_results, 
                        'SVM(random, LDA+LS)':random_svm_results, 
                        'LS':lucene_results}
        
        if include_lsi_features:
            lsi_theta = self._lsi_theta.tolist()
            lda_lsi_lu_features = [(doc_features + lsi_theta[doc_id]) for doc_id, doc_features in enumerate(corpus_docs_features)]  
            random_lda_lsi_lu_svm_pred = svm_pred(lda_lsi_lu_features, random_seed_docs, SVM_C, SVM_g)
            random_lda_lsi_lu_svm_results = eval_prediction(random_lda_lsi_lu_svm_pred)
            eval_results['SVM(k-Means, LDA+LS+LSA)'] = random_lda_lsi_lu_svm_results
        
        '''
        The below code is to include classifiers results based on LDA  
        features alone 
        '''
        if include_ldafeatures_alone:

            lda_theta = self._lda_theta.tolist()
            
            # Selecting seed documents using k-Means 
            
            lda_kmeans_svm_prediction = svm_pred(lda_theta, kmeans_seed_docs, SVM_C, SVM_g)
            lda_kmeans_svm_results = eval_prediction(lda_kmeans_svm_prediction)
    
            # Selecting seed documents by random selection 
            
            lda_random_svm_prediction = svm_pred(lda_theta, random_seed_docs, SVM_C, SVM_g)
            lda_random_svm_results = eval_prediction(lda_random_svm_prediction)
            
            eval_results['SVM(k-Means, LDA)'] = lda_kmeans_svm_results
            eval_results['SVM(random, LDA)'] = lda_random_svm_results


        return eval_results
        
    def _evaluate_classify(self, lucene_query, topic_query, 
                        SVM_C=32, SVM_g=.5, 
                        num_seeds=100, FP_file_name='FP.txt'):
        """
        This function is to evaluate the results of topics 
        modeling-based ranking and Lucene search   

        """
        
        # Opens file for logging 
        fw = open(FP_file_name, 'w')
        fw2 = open(FP_file_name.replace('FP', 'FN'), 'w')
#        svm_data_file = FP_file_name.replace('FP', '-libsvm-data') 
        
        
        
        def eval_prediction(doc_prediction, method='SVM'):
            '''
            doc_prediction: doc_id, predicted_class, prediction_score
            '''
            
            true_positives = 0
            true_negatives = 0
            false_positives = 0
            false_negatives = 0 
            fp = []
            fn = []
            tn = []
            tp = []

            print >>fw, method
            print >>fw, '-------------------------------------------------'
            print >>fw2, method
            print >>fw2, '-------------------------------------------------'
        
            for doc in doc_prediction:
                doc_id, predicted_cls, _ = doc
                true_cls = self._doc_true_class_ids[doc_id]
                # We wanna log the document details 
                doc_details = get_doc_details(doc_id, self._lucene_index_dir_path)
                
                if predicted_cls == self.RESPONSIVE_CLASS_ID: 
                    if predicted_cls == true_cls: 
                        tp.append(doc_details[1])
                        true_positives += 1
                    else: 
                        theta_d = [(topic_id, prop) for topic_id, prop in enumerate(self._lda_theta[doc_id])]
                        dominant_topics = heapq.nlargest(self.TOP_K_TOPICS, dict(theta_d).items(), key=itemgetter(1))
                        dom_topic_entropy = [(topic_id, self._topic_entropy[topic_id]) for topic_id, _ in dominant_topics]
                        print >>fw, 'FP:', false_positives, 'method:', method
                        print >>fw, 'file_path:', doc_details[1]
                        print >>fw, 'email_to:', doc_details[2]
                        print >>fw, 'email_from:', doc_details[3]   
                        print >>fw, 'email_subject:', doc_details[4]   
                        print >>fw, 'email_body:', doc_details[5] 
                        print >>fw, 'lucene_search_score:', self._lucene_prediction[doc_id][2]
#                        print >>fw, 'lda_search_score:', self._lda_score_dict[doc_id]
                        print >>fw, 'lda_dominant_topics:', dominant_topics
                        print >>fw, 'lda_dominant_topics_entropy:', dom_topic_entropy
                        print >>fw, 'doc_num_unique_words:', len(self._doc_tfidf[doc_id])
                        print >>fw
                        
                        fp.append(doc_details[1])
                        false_positives += 1
                elif predicted_cls == self.UNRESPONSIVE_CLASS_ID:
                    if predicted_cls == true_cls: 
                        tn.append(doc_details[1])
                        true_negatives += 1
                    else: 
                        theta_d = [(topic_id, prop) for topic_id, prop in enumerate(self._lda_theta[doc_id])]
                        dominant_topics = heapq.nlargest(self.TOP_K_TOPICS, dict(theta_d).items(), key=itemgetter(1))
                        dom_topic_entropy = [(topic_id, self._topic_entropy[topic_id]) for topic_id, _ in dominant_topics]
                        print >>fw2, 'FN:', false_negatives, 'method:', method
                        print >>fw2, 'file_path:', doc_details[1]
                        print >>fw2, 'email_to:', doc_details[2]
                        print >>fw2, 'email_from:', doc_details[3]   
                        print >>fw2, 'email_subject:', doc_details[4]   
                        print >>fw2, 'email_body:', doc_details[5] 
                        print >>fw2, 'lucene_search_score:', self._lucene_prediction[doc_id][2]
#                        print >>fw2, 'lda_search_score:', self._lda_score_dict[doc_id]
                        print >>fw2, 'lda_dominant_topics:', dominant_topics
                        print >>fw2, 'lda_dominant_topics_entropy:', dom_topic_entropy
                        print >>fw2, 'doc_num_unique_words:', len(self._doc_tfidf[doc_id])
                        print >>fw2
                        
                        fn.append(doc_details[1])
                        false_negatives += 1
                    
            accuracy = (true_positives + true_negatives) * 100.0 / (true_positives + true_negatives + false_positives + false_negatives)
            
            if (true_positives + false_positives) == 0: precision = -1
            else: precision = true_positives * 100.0 / (true_positives + false_positives)
            
            if (true_positives + false_negatives) == 0: recall = -1 
            else: recall = true_positives * 100.0 / (true_positives + false_negatives)
            
            return ({'TP':true_positives, 'TN':true_negatives, 
                    'FP':false_positives, 'FN':false_negatives, 
                    'Accuracy':accuracy, 'Recall':recall, 
                    'Precision':precision}, tp, fp, tn, fn)

        def svm_pred(features, seed_docs, test_docs, SVM_C, SVM_g):

            seed_docs_theta = [features[doc_id] for doc_id in seed_docs] 
            seed_docs_cls = [self._doc_true_class_ids[doc_id] for doc_id in seed_docs] 
            
            test_docs_features = [features[doc_id] for doc_id in test_docs]

#            # Grid search for selecting C and g 
#            
#            save_tm_svm_data(seed_docs_cls, seed_docs_theta, svm_data_file)
#            _, param = find_parameters(svm_data_file, '-log2c -10,20,1 -log2g -1,1,1 -v 5')
#            
#            SVM_C = param['c']
#            SVM_g = param['g']
#            
#            print 'SVM Parameter Search: C = %.3f, g = %.3f' % (SVM_C, SVM_g)
#            print

            
            # SVM train 
            
            train_prob  = svm_problem(seed_docs_cls, seed_docs_theta)
            train_param = svm_parameter('-t 2 -c 0 -b 1 -c %f -g %f -q' % (SVM_C, SVM_g))
            seed_docs_svm_mdl = svm_train(train_prob, train_param)
            
            # SVM prediction for all the documents in the results 
            
            svm_labels, _, svm_decision_values = svm_predict([0]*len(test_docs_features), 
                                                             test_docs_features, 
                                                             seed_docs_svm_mdl, '-b 0 -q')
            
            svm_prediction = [[doc_id, svm_labels[i], svm_decision_values[i][0]] 
                              for i, doc_id in enumerate(test_docs)] # [doc_id, svm_cls, svm_score]

            return svm_prediction
        
        
        # Document Lucene and topic modeling-based ranking
        
#        dominant_topics = get_dominant_query_topics(topic_query, 
#                                                    self._dictionary, 
#                                                    self._lda_mdl, 
#                                                    self.TOP_K_TOPICS)
#        dominant_topics_idx = [idx for (idx, _) in dominant_topics] # gets the topic indices
#        lda_search_results = self.__search_tm_topics(dominant_topics_idx, self._num_corpus_docs) # returns [doc_id, doc_path, doc_name, doc_score] 
#        self._lda_score_dict = dict((int(doc[0]), doc[3]) for doc in lda_search_results)
        
        lucene_search_results = boolean_search_lucene_index(self._lucene_index_dir_path, 
                                                            lucene_query, 
                                                            self._num_corpus_docs) # lucene search 
        self._lucene_score_dict = dict((int(doc[9]), doc[10]) for doc in lucene_search_results)

        self._lucene_prediction = [] # [doc_id, lucene_cls, lucene_score]
        min_lucene_score = min(self._lucene_score_dict.values())
        # max_lucene_score = max(self._lucene_score_dict.values())
        # print 'Lucene: max score = %.5f, min score = %.5f' % (max_lucene_score, min_lucene_score)
        # print 
        for doc_details in self._corpus_doc_paths:
            doc_id, _, _ = doc_details
            if doc_id in self._lucene_score_dict:
                self._lucene_prediction.append([doc_id, self.RESPONSIVE_CLASS_ID, 
                                                self._lucene_score_dict[doc_id]]) 
            else: 
                self._lucene_prediction.append([doc_id, self.UNRESPONSIVE_CLASS_ID, 
                                                min_lucene_score * 1e-24]) 
            
        # Query term Boosting 

        query_vec = self._dictionary.doc2bow(whitespace_tokenize(topic_query)) # converts into the corpus format 
        query_terms_id = [vocab_id for vocab_id, _ in query_vec] # identify keywords' vocabulary ids  
        query_terms_tfidfs = []
        for doc_tfidf in self._doc_tfidf:
            tfidf_dict = dict(doc_tfidf) 
            terms_tfidf = []
            for vocab_id in query_terms_id:
                if vocab_id in tfidf_dict:
                    terms_tfidf.append(tfidf_dict[vocab_id] * 1e+2)
                else: 
                    terms_tfidf.append(.0)
            query_terms_tfidfs.append(terms_tfidf)
                    
        
        # Selecting seed documents using random selection  
        
        random_seed_docs = self.__seed_docs_random_selection(num_seeds) 
        test_docs = [doc_id for doc_id in range(0, self._num_corpus_docs) if doc_id not in random_seed_docs]
        print 'Number of test documents:', len(test_docs)
        print 'Number of seed documents:', len(random_seed_docs)
 
        seed_cls_counts = defaultdict(int)
        for doc_id in random_seed_docs:
            seed_cls_counts[self._doc_true_class_ids[doc_id]] += 1
            
        print "Seed document's class counts:", 
        for (true_class_id, counts) in seed_cls_counts.items():
            print 'class %d - %d; ' % (true_class_id, counts),
        print 
        

        # Building the training set for classification 

#        # Feature selection based on ENTROPY of LDA topics 
#        sorted_topics_entropy = sorted(enumerate(self._topic_entropy), key=lambda x: -x[1]) # DESC
#        top_K_entropy_topics = [topic_id for topic_id, _ in sorted_topics_entropy[0:self.TOP_K_TOPICS]]
#        
#        corpus_docs_features = []
#        for doc_id, theta_d in enumerate((self._lda_theta + 1e-24).tolist()):
#            lda_features = [topic_prob for topic_id, topic_prob in enumerate(theta_d) 
#                            if topic_id in dominant_topics_idx or topic_id not in top_K_entropy_topics]
#            corpus_docs_features.append(lda_features + [self._lucene_prediction[doc_id][2]]) 
#                
#        fs_svm_prediction = svm_pred(corpus_docs_features, random_seed_docs, test_docs, SVM_C, SVM_g)
#        
#
#        print >>fw, 'SVM(random, LDA(FS)+LS)' 
#        print >>fw, '-------------------------------------------------'
#        print >>fw2, 'SVM(random, LDA(FS)+LS)' 
#        print >>fw2, '-------------------------------------------------'
#        fs_svm_results, svm2_fn, svm2_fp = eval_prediction(fs_svm_prediction, method='SVM(random, LDA(FS)+LS)')


        # Features are LDA topics and Lucene search score      
        corpus_docs_features = [(theta_d + [self._lucene_prediction[doc_id][2]] + query_terms_tfidfs[doc_id]) 
                                for doc_id, theta_d in enumerate(self._lda_theta.tolist())]  
#        corpus_docs_features = self._lda_theta.tolist()

        random_svm_prediction = svm_pred(corpus_docs_features, random_seed_docs, test_docs, SVM_C, SVM_g)
        random_svm_results, svm_tp, svm_fp, svm_tn, svm_fn = eval_prediction(random_svm_prediction, 
                                                                             method='SVM(random, LDA+LS+TFIDF)')
        
        
#        # Features are LSA topics and Lucene search score
#        lsi_lu_features = [(doc_lsi_theta + [self._lucene_prediction[doc_id][2]]) 
#                           for doc_id, doc_lsi_theta in enumerate(self._lsi_theta.tolist())]  
#        random_lsi_lu_svm_pred = svm_pred(lsi_lu_features, random_seed_docs, test_docs, SVM_C, SVM_g)
#        random_lsi_lu_svm_results, lsi_tp, lsi_fp, lsi_tn, lsi_fn  = eval_prediction(random_lsi_lu_svm_pred, 
#                                                                             method='SVM(random, LSA+LS)')

        lucene_prediction_on_test = [self._lucene_prediction[doc_id] for doc_id in test_docs]
        lucene_results, lucene_tp, lucene_fp, lucene_tn, lucene_fn = eval_prediction(lucene_prediction_on_test, 
                                                                                     method='LS')

        fw.close()
        fw2.close()

#        print 'Set(SVM(random, LDA(FS)+LS) FPs) - Set(Lucene FPs):'
#        cnt = 0
#        for fn in svm2_fp:
#            if fn not in lucene_fp: 
#                print fn 
#                cnt += 1
#        print 'Total:', cnt 
#        
#        print 'Set(SVM(random, LDA(FS)+LS) FNs) - Set(Lucene FNs):'
#        cnt = 0
#        for fn in svm2_fn:
#            if fn not in lucene_fn: 
#                print fn 
#                cnt += 1
#        print 'Total:', cnt 

#        print 'Compare Topic Search with Lucene Search:'
#        
#        print 'Set(SVM(random, LDA+LS) FPs) - Set(Lucene FPs):'
#        cnt = 0
#        for fp in svm_fp:
#            if fp not in lucene_fp: 
#                print fp 
#                cnt += 1
#        print 'Total:', cnt 
#        print 
#        print 'Set(SVM(random, LDA+LS) FNs) - Set(Lucene FNs):'
#        cnt = 0
#        for fn in svm_fn:
#            if fn not in lucene_fn: 
#                print fn 
#                cnt += 1
#        print 'Total:', cnt 
#        print 
#        
#        print 'Set(SVM(random, LDA+LS) TPs) - Set(Lucene TPs):'
        cnt = 0
        for tp in svm_tp:
            if tp not in lucene_tp: 
                #print tp 
                cnt += 1
#        print 'Total:', cnt 
        print 'Set(SVM(random, LDA+LS) TPs) - Set(Lucene TPs):', cnt
#        print 
#        print 'Set(SVM(random, LDA+LS) TNs) - Set(Lucene TNs):'
        cnt = 0
        for tn in svm_tn:
            if tn not in lucene_tn: 
                #print tn 
                cnt += 1
#        print 'Total:', cnt 
        print 'Set(SVM(random, LDA+LS) TNs) - Set(Lucene TNs):', cnt 
        print 
        
        eval_results = {'SVM(random, LDA+LS+TFIDF)':random_svm_results, 
#                        'SVM(random, LDA(FS)+LS)':fs_svm_results, 
#                        'SVM(random, LSA+LS)':random_lsi_lu_svm_results, 
                        'LS':lucene_results}


        return eval_results
    
    
    


def generate_plots(smarter, keywords, project_name):
    
    norm_tokens = ' '.join( stem_tokens( lemmatize_tokens( regex_tokenizer(keywords) ) ) )
    lucene_query = 'all:(%s)' % norm_tokens # search in all fields 
    
    seed_counts = range(20, smarter._num_corpus_docs, 20) # 
    results = []
    for num_seeds in seed_counts:
        eval_avg = {}
        for i in range(0, 100):
            mdl_results_dict = smarter._smart_classify(lucene_query, 
                                                       norm_tokens, 
                                                       num_seeds=num_seeds, 
                                                       include_ldafeatures_alone=True)
            for mdl, values in mdl_results_dict.items():
                metric_dict = defaultdict(list)
                if mdl in eval_avg: metric_dict = eval_avg[mdl]
                for metric, val in values.items(): 
                    metric_dict[metric] += [val]
                eval_avg[mdl] = metric_dict
        
        # Computes mean and standard deviation of each scores 
        eval_a = dict( (mdl, dict((metric, (np.mean(values), np.std(values))) 
                    for metric, values in values.items())) 
                      for mdl, values in eval_avg.items())
        results.append(eval_a)
    
    print 
    print 'Evaluation Results:'
    print 
    for idx, rs in enumerate(results):
        print 
        print 'Number seeds:', seed_counts[idx]
        print pd.DataFrame(rs)     
        print 
            
    metric_mdl_dict = defaultdict(defaultdict)
    
    for rs in results:
        for mdl, metric_dict in rs.items():
            for metric, values in metric_dict.items():
                if metric in metric_mdl_dict:
                    if mdl in metric_mdl_dict[metric]:
                        metric_mdl_dict[metric][mdl] += [values]
                    else: 
                        metric_mdl_dict[metric][mdl] = [values]
                else: 
                    mmd = defaultdict(list)
                    mmd[mdl] = [values]
                    metric_mdl_dict[metric] = mmd
    

#    for metric, mdl_values in metric_mdl_dict.items():
#        print metric 
#        for mdl, values in mdl_values.items():
#            print mdl, values
        
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    font0 = FontProperties()
    axis_font = font0.copy()
    axis_font.set_family('arial')
    axis_font.set_size(14)
    title_font = font0.copy()
    title_font.set_family('arial')
    title_font.set_size(14)
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'TP'] 
    line_styles = ['ro-', 'kx-', 'c^-', 'gv-', 'bd-', 'y+-'] # for each model 
    
    # To make a single figure with multiple sub plots 
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    axl = [ax1, ax2, ax3, ax4]

    for i, mn in enumerate(metrics):
        y_mins = []
        y_maxs = []  
        for midx, (mdl, values) in enumerate(metric_mdl_dict[mn].items()):
            y = [m for m, s in values]
            y_error = [s for m, s in values]
            axl[i].errorbar(seed_counts, y, yerr=y_error, 
                            fmt=line_styles[midx], label=mdl, 
                            capsize=4)
            
            y_mins += [min(y) - max(y_error) - 5]
            y_maxs += [max(y) + max(y_error) + 5]   
            
        axl[i].set_xlim(0., smarter._num_corpus_docs + 5)
        axl[i].set_ylim(min(y_mins), max(y_maxs))
        axl[i].set_title(mn, fontproperties=title_font)
        axl[i].set_xlabel('Number of Seeds', fontproperties=axis_font)
        axl[i].set_ylabel(mn + ' (mean)', fontproperties=axis_font)
        axl[i].legend(loc='lower right', prop={'size':14, 'family':'arial'})
    
    plt.show()              
          
    # To make individual figures are save them 

    for mn in metrics:
        plt.clf()
        # f, ax = plt.subplots()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        file_name = '%s-seed-eval-%s.eps' % (project_name, mn)

        y_mins = []
        y_maxs = []  
        for midx, (mdl, values) in enumerate(metric_mdl_dict[mn].items()):
            y = [m for m, s in values]
            y_error = [s for m, s in values]
            ax.errorbar(seed_counts, y, yerr=y_error, 
                            fmt=line_styles[midx], label=mdl, 
                            capsize=4)
            
            y_mins += [min(y) - max(y_error) - 5]
            y_maxs += [max(y) + max(y_error) + 5]   
            
        ax.set_xlim(0., smarter._num_corpus_docs + 5)
        ax.set_ylim(min(y_mins), max(y_maxs))
        ax.set_xlabel('Number of Seeds', fontproperties=axis_font)
        ax.set_ylabel(mn + ' (mean)', fontproperties=axis_font)
        ax.legend(loc='lower right', prop={'size':14, 'family':'arial'})
    
        plt.savefig(file_name, dpi=700, bbox_inches='tight', pad_inches=0.1)
        print mn, 'plot is created at', file_name 
        
    plt.close()
    

def plot_classification_performance_on_num_topics(query_id, keywords, num_seeds = 40): 
    
    topic_counts = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    norm_tokens = ' '.join( stem_tokens( lemmatize_tokens( regex_tokenizer(keywords) ) ) )
    lucene_query = 'all:(%s)' % norm_tokens # search in all fields 
    print 
    print 'Lucene query:', lucene_query
    print 'TM query:', norm_tokens
    print '------------------------------------------------------------------------------------------------------'
    print 
    results = []
    for num_topics in topic_counts:
        
        print 'Number of topics for LDA:', num_topics
        
        project_name = "Q%d-%dT" % (query_id, num_topics)
        model_cfg_file = "F:\\Research\\datasets\\trec2010\\%s.cfg" % project_name 
        fp_file_name = '%s-FP-doc-details.txt' % project_name
        
        
        smarter = SMARTeRTest(model_cfg_file)
        mdl_results_dict = smarter._evaluate_classify(lucene_query, 
                                                      norm_tokens, 
                                                      FP_file_name=fp_file_name, 
                                                      num_seeds=num_seeds)
        
        print 'Number of PCs that account for %.2f of the total variance: %d out of %d' % (smarter._pc_fraction * 100., smarter._theta_npc, smarter._lda_num_topics)
        print 'Classification results:'
        print pd.DataFrame(mdl_results_dict)    
        print 
        print '------------------------------------------------------------------------------------------------------'
        print 
        
        results.append(mdl_results_dict)
        
        
    metric_mdl_dict = defaultdict(defaultdict)
    
    for rs in results:
        for mdl, metric_dict in rs.items():
            for metric, values in metric_dict.items():
                if metric in metric_mdl_dict:
                    if mdl in metric_mdl_dict[metric]:
                        metric_mdl_dict[metric][mdl] += [values]
                    else: 
                        metric_mdl_dict[metric][mdl] = [values]
                else: 
                    mmd = defaultdict(list)
                    mmd[mdl] = [values]
                    metric_mdl_dict[metric] = mmd
    

#    for metric, mdl_values in metric_mdl_dict.items():
#        print metric 
#        for mdl, values in mdl_values.items():
#            print mdl, values
        
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    font0 = FontProperties()
    axis_font = font0.copy()
    axis_font.set_family('arial')
    axis_font.set_size(14)
    title_font = font0.copy()
    title_font.set_family('arial')
    title_font.set_size(14)
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'TP'] 
    line_styles = ['ro-', 'kx-', 'c^-', 'gv-', 'bd-', 'y+-'] # for each model 
    
    # To make a single figure with multiple sub plots 
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    axl = [ax1, ax2, ax3, ax4]

    for i, mn in enumerate(metrics):
        y_mins = []
        y_maxs = []  
        for midx, (mdl, values) in enumerate(metric_mdl_dict[mn].items()):
            axl[i].plot(topic_counts, values, line_styles[midx], label=mdl)
            
            y_mins += [min(values) - 5]
            y_maxs += [max(values) + 5]   
            
        axl[i].set_xlim(0., max(topic_counts) + 5)
        axl[i].set_ylim(min(y_mins), max(y_maxs))
        axl[i].set_title(mn, fontproperties=title_font)
        axl[i].set_xlabel('Number of Topics', fontproperties=axis_font)
        axl[i].set_ylabel(mn, fontproperties=axis_font)
        axl[i].legend(loc='lower right', prop={'size':14, 'family':'arial'})
    
    plt.show()              

        


if __name__ == '__main__':
    
#    query_id = 201
#    model_cfg_file = "C:\\Users\\Clint\\SMARTeR\\repository\\prj-201-regex.cfg" 
#    keywords = 'prepay transactions'

#    project_name = 'prj-207-re-20t'
#    num_seeds = 40
#    model_cfg_file = "C:\\Users\\Clint\\SMARTeR\\repository\\%s.cfg" % project_name 
#    keywords = 'football Eric Bass'
#    fp_file_name = '%s-FP-doc-details.txt' % project_name

#    query_id = 202    
#    model_cfg_file = "C:\\Users\\Clint\\SMARTeR\\repository\\prj-202.cfg" 
#    keywords = 'FAS transaction swap trust Transferor Transferee'
#
#    query_id = 204
#    model_cfg_file = "C:\\Users\\Clint\\SMARTeR\\repository\\prj-204.cfg" 
#    keywords = 'retention compliance preserve discard destroy delete clean eliminate shred schedule period documents file policy e-mail'

    query_id = 207 
    keywords = 'football Eric Bass'
    
#    query_id = 201
#    keywords = 'prepay transactions'   

#    query_id = 202     
#    keywords = 'FAS transaction swap trust Transferor Transferee'
    
        
    # Plots classification performance based 
    # on varying number of topics 
    
    plot_classification_performance_on_num_topics(query_id, keywords)
      

#    
#    generate_plots(smarter, keywords)
