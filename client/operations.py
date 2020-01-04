import requests
import re
import json
from PyInquirer import prompt
import configstore
from db import Database
from texttable import Texttable
from examples import custom_style_2, custom_style_1
import click
import speech_recognition as sr
import pyttsx3
import os


engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
signup_url = 'http://localhost:2222/cli/signup'
login_url = 'http://localhost:2222/cli/login'
backup_url = 'http://localhost:2222/cli/backup'

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
    
    def backup(self):
        contactDB = open('store.db','rb')
        res = os.system('curl \
            -F "userid=1" \
            -F "filecomment=This is an image file" \
            -F "image=@store.db" \
            localhost:2222/cli/backup')
        contactDB.close()
        print(res)
        


operationsObject = Operations()

class SpeechOperations:

    # any string passed to it, computer will speak
    def say(self,audio):
        engine.say(audio)
        engine.runAndWait()
    

    def recognizeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")    
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}\n")

        except Exception as e:
            print(e)
            print("Say that again please...")  
            return "None"
        return query


    def search(self):
        lines = "Say contact keyword"
        self.say(lines)
        keyword = self.recognizeCommand()
        if keyword.isalpha()==True:
            result=db.searchContact(keyword)
            if result=="No contact found":
                self.say(result)
            else:
                operationsObject.printContacts(result)
        else:
            print("Not recognized, please say again")
            self.search()
    
    def delete(self):
        lines = "Say contact id"
        self.say(lines)
        id = self.recognizeCommand()
        if id.isdigit()==True:
            result = db.deleteContact(id)
            self.say(result)
        else:
            print("Not recognized, please say again")
            self.delete()
    
    def read(self):
        lines = "Do you want to list in order by name"
        print(lines)
        self.say(lines)
        ans = self.recognizeCommand().lower()
        if ans=="yes":
            contacts = db.getContacts()
            operationsObject.printContacts(contacts)
        else:
            contacts = db.getContactsByNameSort()
            operationsObject.printContacts(contacts)