#!/usr/bin/env python
'''

This script searches over the lucene index for a search term  

Created On: Jan 28, 2013 
Created By: Abhiram J 
  
@deprecated: June 21, 2013 
'''
import logging
import lucene
import os
from lucene import \
    SimpleFSDirectory,File, \
    StandardAnalyzer, IndexSearcher, Version, QueryParser

# Setting up logger
logger = logging.getLogger('lucene_search')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO,
                    delay=True)
def lucene_search(index_dir, limit, query_text):
    '''
    lucene_search: Search a built index and return upto limit number of responses 
    Arguments: Input index folder, limit value of results returned, query(as string)
    Returns: paths of responsive files as list
    '''
    
    logging.basicConfig(file=os.path.join(index_dir,"lucene_search.log"))
    logger.info("Initializing search....")
    lucene.initVM()
    logger.info("Reading index from "+index_dir)
    index = SimpleFSDirectory(File(index_dir))
    analyzer = StandardAnalyzer(Version.LUCENE_30) #Lucene version used to generate index
    searcher = IndexSearcher(index)
    
    logger.info("Parsing query :"+ query_text)
    query = QueryParser(Version.LUCENE_30, "text", analyzer).parse(query_text)
    hits = searcher.search(query, limit)

    logger.info("Found %d document(s) that matched query '%s':" % (hits.totalHits, query))
    hit_paths = []

    for hit in hits.scoreDocs:
        # The following code also generates score for responsive/found documents and the 
        # content index which matched
        # print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        hit_paths.append(doc.get("path"))
    
    return hit_paths 
