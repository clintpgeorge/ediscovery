Data preprocess module 
======================

This module contains the source code for preprocessing datasets. This includes methods such as 
* deduplication 
* deNISTing 
* handling different file types 
* NLP techniques such as tokenization, stemming, lemmatization, stopwords removal  


Supported public datasets 
-------------------------
[Enron](http://www.cs.cmu.edu/~enron/) dataset: This module has scripts to 
- process the enron emails which is in the plain text format
- insert into Postgres database
- convert the documents collections to topic modeling input format (e.g. Blei corpus)



Source dependencies
--------------------
The [Gensim package](http://radimrehurek.com/gensim/) is used for creating the LDA corpus and dictionary for topic modeling. 



Database configurations 
------------------------

This section describes how to setup a Postgres server in a Unix environment. For a detailed review [see](http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/)

Steps: 

Unix: 

    sudo adduser eduser # creates a new db system user 

Postgres:  

    sudo su - postgres 
    psql -d template1 -U postgres
    create user eduser with password ‘password’; # creates a db user 
    create database enron; # creates a databased named 'enron'
    GRANT ALL PRIVILEGES ON DATABASE enron to eduser; # grant all permissions to eduser 
    sudo /etc/init.d/postgresql restart 9.1 # restart postgres 
