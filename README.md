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

- Do not check in *.pyc files 
- Follow [coding standards](http://www.python.org/dev/peps/pep-0008)
- Use [argparse](http://docs.python.org/2/howto/argparse.html) for handling arguments 
- Use no hard coding in functions except for the test scripts, try to pass all constants as function parameters

**pyLucene Installation**

**Ubuntu**

- Install g++
- Install python-dev
- Download pylucene3.6 from http://mirror.sdunix.com/apache/lucene/pylucene/
- Execute the following command in JCC installation directory
    - python setup.py build 
    - sudo python setup.py install
- Uncomment properties applicable to relevant platform(Linux,Mac,Windows) etc. from pylucene makefile
- Install ant
- Install setuptools
- Execute following commands from pylucene directory
      - make
      - sudo make install
      - make test

**Windows 7 and Python 32 bit**

- Install Java JDK (32 bit) latest version 
- Install Python [setup tools](http://pypi.python.org/pypi/setuptools) 
- Follow instructions in [pyLucene Extra](https://code.google.com/a/apache-extras.org/p/pylucene-extra/wiki/PyLucene). Direct installation using the installation files from the Apache site is cumbersome some times. 


**Topic Modeling**

- Topic modeling is performed using the package Gensim -- http://radimrehurek.com/gensim/ 


**Development Environment Setup**

Please follow the following steps in the order given below for setting up development 
environment, The executables can be found in the software folder(Coming Soon)

- Install Python27
- Install sciPy, NumPy, wxPython, pywin32, Py2exe
- Install wxFormBuilder
- Delete files boot_common.py, and boot_common.pyc from C:\Python27\Lib\site-packages\py2exe. Add the boot_common.py from the software folder to the given path, compile it using the following code in python CLI

    
    import py_compile
    py_compile.compile('boot_common.py')
    

*for SMARTeR*

- Install both Visual Studio Express 2008 and 2010
- Run the script ez_setup.py
- Using the following command install gensim, JCC and lucene

    easy_install <file_name>.egg


--------------------------------------

