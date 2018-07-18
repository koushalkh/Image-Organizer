import sqlite3 as sql

def create_table():
	con=sql.connect('USERINFO.db')
	#	print("haha")
	con.execute("DROP TABLE IF EXISTS USER")
	con.execute("CREATE TABLE USER(username TEXT PRIMARY KEY NOT NULL,password TEXT NOT NULL)")
	c=con.cursor()
	con.execute("INSERT INTO USER(username,password) VALUES('admin','admin')")
	con.commit()

create_table()
