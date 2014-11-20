'''
Created on Jun 2, 2014

@author: Clint
'''
from collections import defaultdict 

file_name = "E:\\E-Discovery\\trec2010results\\qrels.t10legallearn\\qrels.t10legallearn"

# I think -1 is for non-relevant documents and 0 is for relevant documents and 1 is for relevant attachments 

prev_query_id = ""
class_counts = defaultdict(int)
with open(file_name) as fp: 
    for line in fp:
        query_file_name, batch_no, class_id = line.split()
        query_id, file_name = query_file_name.split(":")
        if (prev_query_id == query_id):
            # if int(batch_no.strip()) in [10, 100, 1000]:
            class_counts[class_id] += 1
        else: 
            if len(class_counts) > 0:
                print "query %s: " % prev_query_id, class_counts
                class_counts = defaultdict(int)
        prev_query_id = query_id
    print "query %s: " % prev_query_id, class_counts    
        
        