import requests
import re
import json
from PyInquirer import prompt
import configstore
from db import Database
from texttable import Texttable
from examples import custom_style_2, custom_style_1
import click

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
signup_url = 'http://localhost:2222/cli/signup'
login_url = 'http://localhost:2222/cli/login'

# initialize database connection
db=Database('store.db')

class Operations:

    # print contacts in tabular form in terminal
    def printContacts(self,contacts):
        t = Texttable()
        t.set_cols_dtype(['i','t','i','t','t'])
        t.add_rows([['id','Name', 'Number','Address','Email']])
        for contact in contacts:
            t.add_row([contact[0], contact[1], str(contact[2]), contact[3], contact[4]])
        print(t.draw())
    
    def signup(self,name, email, password):
        if re.search(regex,email):
            if len(password)>6:
                data = {
                    'name':name,
                    'email':email,
                    'password':password
                }
                result = requests.post(url=signup_url, data=data)
                click.echo(result.text)
            else:
                click.echo('Password should be greater than 6 character')
        else:
            click.echo("Invalid email")
    
    def login(self,email, password):
        if re.search(regex,email):
            data = {
                'email':email,
                'password':password
            }
            result = requests.post(url=login_url,data=data)
            jsonResult = json.loads(result.text)
            code = jsonResult['code']
            if code==200:
                print('Loggedin')
            elif code==401:
                click.echo('Wrong password')
            elif code==400:
                click.echo('User not found')
            else:
                click.echo('Server error')
        else:
            click.echo("Invalid email")
    
    def create(self,name, number, address, email):
        db.insertContact(name, number, address, email)
    
    def read(self):
        questions = [
            {
                'type': 'confirm',
                'message': 'Do you want to list in order by name?',
                'name': 'sort',
                'default': False,
            },
        ]
        answers = prompt(questions, style=custom_style_1)
        if answers['sort']==False:
            contacts = db.getContacts()
            self.printContacts(contacts)
        else:
            contacts = db.getContactsByNameSort()
            self.printContacts(contacts)
    
    def delete(self,id):
        result = db.deleteContact(id)
        print(result)
    
    def update(self,id):
        result = db.getContact(id)
        if result=='No contact found':
            print('No contact found')
        else:
            data=result[0]
            questions = [
                {
                    'type': 'input',
                    'name': 'name',
                    'message': 'What\'s name',
                    'default':f"{data[1]}"
                },
                {
                    'type': 'input',
                    'name': 'number',
                    'message': 'What\'s phone number',
                    'default':f"{data[2]}"
                },
                {
                    'type': 'input',
                    'name': 'address',
                    'message': 'What\'s address',
                    'default':f"{data[3]}"
                },
                {
                    'type':'input',
                    'name':'email',
                    'message':'What\'s email',
                    'default':f"{data[4]}"
                }
            ]
            answers = prompt(questions, style=custom_style_2)
            res = db.updateContact(answers,id)
            print(res)
    
    def search(self,keyword):
        result=db.searchContact(keyword)
        if result=="No contact found":
            print("No contact found")
        else:
            self.printContacts(result)
    