Data base configurations: 
=========================

Ref: http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/


UNIX: 
=====

sudo adduser eduser # creates a new db system user 

Postgres 
========

sudo su - postgres 

psql -d template1 -U postgres

create user eduser with password ‘password’; # creates a db user 

create database enron; # creates a databased named 'enron'

GRANT ALL PRIVILEGES ON DATABASE enron to eduser; # grant all permissions to eduser 

sudo /etc/init.d/postgresql restart 9.1 # restart postgres 
