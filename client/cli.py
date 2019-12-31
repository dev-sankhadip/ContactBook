import click
from operations import Operations
from db import Database
import speech_recognition as sr
import pyttsx3


engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# initialize database connection
db=Database('store.db')

#create operations object
operation=Operations()


# any string passed to it, computer will speak
def say(audio):
    engine.say(audio)
    engine.runAndWait()


# take input from microphone and recognize contact operation command
def recognizeCommand():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Say that again please...")  
        return "None"
    return query



# group all commands
@click.group()
def main():
    """Simple CLI tool for storing contacts in System"""
    pass


# signup command
@main.command()
@click.option('--name', prompt='Your Name', required=True, type=str)
@click.option('--email', prompt='Your Email', required=True, type=str)
@click.option('--password', prompt='Your Password', required=True, type=str,hide_input=True, confirmation_prompt=True)
def signup(name, email, password):
    operation.signup(name, email, password)


# login command
@main.command()
@click.option('--email', prompt='Your Email', required=True, type=str)
@click.option('--password', prompt='Your Password',required=True, type=str, hide_input=True)
def login(email, password):
    operation.login(email, password)


# contact create contact
@main.command()
@click.option('--name', prompt="His/Her name", required=True, type=str)
@click.option('--number', prompt="His/Her number", required=True, type=int)
@click.option('--address', prompt="His/Her address", type=str, default='null')
@click.option('--email', prompt="His/Her Email address", type=str, default='null')
def create(name, number, address, email):
    operation.create(name, number, address, email)


# all contact read command
@main.command()
def read():
    operation.read()


# contact delete command
@main.command()
@click.option('--id', prompt="Contact Id", required=True, type=int)
def delete(id):
    operation.delete(id)


# contact update command
@main.command()
@click.option('--id', prompt="Contact id", required=True, type=int)
def update(id):
    operation.update(id)


# contact search command
@main.command()
@click.option('--keyword', prompt="Type contact keyword",required=True, type=str)
def search(keyword):
    operation.search(keyword)

# contacts operation by speech recognition
@main.command()
def speak():
    command = recognizeCommand().lower()
    if command=='search':
        print(command)
    elif command=='delete':
        print(command)
    elif command=='read':
        print(command)
    else:
        print(command)


if __name__ == "__main__":
    main()