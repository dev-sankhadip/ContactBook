import sqlite3
import uuid
import datetime

class Database:
    
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists contact (id integer primary key AUTOINCREMENT, name text, number int, address text, email text, date text)')
        self.conn.commit()
    
    def insertContact(self,name, number, address, email):
        date = datetime.datetime.now()
        self.cur.execute('insert into contact values(NULL,?,?,?,?,?)',(name, number, address, email, date))
        self.conn.commit()
    
    def getContacts(self):
        self.cur.execute('select * from contact')
        rows=self.cur.fetchall()
        return rows