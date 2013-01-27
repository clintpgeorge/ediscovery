import logging

import lucene
import os
from lucene import \
    SimpleFSDirectory,File, \
    StandardAnalyzer, IndexSearcher, Version, QueryParser

logger = logging.getLogger('lucene_search')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO,
                    delay=True)
def lucene_search(index_dir, limit, query_text):
    
    
    logging.basicConfig(file=os.path.join(index_dir,"lucene_search.log"))
    logger.info("Initializing search....")
    lucene.initVM()
    logger.info("Reading index from "+index_dir)
    index = SimpleFSDirectory(File(index_dir))
    analyzer = StandardAnalyzer(Version.LUCENE_30)
    searcher = IndexSearcher(index)
    
    logger.info("Parsing query :"+ query_text)
    query = QueryParser(Version.LUCENE_30, "text", analyzer).parse(query_text)
    hits = searcher.search(query, limit)

    logger.info("Found %d document(s) that matched query '%s':" % (hits.totalHits, query))
    hit_paths = []

    for hit in hits.scoreDocs:
        #print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        hit_paths.append(doc.get("path"))
    
    return hit_paths 