#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

This script is used to parse the enron emails 
in the palin text format and insert them into 
the Postgres db

Created by: Clint P. George
Created On: Jan 12, 2013   

'''

import email
import os 
import psycopg2
import logging
import argparse
import time

from dateutil import parser


# Configures logger 
logger = logging.getLogger('enron_insert_db')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Creates console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_max_employee_id():
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("SELECT coalesce(MAX(eid), 0) FROM employees;")
    record = cursor.fetchone()    
    cursor.close()
    conn.close()
    return int(record[0]) 

def get_max_message_id():
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("SELECT coalesce(MAX(mid), 0) FROM messages;")
    record = cursor.fetchone()    
    cursor.close()
    conn.close()
    return int(record[0]) 


def get_employee_id(email_id):
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("select eid from employees where email_id = %s", (email_id,))
    
    record = cursor.fetchone()        
    cursor.close()
    conn.close()
    
    if record is None: return -1
    else: return record[0]

def insert_employee(eid, xname, email_id):
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (eid, xname, email_id) VALUES (%s, %s, %s)", (eid, xname, email_id))
    conn.commit()
    cursor.close()
    conn.close()

def insert_message(mid, sender, receiver, subject, date, body):
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (mid, sender, receiver, subject, date, body) VALUES (%s, %s, %s, %s, %s, %s)", (mid, sender, receiver, subject, date, body))
    conn.commit()
    cursor.close()
    conn.close()


def insert_message_aux_info(mid, xsender, xreceiver, xfolder, xorigin, xfile):
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages_aux (mid, xfrom, xto, xfolder, xorigin, xfile) VALUES (%s, %s, %s, %s, %s, %s)", (mid, xsender, xreceiver, xfolder, xorigin, xfile))
    conn.commit()
    cursor.close()
    conn.close()


def get_file_info(mail_dir):
    file_tuples = []
    for root, dirs, files in os.walk(mail_dir): # Walk directory tree
        for f in files:
#            _, ext = os.path.splitext(f)
            file_tuples.append((root, dirs, f)) 
    return file_tuples


def insert_files(file_tuples):
    
    count = 0 
    for t in file_tuples:
        root, _, file_name = t
        
        
        
        with open(os.path.join(root, file_name), 'r') as fp: 
            
            logger.info('Processing: #%d. %s' % (count+1, os.path.join(root, file_name)) )
            
            msg = email.message_from_string(fp.read())
            subject = msg['subject']
            receiver = str(msg['to'])
            sender = str(msg['from'])
            dt = parser.parse(msg['date']) 
            cc = str(msg['cc'])
            xfrom = msg['X-From']
            xto = msg['X-To']
            xfolder = msg['X-Folder']
            xorigin = msg['X-Origin']
            xfile = msg['X-FileName']
            
            if not cc == None: cc = cc.strip().replace('\n', '').replace('\t', '')
            if not receiver == None: receiver = receiver.strip().replace('\n', '').replace('\t', '')
            if not sender == None: sender = sender.strip().replace('\n', '').replace('\t', '')
            
            body_text = msg.get_payload()
            lines = body_text.strip().split('\n')
            message_text = ''
            
            for line in lines: 
                line = line.strip()
                if line == '':  continue 
                message_text += line  + '\n'
                
                
            ## db operations 
            try: 
                from_eid = get_employee_id(sender)
                if from_eid == -1: # a new employee 
                    eid = get_max_employee_id() + 1
                    insert_employee(eid, xfrom, sender)
                    
                max_mid = get_max_message_id()
                
                insert_message(max_mid + 1, sender, receiver, subject, dt, message_text)
                insert_message_aux_info(max_mid + 1, xfrom, xto, xfolder, xorigin, xfile)
            except Exception as err:
                logger.exception('File: %s function: %s'% (os.path.join(root, file_name), err))


            
            count += 1 
            
            # print count, file_name, subject, receiver, sender

    return count
'''
The main function call 

Examples: 
    python enron_email_parser.py -h 
    python enron_email_parser.py -d /home/cgeorge/Dropbox/eDiscovery/data -l -s localhost -n enron -u eduser -p eddb13

'''
if __name__=="__main__":
    
    arg_parser = argparse.ArgumentParser('Enron email (in plain text) parser:')
    arg_parser.add_argument("-d", dest="directory", type=str, help="the root directory for all the mails", required=True)
    arg_parser.add_argument("-l", "--log", dest="log", default=False, action="store_true", help="log details into a log file (enron_insert_db.log)")
    arg_parser.add_argument("-s", dest="host", type=str, help="db server address", required=True)
    arg_parser.add_argument("-n", dest="dbname", type=str, help="db name", required=True)
    arg_parser.add_argument("-u", dest="user", type=str, help="db user name", required=True)
    arg_parser.add_argument("-p", dest="password", type=str, help="db user login password", required=True)
    
    args = arg_parser.parse_args()
    
    # Sets connection string from arguments 
    CONNECTION_STRING = "host='%s' dbname='%s' user='%s' password='%s'" % (args.host, args.dbname, args.user, args.password)
    

    # create file handler which 
    # logs even debug messages
    if args.log: 
        fh = logging.FileHandler('enron_insert_db.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    logger.info('Execution directory: %s' % args.directory)
    
    logger.info('Loads email paths...')
    file_tuples = get_file_info(args.directory)
    
    logger.info('Loads emails into the data base')
    
    current_time = time.time()
    
    num_files_inserted = insert_files(file_tuples)
    
    exec_time = time.time() - current_time
    
    logger.info('DB inserts are completed. Execution time = %0.4f seconds. Number of files = %d' % (exec_time, num_files_inserted))
    
    
    
