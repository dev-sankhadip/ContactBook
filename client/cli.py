import click
import keyring
import requests
from PyInquirer import style_from_dict,Token,Separator,prompt

@click.group()
def main():
    """Simple CLI tool for storing contacts in System"""
    pass

@main.command()
@click.option('--name', prompt='Your Name', required=True, type=str)
@click.option('--email', prompt='Your Email', required=True, type=str)
@click.option('--password', prompt='Your Password', required=True, type=str,hide_input=True, confirmation_prompt=True)
def signup(name, email, password):
    click.echo(password)


@main.command()
@click.option('--name', prompt='Your Email', required=True, type=str)
@click.option('--password', prompt='Your Password',required=True, type=str, hide_input=True, confirmation_prompt=True)
def login(name, password):
    click.echo(name)
    click.echo(password)


if __name__ == "__main__":
    main()