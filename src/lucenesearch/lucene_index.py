#!/usr/bin/env python

import lucene
import os
import logging
from file_utils import find_files_in_folder
from lucene import \
    SimpleFSDirectory, File, \
    Document, Field, StandardAnalyzer, IndexWriter, Version

logger = logging.getLogger('lucene_index')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO,
                    delay=True)

def lucene_index(input_folder,output_folder):
    
    
    logging.basicConfig(file=os.path.join(output_folder,"lucene_index.log"))
    logging.info("Input directory for logging: "+input_folder)
    logging.info("Output directory of index: "+output_folder)
    if  not os.path.isdir(output_folder):
        logger.debug("Making output directory for index: "+ output_folder)
        os.makedirs(output_folder)
        
    lucene.initVM(initialheap='1024m',maxheap='2048m')
    index_folder = SimpleFSDirectory(File(output_folder))
    analyzer = StandardAnalyzer(Version.LUCENE_30)
    writer = IndexWriter(index_folder, analyzer, True, IndexWriter.MaxFieldLength.UNLIMITED)
    writer.setMergeFactor(15)
    writer.setRAMBufferSizeMB(32.0)
    
    files_to_index = find_files_in_folder(input_folder) 
    for input_file in files_to_index:
        doc = Document()
        content = open(input_file, 'r').read()
        doc.add(Field("text", content, Field.Store.NO, Field.Index.ANALYZED))
        doc.add(Field("path", input_file, Field.Store.YES, Field.Index.NO))
        writer.addDocument(doc)

    logger.info("Indexed lines from " +input_folder+" (%d documents in index)" % (writer.numDocs()))
    logger.info( "About to optimize index of %d documents..." % writer.numDocs())
    writer.optimize()
    logger.info("...done optimizing index of %d documents" % writer.numDocs())
    logger.info("Closing index of %d documents..." % writer.numDocs())
    writer.close()
    logger.info("Closed index")
