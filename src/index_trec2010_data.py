'''
Created on Feb 5, 2014

@author: Clint
'''
import time 
from index_data import index_data 



#########################################################
## Hard coded values. Should be edited/checked before 
## running this script  
#########################################################

data_folder = "E:\\E-Discovery\\trec2010dataset"
output_folder = "E:\\E-Discovery\\trec2010index"
query_ids = [201]
topic_counts = [5] # , 10, 15, 20, 30, 40, 50, 60, 70, 80
num_passes = 200

#########################################################


print "Indexing documents...."

start_time = time.time()
    
for query_id in query_ids:
    
    query_data_folder = "%s\\%d" % (data_folder, query_id)
    print "Indexing ", query_data_folder
    
    for num_topics in topic_counts:
        
        print "Number of topics for LDA:", num_topics             
        
        # With stemmed and lemmatized tokens 
        project_name = "Q%d-LSW-%dT" % (query_id, num_topics)
        index_data(query_data_folder, output_folder, 
                   project_name, output_folder, 
                   num_topics, num_passes, 
                   min_token_freq=2, 
                   lemmatize=True, 
                   stem=True)


        # With lemmatized tokens 
        project_name = "Q%d-LW-%dT" % (query_id, num_topics)
        index_data(query_data_folder, output_folder, 
                   project_name, output_folder, 
                   num_topics, num_passes, 
                   min_token_freq=2, 
                   lemmatize=True, 
                   stem=False)


        # With raw tokens 
        project_name = "Q%d-UNW-%dT" % (query_id, num_topics)
        index_data(query_data_folder, output_folder, 
                   project_name, output_folder, 
                   num_topics, num_passes, 
                   min_token_freq=1, 
                   lemmatize=False, 
                   stem=False)
        
print '\nIndexing time:', time.time() - start_time, 'seconds'        