import sqlite3 as sql
import os
#conn=sql.connect('/home/chetan/Desktop/Image-Organizer/ImageData3.db',check_same_thread=False)
conn=sql.connect(os.path.abspath('./ImageData3.db'),check_same_thread=False)
print(os.path.abspath('../ImageData3.db'))