import click
import requests
import re
import json
from PyInquirer import style_from_dict,Token,Separator,prompt
import configstore

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
signup_url = 'http://localhost:2222/cli/signup'
login_url = 'http://localhost:2222/cli/login'


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
def get():
    configstore.setUserConfig('1','2','3')

if __name__ == "__main__":
    main()