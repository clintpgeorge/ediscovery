#!/usr/bin/env python
'''
 This script indexes the plain text in all the files in a given folder using Lucene 3.6

@note: to be removed 

'''
import lucene
import os
import logging
from file_utils import find_files_in_folder
from lucene import \
    SimpleFSDirectory, File, \
    Document, Field, StandardAnalyzer, IndexWriter, Version

# Setting up log format.
logger = logging.getLogger('lucene_index')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO,
                    delay=True)

def lucene_index(input_folder,output_folder):
    '''
    Indexes fresh text data using lucene 3.6.
    Doesn't support incremental generation of index as of now.
    Currently crashes on neo by running out of heap space.
    Arguments: Input folder for text files. output folder for index location 
    Returns: void. The index is stored if generated.
    
    
    '''
    
    # Setting up log file
    logging.basicConfig(file=os.path.join(output_folder,"lucene_index.log"))
    logging.info("Input directory for logging: "+input_folder)
    logging.info("Output directory of index: "+output_folder)
    if  not os.path.isdir(output_folder):
        logger.debug("Making output directory for index: "+ output_folder)
        os.makedirs(output_folder)
    
    # Setting up lucene's heap size for index and version of indexer
    lucene.initVM(initialheap='1024m',maxheap='2048m')
    index_folder = SimpleFSDirectory(File(output_folder))
    analyzer = StandardAnalyzer(Version.LUCENE_30)
    writer = IndexWriter(index_folder, analyzer, True, IndexWriter.MaxFieldLength.UNLIMITED)
    
    # Optimization to reduce heap space usage for generation of index. Merges buffer with
    # current index after 15 docs.
    writer.setMergeFactor(15) 
    writer.setRAMBufferSizeMB(32.0)
    
    # Search to find the files to index
    files_to_index = find_files_in_folder(input_folder) 
    for input_file in files_to_index:
        doc = Document()
        content = open(input_file, 'r').read()
        doc.add(Field("text", content, Field.Store.NO, Field.Index.ANALYZED)) # Do not store text.Only index.
        doc.add(Field("path", input_file, Field.Store.YES, Field.Index.NO)) # Store path to assist in retreiving the file
        writer.addDocument(doc) # Index

    logger.info("Indexed lines from " +input_folder+" (%d documents in index)" % (writer.numDocs()))
    logger.info( "About to optimize index of %d documents..." % writer.numDocs())
    writer.optimize() # Compress index
    logger.info("...done optimizing index of %d documents" % writer.numDocs())
    logger.info("Closing index of %d documents..." % writer.numDocs())
    writer.close()
    logger.info("Closed index")
