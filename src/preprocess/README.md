Source dependencies: 
========================

1. The Gensim package is used for creating the LDA corpus and dictionary for topic modeling. Please see http://radimrehurek.com/gensim/ for more details 



Database configurations: 
========================

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
