import sqlite3 as sql 
import os
from imgidvalues import imgid
from connection import conn
#conn=sql.connect('/home/chetan/Desktop/Image-Organizer/ImageData3.db',check_same_thread=False)

'''def Execute(q ,cursor = False):
    cur = conn.cursor()
    cur.execute(q)
    res =cur.fetchall()
    #conn.commit()
    if cursor:
        return cur
    return res'''
cur=conn.cursor()

cur.execute("PRAGMA foreign_keys = ON")




def call_script():
	print('calling the trgger script')
	query="select imgid from images"
	cur.execute(query)
	res=cur.fetchall()
	newimgid = list()
	for item in res:
		newimgid.append(item[0])

	appendimgid = list(set(newimgid) - set(imgid))

	for item in appendimgid:
		query = "select imgname from images where imgid = %s"%(item)
		cur.execute(query)
		res=cur.fetchall()
		print(res)
		os.system('/home/chetan/Desktop/darknet/test.sh ' + item)
		imgid.append(item)

def define_test():
	print("hello")
conn.create_function("call_scripts", 0, call_script)
#cur.execute("CREATE TRIGGER run_on_insert_image AFTER UPDATE ON images BEGIN SELECT call_scripts(); END;")

#Execute("CREATE TRIGGER run_on_insert_image AFTER INSERT ON images BEGIN SELECT call_script(); END;")
#call_script()
