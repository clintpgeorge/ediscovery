#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' 
This script creates Whoosh indices for all files stored in a directory 
   
Created By: Clint P. George 
Created On: Feb 19, 2013 

Updated By: Clint P. George 
Updated On: June 30, 2014 
'''
import datetime
import os
import logging 
from whoosh import index
from whoosh import scoring
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer, StandardAnalyzer
from utils.utils_email import parse_text_emails_and_attachments, stop_words, \
                            pat4, parse_plain_text_email
from utils.utils_file import get_file_paths_index, load_file_paths_index, \
                            store_file_paths_index

class MetadataType:
    '''
    The meta data types (enumerator) class  
    '''
    
    # for basic files 

    FILE_NAME = 'file_name'
    FILE_PATH = 'file_path' 
    FILE_ID = 'file_id' 

    # for emails
        
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


def index_plain_text_emails(data_folder, path_index_file, store_dir, 
                            lemmatize=False, stem=False, nonascii=True):
    '''
    Indexes all the plain text emails in the input directory and stores the 
    index in the store_dir  
    
    Arguments: 
        data_folder - input directory (absolute path)
        path_index_file - file paths index file 
        store_dir - index store directory absolute path 
        lemmatize - lemmatize tokens based on the NLTK WordNet lemmatizer 
        stem - stem tokens 
        nonascii - allow non-ASCII characters  
         
        
    Returns: 
        None 

    '''
    
    if not os.path.exists(store_dir): os.mkdir(store_dir)
    
    if os.path.exists(path_index_file): 
        logging.info('Loading file paths index...')
        file_tuples = load_file_paths_index(path_index_file)
        logging.info('%d files found in the file paths index.' % len(file_tuples))
    else: 
        logging.info('Loading files in the data folder %s...' % data_folder)
        file_tuples = get_file_paths_index(data_folder)
        logging.info('%d email documents found.' % len(file_tuples))    
        store_file_paths_index(path_index_file, file_tuples)
        logging.info('Index file path: %s' % path_index_file)

    schema = Schema(file_id=NUMERIC(int, stored=True), 
                    file_name=ID(stored=True), 
                    file_path=ID(stored=True), 
                    email_reciever=TEXT(stored=True), 
                    email_sender=TEXT(stored=True), 
                    email_cc=TEXT(stored=True), 
                    email_subject=TEXT(stored=True), 
                    email_bcc=TEXT(stored=True),
                    date=ID(stored=True),
                    email_body=TEXT(stored=True),
                    all=TEXT(stored=True))
    ix = create_in(store_dir, schema)
    writer = ix.writer()
    logging.info('Stem = %s, Lemmatize = %s, D = %d, non-ASCII = %s' 
                 % (stem, lemmatize, len(file_tuples), nonascii))
    
    for ft in file_tuples: 
        idx, root, file_name, file_type = ft
        file_path = os.path.join(root, file_name)
        logging.info("[%d] creating index for %s...", idx, file_name)
        
        
        ret = parse_plain_text_email(file_path, lemmatize=lemmatize, stem=stem, 
                                     nonascii=nonascii, file_type=file_type)

        (receiver, sender, cc, subject, body_text, bcc, date, doc_text) = ret
        
        writer.add_document(file_id = idx, 
                            file_name = unicode(file_name), 
                            file_path = unicode(file_path), 
                            email_reciever = unicode(receiver), 
                            email_sender = unicode(sender), 
                            email_cc = unicode(cc),
                            email_subject = unicode(subject), 
                            email_bcc = unicode(bcc), 
                            date = unicode(date), 
                            email_body = unicode(body_text), 
                            all = unicode(doc_text))
 
    writer.commit()
    logging.info('All files are indexed.')



def index_plain_text_emails2(data_folder, path_index_file, store_dir, 
                             stem=False, min_token_len=2, max_token_len=40,
                             procs=1, limitmb=128, multisegment=False, 
                             max_doc_length=-1):
    '''
    Indexes all the plain text emails and attachements in the input directory 
    and stores the index in the store_dir  
    
    Arguments: 
        data_folder - input directory (absolute path)
        path_index_file - file paths index file 
        store_dir - index store directory absolute path 
        stem - stem tokens 
        min_token_len - minimum required length for a token 
        max_token_len - maximum required length for a token 
        procs - number of processors 
        limitmb - memory limit
        multisegment - allow multi-segment write  
        max_doc_length - max document length 
        
    Returns: 
        None 

    '''

    if os.path.exists(path_index_file): 
        logging.info('Loading file paths index...')
        file_tuples = load_file_paths_index(path_index_file)
        logging.info('%d files found in the file paths index.' % len(file_tuples))
    else: 
        logging.info('Loading files in the data folder %s...' % data_folder)
        file_tuples = get_file_paths_index(data_folder)
        logging.info('%d email documents found.' % len(file_tuples))    
        store_file_paths_index(path_index_file, file_tuples)
        logging.info('Index file path: %s' % path_index_file)

    if stem:
        analyzer = StemmingAnalyzer(expression=pat4, stoplist=stop_words, 
                                    minsize=min_token_len, 
                                    maxsize=max_token_len, 
                                    cachesize=-1)
    else: 
        analyzer = StandardAnalyzer(expression=pat4, stoplist=stop_words, 
                                    minsize=min_token_len, 
                                    maxsize=max_token_len)        
    std_ana = StandardAnalyzer(stoplist=None)    
    schema = Schema(file_id=NUMERIC(int, stored=True), 
                    file_name=ID(stored=True), file_path=ID(stored=True), 
                    email_reciever=TEXT(stored=True, analyzer=std_ana), 
                    email_sender=TEXT(stored=True, analyzer=std_ana), 
                    email_cc=TEXT(stored=True, analyzer=std_ana), 
                    email_subject=TEXT(stored=True, analyzer=std_ana), 
                    email_bcc=TEXT(stored=True, analyzer=std_ana),
                    date=ID(stored=True), 
                    email_body=TEXT(stored=True, analyzer=analyzer),
                    all=TEXT(stored=True, analyzer=analyzer))
    if not os.path.exists(store_dir): os.mkdir(store_dir)
    ix = create_in(store_dir, schema)
    
    if procs > 1: 
        writer = ix.writer(procs=procs, limitmb=limitmb, 
                           multisegment=multisegment)
    else: 
        writer = ix.writer(limitmb=limitmb)

    logging.info('Stem = %s, D = %d' % (stem, len(file_tuples)))
    
    truncate_count = 0
    for ft in file_tuples: 
        idx, root, file_name, file_type = ft
        file_path = os.path.join(root, file_name)
        logging.info("[%d] creating index for %s...", idx, file_name)
        
        (receiver, sender, cc, subject, body_text, bcc, date, 
         doc_text) = parse_text_emails_and_attachments(file_path, file_type)
        
        # TODO this needs to be removed 
        et = doc_text.split()
        if max_doc_length > 1 and len(et) > max_doc_length: 
            doc_text = " ".join(et[:max_doc_length])
            truncate_count += 1
        
        writer.add_document(file_id = idx, 
                            file_name = unicode(file_name), 
                            file_path = unicode(file_path), 
                            email_reciever = unicode(receiver), 
                            email_sender = unicode(sender), 
                            email_cc = unicode(cc),
                            email_subject = unicode(subject), 
                            email_bcc = unicode(bcc), 
                            date = unicode(date), 
                            email_body = unicode(body_text), 
                            all = unicode(doc_text))
    writer.commit()

    logging.info('%d documents are truncated.', truncate_count)
    logging.info('All files are indexed.')



def boolean_search_whoosh_index(index_dir, query_text):
    '''
    This function searches a boolean query in the learned Whoosh index 
    
    The query is created using 
    http://lucene.apache.org/core/3_6_0/queryparsersyntax.html
    
    Arguments: 
        index_dir - the Whoosh index directory 
        query_text - the query text
    Return: 
        rows - the returned document details 

    '''
    DEFAULT_FIELD = "all"
    ix = index.open_dir(index_dir)
    qp = QueryParser(DEFAULT_FIELD, schema=ix.schema)
    q = qp.parse(unicode(query_text))

    rows = []
    with ix.searcher(weighting=scoring.TF_IDF()) as s:
        start = datetime.datetime.now()
        results = s.search(q,limit=None)
        duration = datetime.datetime.now() - start
        logging.info("Whoosh Search: Found %d document(s) (in %s) that matched query '%s':", 
                     results.scored_length(), duration, query_text)
        for doc in results:
            row = []
            row.append(doc['file_name'])
            row.append(doc['file_path'])
            row.append(doc['email_reciever'])
            row.append(doc['email_sender'])
            row.append(doc['email_subject'])
            row.append(doc['email_body'])
            row.append(doc['email_cc'])
            row.append(doc['email_bcc'])
            row.append(doc['date'])
            row.append(doc['file_id'])
            row.append(doc.score)
            rows.append(row)

    return rows


