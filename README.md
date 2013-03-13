PyCon2013
=========

Code, data and slides for PyCon 2013


Install instructions
=========
$ mkvirtualenv sna --python=python2.7     

If you have never installed matplotlib on your machine before:
    Next, we will install the requirements. If you have never installed 
matplotlib before, you need (brew,port,apt-get) some extra files. 
Read more here: http://matplotlib.org/users/installing.html#build-requirements

After you have the libraries needed, continue with installing the 
requirements.txt.

$ pip install -r requirements.txt


To run ipython notebooks
=========
pip install...   
ipython==0.13.1    
pyzmq==13.0.0    
tornado==2.4.1   

Run ipython notebook w/ inline graphs   
$ ipython notebook --pylab inline

For more info: http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html
