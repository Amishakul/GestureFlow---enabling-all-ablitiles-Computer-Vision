import speech_recognition as sr
import pyttsx3
import keyboard
import os
import subprocess
import webbrowser
import time


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    command = ""  # Initialize command with an empty string
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except sr.UnknownValueError:
        pass
    return command



def open_folder(path):
    if os.path.exists(path):
        if os.name == 'nt':  # For Windows OS
            subprocess.Popen(f'explorer {os.path.realpath(path)}')
    else:
        talk("Folder doesn't exist.")

def type_word_by_word(text):
    words = text.split()
    for word in words:
        if word == 'enter':
            keyboard.press_and_release('enter')
        else:
            keyboard.write(word)
            keyboard.press_and_release('space')
            time.sleep(0.1)

def run_voice_typing():
    talk('Starting voice typing...')
    command = take_command()
    type_word_by_word(command)

def copy_selected_file():
    keyboard.send('ctrl+c')
    time.sleep(1)  # Add a delay to ensure the file is copied
    talk('copied file...')


def paste_selected_file():
    keyboard.send('ctrl+v')
    time.sleep(1)  # Add a delay to ensure 
    talk('pasted file...')

def cut_selected_file():
    keyboard.send('ctrl+x')
    time.sleep(1)  # Add a delay to ensure 
    talk('cut file...')

def delete_selected_file():
    keyboard.send('delete')
    time.sleep(1)  # Add a delay to ensure 
    talk('deleted file...')




def run_alexa():
    command = take_command()
    print(command)

    #open imp desktop , download like folders directly... by giving cmd like desktop, downloads, documents etc.
    if 'desktop' in command:
        talk('Opening desktop folder')
        open_folder(os.path.join(os.path.expanduser('~'), 'Desktop'))
    elif 'downloads' in command:
        talk('Opening downloads folder')
        open_folder(os.path.join(os.path.expanduser('~'), 'Downloads'))
    elif 'documents' in command:
        talk('Opening documents folder')
        open_folder(os.path.join(os.path.expanduser('~'), 'Documents'))
    elif 'pictures' in command:
        talk('Opening pictures folder')
        open_folder(os.path.join(os.path.expanduser('~'), 'Pictures'))
    elif 'videos' in command:
        talk('Opening videos folder')
        open_folder(os.path.join(os.path.expanduser('~'), 'Videos'))
    elif 'music' in command:
        talk('Opening music folder')
        open_folder(os.path.join(os.path.expanduser('~'), 'Music'))

    #down,left,right,up go in folders or like. eg. kissi ek file pe click hai to uske left wali file pe jano ko "left" asa cmd do etc.
    elif 'down' in command:
        talk('Pressing down key')
        keyboard.press('down')  # Simulate pressing the down arrow key
        keyboard.release('down')  # Release the down arrow key
    elif 'up' in command:
        talk('Pressing up key')
        keyboard.press('up')
        keyboard.release('up')
    elif 'left' in command:
        talk('Pressing left key')
        keyboard.press('left')
        keyboard.release('left')
    elif 'right' in command:
        talk('Pressing right key')
        keyboard.press('right')
        keyboard.release('right')
    

    #DAILY USED APPLICATIONS OPEN BY VOICE CMD. for eg: file explorer, gmail open directly by voice cmd.
    elif 'file explorer' in command:
        talk('Opening File Explorer')
        if os.name == 'nt':
            subprocess.Popen('explorer')
    elif 'gmail' in command:
        talk('Opening Gmail')
        webbrowser.open('https://mail.google.com')

    elif 'type' in command:
        run_voice_typing()


    #cut,copy,paste,delete file.eg. file pe click karke rakhna phir copy file cmd give and then dusre folder mai jake waha cmd give paste file so it will get paste.
    elif 'copy file' in command:
        copy_selected_file()

    elif 'paste file' in command:
        paste_selected_file()

    elif 'cut file' in command:
        cut_selected_file()

    elif 'delete file' in command:
        delete_selected_file()
    else:
        talk('Please say the command again.')


while True:
    run_alexa()
