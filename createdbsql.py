
from sqlite3 import Cursor
import pymysql


# To connect MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root', 
    password = "admin",
    db='data',
    )


Cursor = conn.cursor()
sql ='''CREATE TABLE "UserData" (
	"UID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"UNAME"	TEXT,
	"CONTACT"	TEXT,
    "EMAIL"	TEXT,
    
)'''
Cursor.execute(sql)
conn.close()