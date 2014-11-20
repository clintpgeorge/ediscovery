'''
Created on Jul 2, 2014

@author: Clint
'''
def compare_topics(topic1, topic2):
    t1 = []
    t2 = []
    for word in topic1:
        t1.append(word.split("(")[0])        
    for word in topic2:
        t2.append(word.split("(")[0])
    t1 = set(t1)
    t2 = set(t2)    
    return len(t1.intersection(t2))

gibbs_topics = []
with open("fgs-top30-topic-words.txt") as fp:
    for line in fp:
        gibbs_topics.append(line.strip().split(",")[1:])
        
        
vb_topics = []
with open("vb-top30-topics-words.txt") as fp:
    for line in fp:
        vb_topics.append(line.strip().split(" ")[3:])
        

import numpy as np 

for i, topic1 in enumerate(gibbs_topics):
    mc = []
    for topic2 in vb_topics:
        mc.append(compare_topics(topic1, topic2))
    sort_index = np.argsort(mc)[::-1] # desc order of coherence scores 

    print "Gibbs", i, topic1
    print "VB", sort_index[0], vb_topics[sort_index[0]]
    print "VB", sort_index[1], vb_topics[sort_index[1]]
    print 
    
    if i > 10: break
    

    
        