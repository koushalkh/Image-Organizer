import  sqlite3 as sql
import time
import os
from  app.connection import conn
from pathlib import Path
import multiprocessing
def Execute(q ,cursor = False):
    cur = conn.cursor()
    cur.execute(q)
    res =cur.fetchall()
    conn.commit()
    if cursor:
        return cur
    return res
Execute("PRAGMA foreign_keys = ON")
def insertImages(uid , imgname , imglink ):
    query = 'insert into images(uid,imgname,imglink,upvotes,objects,processed) values("%s","%s","%s",0,0,0)'%(uid , imgname , imglink)
    try:
        Execute(query)
    except:
        return False
    return True
    
def PublicSearch(attr):
    query = 'select imglink from images I , attributes A where I.imgid = A.imgid and objname = "%s" '%(attr)
    try:
        res = Execute(query)
        #print(res)
    except:
        return None
    return [r[0] for r in res]
def  suggestions(uid):
    query = 'select objname from  images I , attributes A  where I.imgid = A.imgid and I.uid = "%s"'%(str(uid))
    try:
        res = Execute(query)
        #print(res)
    except:
        return None
    return  [r[0] for r in res]


def insertAttribute(imgid , objname):
    query = 'insert into attributes values ("%s","%s")'%(imgid,objname)
    try:
        Execute(query)
    except:
        return False
    return True

def addObjects(imgid, objset):
    
    query = 'update images set objects = %d where imgid = "%s"'%(len(objset),imgid)
    q = 'update images set processed = 1 where imgid = "%s"'%(imgid)
    try:
        Execute(query)
        Execute(q)
        for obj in objset:
            insertAttribute(imgid,obj)
        return True
    except Exception as e:
        print(e)
        return False

#print(insertImages(1,'DogPerson.jpeg','/home/koushal/Documents/multiprocess/images/DogPerson.jpeg'))

print(Execute("select * from images"))

def getList(outputloc):
    fhand = open(outputloc, "r")
    count = 0
    l = list()
    for line in fhand:
        if count == 0:
            count = 1
            continue
        s = line.split()
        l.append((s[0][:len(s[0]) - 1]))
    
    l = list(set(l))
    return l


def EXECUTE_ALGO(image_names , imgid):
    #outputloc = os.path.abspath('app/outputs/img%s.txt'%(imgid))
    outputloc = '/home/chetan/Desktop/Image-Organizer/app/outputs/img%s.txt'%(imgid)
    print(image_names)
    #os.system(os.path.abspath('app/test.sh  %s  %s'%(image_names, outputloc)))
    os.system('/home/chetan/Desktop/Image-Organizer/app/test.sh  %s  %s'%(image_names, outputloc))
    objList = getList(outputloc)
    addObjects(imgid,objList)
    #print(open(outputloc,'r').read())





while True:
    res  = Execute('select imglink , imgid from images where processed =  0')
    print(res)
    if  len(res) is 0 :
        print("sleeping.")
        time.sleep(  10)
        print("continued!! after sleep")
        continue
    else:
        t=[]
        length= len(res)
        if(multiprocessing.cpu_count()<length):
            length = multiprocessing.cpu_count()
        for i in range(length):
            t.append(res[i])
        print(t)
        pool=multiprocessing.Pool(processes=length)
        result=[pool.apply_async(EXECUTE_ALGO,a) for a in t]
        for item in result:
            item.get()
        #pool.map(EXECUTE_ALGO,t)


print(Execute("select * from attributes"))  






