import sqlite3 as sql

#connect to SQLite
con = sql.connect('db_web.db')

#Create a Connection
cur = con.cursor()

#Drop users table if already exsist.
#cur.execute("DROP TABLE IF EXISTS users")

#Create users table  in db_web database
sql ='''CREATE TABLE "UserData" (
	"UID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"UNAME"	TEXT,
	"CONTACT"	TEXT,
    "EMAIL"	TEXT,
    
)'''
#cur.execute(sql)

addtable = ''' ALTER TABLE "UserData"
ADD NOTES varchar; '''

cur.execute(addtable)
#commit changes
con.commit()

#close the connection
con.close()