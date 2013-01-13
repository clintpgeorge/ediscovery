DB creattion: 
==============

http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/

UNIX: 
=====

sudo adduser eduser 

Postgres 
========

sudo su - postgres

psql -d template1 -U postgres

create user eduser with password ‘password’; 

create database enron; 

GRANT ALL PRIVILEGES ON DATABASE enron to eduser;

restart postgres 
sudo /etc/init.d/postgresql restart 9.1
