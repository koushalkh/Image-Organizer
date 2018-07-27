from flask import render_template,flash,redirect,url_for,request,session,abort
import sqlite3 as sql 
import os
from connection import conn
#conn=sql.connect('/home/chetan/Desktop/Image-Organizer/ImageData3.db',check_same_thread=False)
# In[2]:


# In[3]:

def Execute(q ,cursor = False):
    cur = conn.cursor()
    print('before execute')
    cur.execute(q)
    print('after execute')
    res =cur.fetchall()
    conn.commit()
    if cursor:
        return cur
    return res




# In[4]:


Execute("PRAGMA foreign_keys = ON")


# In[10]:

def createTables():
    users = "create table users (uid integer primary key autoincrement, uname text not null unique, pwd text not null , email text not null, phoneno text)"
    images = 'create table images (uid integer not null ,imgid integer primary key autoincrement ,imgname text not null  , imglink text not null unique, upvotes integer , objects integer, foreign key(uid) references users(uid) on delete cascade)'
    attributes = 'create table attributes ( imgid integer not null ,objname text not null , primary key(imgid , objname) , foreign key(imgid) references images(imgid) on delete cascade)'
    favourites = 'create table favourites (imgid integer not null , uid integer not null , primary key (uid,imgid) ,foreign key(uid) references users(uid) on delete cascade, foreign key(imgid) references images(imgid) on delete cascade)'
    try:
        Execute(users)
        Execute(images)
        Execute(attributes)
        Execute(favourites)
    except:
        print("error occured while creating table")

#createTables()


# In[89]:

def insertUser(uname , pwd , email , phoneno = ''):
    """
    Used to create a new user.
    usage:
        insertUser("koushal","abcd","me@koushalkh.com","9900955117")
    """
    query = 'insert into users (uname , pwd , email , phoneno) values("%s","%s","%s","%s")'%(uname,pwd,email,phoneno)
    try:
        Execute(query)
    except:
        raise ValueError("uname aldredy exists.")

#insertUser('koushal','abc','koushalkh@gmail.com','9989898989')
#insertUser('madan','abc','madan@gmail.com','9989898989')

def SignIn(uname, pwd):
    """
    Call this function to validate the credentials.
    -> if uname and pwd match with entry in database it returns True else if error occurs it returns False
    """
    query = 'select pwd from users where uname = "%s"'%(uname)
    try:
        res = Execute(query)
        if str(res[0][0]) == pwd:
            q='select uid from users where uname= "%s"'%(uname)
            r=Execute(q)
            session['uid']=r[0][0]
            print(session['uid'])
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
print(Execute('PRAGMA table_info([users])'))


def SignUp(uname , pwd , email , phoneno = ''):
    """
    used to create a new user.
    -> returns True if new user is created.
    """
    try:
        insertUser(uname , pwd , email , phoneno)
    except Exception as e:
        print(e)
        return False
    return True


def insertImages(uid , imgname , imglink ):
    query = 'insert into images(uid,imgname,imglink,upvotes,objects) values("%s","%s","%s",0,0)'%(uid , imgname , imglink )
    try:
        #Execute(query)
        cur = conn.cursor()
        print("Inserting images")
        #cur.execute(query)
        Execute(query)
    except Exception as e:
        print(e)
        #return False
    #return True


def upvote(imgid):
    """
    Used to upvote an image
    does not return anything, takes imgid as input.
    """
    query = 'update  images set upvotes = (upvotes + 1) where imgid = %d'%(imgid)
    Execute(query)

def insertAttribute(imgid , objname):
    query = 'insert into attributes values ("%s","%s")'%(imgid,objname)
    try:
        Execute(query)
    except:
        return False
    return True
def insertFavourites(imgid,uid):
    query = 'insert into favourites(imgid,uid) values (%d,%d)'%(imgid,uid)
    print(query)
    Execute(query)
    
def addObjects(imgid, objset):
    query = 'update images set objects = %d where imgid = "%s"'%(len(objset),imgid)
    try:
        Execute(query)
        for obj in objset:
            insertAttribute(imgid,obj)
        return True
    except:
        return False


def PublicSearch(attr):
    query = 'select imglink from images I , attributes A where I.imgid = A.imgid and objname = "%s" '%(attr)
    try:
        res = Execute(query)
        print(res)
    except:
        return None
    return [r[0] for r in res]