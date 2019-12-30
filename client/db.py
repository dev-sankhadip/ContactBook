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
    
    def getContactsByNameSort(self):
        self.cur.execute('select * from contact order by name')
        rows = self.cur.fetchall()
        return rows
    
    def deleteContact(self, id):
        self.cur.execute('select * from contact where id = ?',(id,))
        rows=self.cur.fetchall()
        if len(rows)>0:
            self.cur.execute('delete from contact where id = ?',(id,))
            self.conn.commit()
            return "Contact deleted"
        else:
            return "No contact found"
    def getContact(self, id):
        self.cur.execute('select * from contact where id = ?',(id,))
        rows=self.cur.fetchall()
        if len(rows)>0:
            return rows
        else:
            return "No contact found"
    def updateContact(self,answer, id):
        self.cur.execute('update contact set name = ?, number = ?, address = ?, email = ? where id = ?',(answer['name'], answer['number'], answer['address'], answer['email'], id))
        self.conn.commit()
        return "Updated"