import click
import requests
import re
import json
from PyInquirer import style_from_dict,Token,Separator,prompt
import configstore
from db import Database
from texttable import Texttable
from PyInquirer import style_from_dict, Token, prompt
from examples import custom_style_2



regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
signup_url = 'http://localhost:2222/cli/signup'
login_url = 'http://localhost:2222/cli/login'

db=Database('store.db')

@click.group()
def main():
    """Simple CLI tool for storing contacts in System"""
    pass

@main.command()
@click.option('--name', prompt='Your Name', required=True, type=str)
@click.option('--email', prompt='Your Email', required=True, type=str)
@click.option('--password', prompt='Your Password', required=True, type=str,hide_input=True, confirmation_prompt=True)
def signup(name, email, password):
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



@main.command()
@click.option('--email', prompt='Your Email', required=True, type=str)
@click.option('--password', prompt='Your Password',required=True, type=str, hide_input=True)
def login(email, password):
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

@main.command()
@click.option('--name', prompt="His/Her name", required=True, type=str)
@click.option('--number', prompt="His/Her number", required=True, type=int)
@click.option('--address', prompt="His/Her address", type=str, default='null')
@click.option('--email', prompt="His/Her Email address", type=str, default='null')
def create(name, number, address, email):
    db.insertContact(name, number, address, email)

@main.command()
def read():
    contacts = db.getContacts()
    t = Texttable()
    t.set_cols_dtype(['i','t','i','t','t'])
    t.add_rows([['id','Name', 'Number','Address','Email']])
    for contact in contacts:
        t.add_row([contact[0], contact[1], str(contact[2]), contact[3], contact[4]])
    print(t.draw())

@main.command()
@click.option('--id', prompt="Contact Id", required=True, type=int)
def delete(id):
    result = db.deleteContact(id)
    print(result)

@main.command()
@click.option('--id', prompt="Contact id", required=True, type=int)
def update(id):
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







@main.command()
def set():
    configstore.setUserConfig('1','2','3')

@main.command()
def get():
    configData = configstore.getUserConfig()
    print(configData)

if __name__ == "__main__":
    main()