# MINDFIRL
MINDFIRL stands for Minimum & Necessary Disclosure for Interactive Record Linkage. It is a software for interactive record linkage. For more information please visit https://pinformatics.tamhsc.edu/ppirl/

## Files
You can find these 4 files in the docs folder:
1. mindfirl_DUA.docx -> 
2. irb_app_template_mindfirl.docx -> 
3. faq.html -> frequently asked questions (The html file)
4. faq.zip -> frequently asked questions (all files for faq including images, css, and etc. files)

## How to install the software
Our software basically is a web server using Flask framework. It requires Python3, MongoDB, Redis, and some python packages. The install instruction is independent of the operating system. Some of the software or packages only provide the latest version. In this case, just install the latest version. 

1. Install python 3.6.5 (https://www.python.org/downloads/)
Any version after 3.6 should be able to work. However, we are using 3.6.5 currently. So it would be best if python 3.6.5 is installed.

2. Install MongoDB 3.6.4 (https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
We do not have authentication for MongoDB in our local environment. If there is authentication for MongoDB, please modify the setting in mindfirl-software/mindfirl/mindfirl.py accordingly (line 39)

3. Start MongoDB 

4. Open MongoDB in the terminal, use the following commands to create database and collections:
use mindfirl
db.createCollection("users")
db.createCollection("projects") 
db.createCollection("log")

5. Install redis server 5.0.2 (https://redislabs.com/ebook/appendix-a/a-3-installing-on-windows/a-3-2-installing-redis-on-window/)

6. Start redis server

7. Install the following python libraries:
Flask==0.12.2: https://pypi.org/project/Flask/
Jinja2==2.9.5: https://pypi.org/project/Jinja2/#files
requests==2.10.0: https://pypi.org/project/requests2/
simplejson==3.10.0: https://pypi.org/project/simplejson/#files
Werkzeug==0.11.15: https://pypi.org/project/Werkzeug/
gunicorn==19.0.0: https://pypi.org/project/gunicorn/
redis==2.10.6: https://pypi.org/project/redis/
flask-pymongo: https://pypi.org/project/Flask-PyMongo/
numpy: https://pypi.org/project/numpy/
flask-login==0.4.1: https://pypi.org/project/Flask-Login/
wtforms==2.1: https://pypi.org/project/WTForms/

8. Go to the folder mindfirl-software/mindfirl/
Run this command to start the software:
python run.py

9. Open the port 5000 on this server, then on the other computers, the uses should be able to access the software via a web browser at ip:5000

## How to use the software
1. Create an account and log in to MINDFIRL.
2. Create a project either by pair file or by blocking on fields and assign it to one or more users. (see help in MINDFIRL)
  - There are some demo files (/mindfirl/data) that you can use:
      * dev_file1.csv and dev_file2.csv are for creating a project by blocking.
      * pairfile_extra.csv and name_freq.csv are for creating a project by pair file.
3. Do your assignment.
4. After all users finished their assignment, you can export the result (projects -> export result)
5. More:

Tutorial: http://mindfil4.herokuapp.com/introduction

Video: https://www.youtube.com/watch?v=xM_Yw4h6nn4&feature=youtu.be
