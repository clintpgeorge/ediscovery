#!/usr/bin/env python

'''
This script is to create lucene indices for 
all files stored in a directory 
   
Created By: Clint P. George 
Created On: Feb 19, 2013 

'''
import datetime
import os
import logging 
from lucene import IndexWriter, StandardAnalyzer, Document, Field 
from lucene import SimpleFSDirectory, File, initVM, Version
from lucene import IndexSearcher, QueryParser, MultiFieldQueryParser, BooleanClause
from utils.utils_email import parse_plain_text_email 
from utils.utils_file import get_file_paths_index, load_file_paths_index, store_file_paths_index


'''
The analyzer used for both indexing and searching  
'''
initVM()
STD_ANALYZER = StandardAnalyzer(Version.LUCENE_CURRENT) 

class MetadataType:
    '''
    The meta data types (enumerator) class  
    '''
    
    # for basic files 

    FILE_NAME = 'file_name'
    FILE_PATH = 'file_path' 
    FILE_ID = 'file_id' 

    # for email files 
        
    EMAIL_RECEIVER = 'email_to'
    EMAIL_SENDER = 'email_from'
    EMAIL_SUBJECT = 'email_subject'
    EMAIL_BODY = 'email_body' 
    EMAIL_CC = 'email_cc' 
    EMAIL_BCC = 'email_bcc'
    EMAIL_DATE = 'email_date'  
    ALL = 'all'
    
    _types = ['file_name', 'file_path', 
              'email_to', 
              'email_from', 'email_subject', 
              'email_body', 'email_cc',
              'email_bcc', 'email_date']


