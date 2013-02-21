#!/usr/bin/env python

'''
This script is to create lucene indices for 
all files stored in a directory 
   
Created By: Clint P. George 
Created On: Feb 19, 2013 

'''

import os
import sys 
from lucene import IndexWriter, StandardAnalyzer, Document, Field, LimitTokenCountAnalyzer
from lucene import SimpleFSDirectory, File, initVM, Version
from lucene import IndexSearcher, QueryParser
from preprocess.utils_email import parse_plain_text_email 
from file_utils import get_file_info


class MetadataType:
    '''
    The meta data types (enumerator) class  
    '''
    
    # for basic files 

    FILE_NAME = 'file_name'
    FILE_PATH = 'file_path' 

    # for email files 
        
    EMAIL_RECEIVER = 'email_to'
    EMAIL_SENDER = 'email_from'
    EMAIL_SUBJECT = 'email_subject'
    EMAIL_BODY = 'email_body' 
    EMAIL_CC = 'email_cc' 
    EMAIL_BCC = 'email_bcc'
    EMAIL_DATE = 'email_date'  
    
    _types = ['file_name', 'file_path', 
              'email_to', 
              'email_from', 'email_subject', 
              'email_body', 'email_cc',
              'email_bcc', 'email_date']


'''
The analyzer used for both indexing and searching  
'''
STD_ANALYZER = StandardAnalyzer(Version.LUCENE_CURRENT) 


def index_plain_text_emails(input_dir, store_dir):
    '''
    Indexes all the plain text emails in the input directory 
    and stores the index in the store_dir  
    
    Arguments: 
        input_dir - input directory absolute path 
        store_dir - index store directory absolute path 
    Returns: 
        None 

    TODO: 
        1. Need to handle dates 
        2. Need to handle general meta data of files (e.g. last modified date, modified by, owner, etc)
    '''
    
    
    if not os.path.exists(store_dir): 
        os.mkdir(store_dir)
    
    initVM()
    store = SimpleFSDirectory(File(store_dir))
    writer = IndexWriter(store, STD_ANALYZER, True, IndexWriter.MaxFieldLength.LIMITED)
    
    file_tuples = get_file_info(input_dir)
    
    # Stores the email paths into a text 
    # file for future reference 
    file_paths = os.path.join(store_dir, 'index.file_paths')
    with open(file_paths, 'w') as fw:
        for idx, ft in enumerate(file_tuples): 
            root, _, file_name = ft
            print >>fw, idx, root, file_name
    
    for idx, ft in enumerate(file_tuples): 
        root, _, file_name = ft

        file_path = os.path.join(root, file_name)
        print "  File: ", file_name
        
        # parses the emails in plain text format 
        receiver, sender, cc, subject, message_text = parse_plain_text_email(file_path)

        doc = Document()
        doc.add(Field(MetadataType.FILE_NAME, file_name, Field.Store.YES, Field.Index.NOT_ANALYZED, Field.TermVector.YES))
        doc.add(Field(MetadataType.FILE_PATH, file_path, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field(MetadataType.EMAIL_RECEIVER, receiver, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field(MetadataType.SENDER, sender, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field(MetadataType.EMAIL_CC, cc, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field(MetadataType.EMAIL_SUBJECT, subject, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        if len(message_text) > 0:
            doc.add(Field(MetadataType.EMAIL_BODY, message_text, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.YES))
        else:
            print "warning: no content in %s" % file_name

        writer.addDocument(doc)


    writer.commit()
    writer.close()



def test_search(index_dir):
    '''
    The test function to test the created index 
    '''

    initVM()
    store = SimpleFSDirectory(File(index_dir))
    
    import datetime
    
    searcher = IndexSearcher(store, True)
    parser = QueryParser(Version.LUCENE_CURRENT, "keywords", STD_ANALYZER)
    parser.setDefaultOperator(QueryParser.Operator.AND)
    query = parser.parse('message_subject:"misc"')
    start = datetime.datetime.now()
    scoreDocs = searcher.search(query, 50).scoreDocs
    duration = datetime.datetime.now() - start
    
    print "Found %d document(s) (in %s) that matched query '%s':" %(len(scoreDocs), duration, query)
    
    
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        table = dict((field.name(), field.stringValue())
                     for field in doc.getFields())
        print table




if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print "Usage: python lucene_index_dir.py <input dir> <store dir>"

    else:
        input_dir = sys.argv[1] # '/home/cgeorge/data/maildir' # 
        store_dir = sys.argv[2] # '/home/cgeorge/data/lucene_index'# 

        index_plain_text_emails(input_dir, store_dir)






