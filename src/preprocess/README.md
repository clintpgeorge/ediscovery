Description
------------

This module contains the source code for preprocessing datasets. 


Supported public datasets 
-------------------------
Enron [http://www.cs.cmu.edu/~enron/]: This module has scripts to (a) process the enron emails which is in the plain text format, (b) insert into Postgres database, and (c) convert the documents collections to topic modeling input format (e.g. Blei corpus). 



Source dependencies
--------------------

1. The Gensim package is used for creating the LDA corpus and dictionary for topic modeling. Please see http://radimrehurek.com/gensim/ for more details 



Database configurations 
------------------------

This section describes how to setup a Postgres server in a Unix environment. For a detailed review see http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/

Steps: 

1. Unix: 
  - sudo adduser eduser # creates a new db system user 

2. Postgres:  
  - sudo su - postgres 
  - psql -d template1 -U postgres
  - create user eduser with password ‘password’; # creates a db user 
  - create database enron; # creates a databased named 'enron'
  - GRANT ALL PRIVILEGES ON DATABASE enron to eduser; # grant all permissions to eduser 
  - sudo /etc/init.d/postgresql restart 9.1 # restart postgres 
