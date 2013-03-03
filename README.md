Research outline
----------------

EDiscovery refers to the management of electronically stored information 
in the litigations, dispute resolution proceedings, and investigations. 
Different machine learning techniques such as supervised classification 
and unsupervised clustering have been employed to reduce manual 
(linear human review) and increase investigative speed and efficiencies. 
We propose to improve on the state of the art of machine learning for 
EDiscovery by i) using topic modeling to provide greater power than 
commonly employed methods such as keyword search and Latent Semantic Analysis, 
ii) using identified topics for document categorization and ranking their 
relevance to a given query, and iii) using the topic framework to provide 
document summaries. Furthermore, to ensure the broad penetration of our effort, 
all software tools resulting from this effort will be implemented in the context 
of an open-source system that can serve as the basis for an open EDiscovery framework.



General guide lines
-------------------
This section provides the general guidelines to access the Git Hub repository, coding style, enhancements, and issue tracking.  

**To Edit this file**

See GitHub markdown online [help](https://help.github.com/articles/github-flavored-markdown)


**Enhancements and issues**

* Use the [***issues***](https://github.com/clintpgeorge/ediscovery/issues?state=open) tab to keep track of all issues and enhancements. 
* When we check in the soruce code to the repository, specify the inssue or enhancement number in the checkin message. 
  e.g. ```git commit -a -m'issue #1 fix: see the issue details for information.'```


**Git**

To clone the [***ediscovery***](https://github.com/clintpgeorge/ediscovery) repository use the following command

    git clone https://github.com/clintpgeorge/ediscovery

See [crash course on Git SVN](http://git.or.cz/course/svn.html) for more details. 
The following are some useful ***git*** commands 

    git pull # to update the local from the remote 
    git status # to see the local repository status 
    git add file_name # to add a new file file_name 
    git commit -a -m'[commit message]' # for commit all files in your local 
    git push # to update your commits to the master 

**Python**

- do not check in *.pyc files 
- follow [coding standards](http://www.python.org/dev/peps/pep-0008)
- use [argparse](http://docs.python.org/2/howto/argparse.html) for handling arguments 
- use no hard coding in functions except for the test scripts, try to pass all constants as function parameters

--------------------------------------