def index_plain_text_emails(data_folder, path_index_file, store_dir):
    '''
    Indexes all the plain text emails in the input directory 
    and stores the index in the store_dir  
    
    Arguments: 
        data_folder - input directory absolute path 
        path_index_file - file paths index file 
        store_dir - index store directory absolute path 
    Returns: 
        None 

    TODO: 
        1. Need to handle dates 
        2. Need to handle general meta data of files (e.g. last modified date, modified by, owner, etc)
    '''
    
    
    if not os.path.exists(store_dir): 
        os.mkdir(store_dir)
    
    
    if os.path.exists(path_index_file): 
        logging.info('Loading file paths index...')
        file_tuples = load_file_paths_index(path_index_file)
        logging.info('%d files found in the file paths index.' % len(file_tuples))
    else: 
        logging.info('Loading files in the data folder %s...' % data_folder)
        file_tuples = get_file_paths_index(data_folder)
        logging.info('%d email documents found.' % len(file_tuples))
    
        store_file_paths_index(path_index_file, file_tuples)
        logging.info('File paths index is stored into %s' % path_index_file)
    
    logging.info('Lucene indexing..')
        
    store = SimpleFSDirectory(File(store_dir))
    writer = IndexWriter(store, STD_ANALYZER, True, IndexWriter.MaxFieldLength.LIMITED)
    
    print 'Count ', len(file_tuples)
    
    for ft in file_tuples: 
        idx, root, file_name = ft
        file_path = os.path.join(root, file_name)
        logging.info("[%d] file: %s - waiting to add to index.", idx, file_name)
        # parses the emails in plain text format 
        receiver, sender, cc, subject, message_text, bcc, date = parse_plain_text_email(file_path)

        doc = Document()
        doc.add(Field(MetadataType.FILE_ID, str(idx), Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field(MetadataType.FILE_NAME, file_name, Field.Store.YES, Field.Index.NOT_ANALYZED, Field.TermVector.YES))
        doc.add(Field(MetadataType.FILE_PATH, file_path, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field(MetadataType.EMAIL_RECEIVER, receiver, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field(MetadataType.EMAIL_SENDER, sender, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field(MetadataType.EMAIL_CC, cc, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field(MetadataType.EMAIL_SUBJECT, subject, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        #Subodh-Rahul - Added BCC field in indexing.
        doc.add(Field(MetadataType.EMAIL_BCC, bcc, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        #Subodh-Rahul - Added Email-Date field in indexing
        doc.add(Field(MetadataType.EMAIL_DATE, date, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        
        if len(message_text) > 0:
            doc.add(Field(MetadataType.EMAIL_BODY, message_text, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.YES))
        else:
            logging.error("[%d] file: %s - no contents found.", idx, file_name)
            
        # Adds all documents fields as a separate index so that we can search through them 
        all_text = receiver + ' ' + sender + ' ' + cc + ' ' + bcc + ' ' + subject + ' ' + message_text  
        doc.add(Field(MetadataType.ALL, all_text, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.YES))

        writer.addDocument(doc)
        logging.info("[%d] file: %s - added to index.", idx, file_name)


    writer.commit()
    writer.close()

    logging.info('All files are indexed.')

def test_search(index_dir):
    '''
    The test function to test the created index 
    '''
    store = SimpleFSDirectory(File(index_dir))
   
    searcher = IndexSearcher(store, True)
    parser = QueryParser(Version.LUCENE_CURRENT, "keywords", STD_ANALYZER)
    parser.setDefaultOperator(QueryParser.Operator.AND)
    query = parser.parse('email_subject:Training')
    start = datetime.datetime.now()
    scoreDocs = searcher.search(query, 50).scoreDocs
    duration = datetime.datetime.now() - start
    
    print "Found %d document(s) (in %s) that matched query '%s':" %(len(scoreDocs), duration, query)
    
    
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        print scoreDoc.score
        table = dict((field.name(), field.stringValue())
                     for field in doc.getFields())
        print table

def get_indexed_file_details(ts_results, lucene_index_dir):
    '''
    This function gets each files details from the lucene 
    index. 
    
    Arguments: 
        ts_results - topic search results, each item contains 
                     [file id, root, file name, similarity score]
        lucene_index_dir - lucene index directory 
    
    Returns: 
        file details in a list 
    '''
    
    store = SimpleFSDirectory(File(lucene_index_dir))
    searcher = IndexSearcher(store, True)
    
    rows = []
    for rs in ts_results:
        doc = searcher.doc(rs[0])
        table = dict((field.name(), field.stringValue())
                     for field in doc.getFields())
        row = []
        metadata = MetadataType._types
        for field in metadata:
            if table.get(field,'empty') != 'empty' :
                row.append(table.get(field,'empty'))
            else: 
                row.append('')
        row.append(str(table.get(MetadataType.FILE_ID,'empty')))
        row.append(str(rs[3])) # similarity score
        
        rows.append(row)
    
    return rows
    
    
def retrieve_document_details(docid, index_dir):
    '''
    This method will be used to retrieve a single document associated with the docid 
    that is passed to it as parameter. 
    The document will be searched in the directory referred by index_dir.
    
    If you want to access a specific field's value you can access that using the instance 
    of this document class as document.get(<field_name>). Here <field_name> is a string.
    '''
    
    store = SimpleFSDirectory(File(index_dir))
    searcher = IndexSearcher(store, True)
    document = searcher.doc(int(docid))
    return document


def search_lucene_index(index_dir, query_model, limit):
    '''
    This function searches query model (query terms along with their 
    meta data) in the learned lucene index
    
    Arguments: 
        index_dir - the lucene index directory 
        query_model - the query model (contains query terms, meta data, and conjunctions) 
        limit - the number of records to be retrieved 
    Return: 
        rows - the returned document details 
        
    TODO: 
        1. Search in all fields if the user hasn't selected any particular item 
    
    '''
    store = SimpleFSDirectory(File(index_dir))
    searcher = IndexSearcher(store, True)
    parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, query_model[1], STD_ANALYZER)
    query = parser.parse(Version.LUCENE_CURRENT, query_model[0], query_model[1], query_model[2], STD_ANALYZER)
    scoreDocs = searcher.search(query, limit).scoreDocs
    
    print "Found %d document(s) that matched query '%s':" %(len(scoreDocs), query)
    
    rows = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        table = dict((field.name(), field.stringValue())
                     for field in doc.getFields())
        row = []
        metadata = MetadataType._types
        for field in metadata:
            if table.get(field,'empty') != 'empty' :
                row.append(table.get(field,'empty'))
            else: 
                row.append('')
        row.append(str(table.get(MetadataType.FILE_ID,'empty'))) # the unique file id of a file 
        row.append(scoreDoc.score)
        row.append('')
        
        rows.append(row)
    
    return rows

def main():
    print "Hello"
    test_search("C:\\Users\\Sahil\\Output\\Project1\\lucene")

if __name__ == '__main__':
    
    main()