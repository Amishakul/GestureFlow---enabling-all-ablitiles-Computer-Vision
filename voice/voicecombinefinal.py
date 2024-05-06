import os
import time
import webbrowser
import pyttsx3
import speech_recognition as sr
import pyautogui
import keyboard
import sys

def open_youtube_shorts():
    url = 'https://www.youtube.com/shorts'
    webbrowser.open(url)
    speak("Opening YouTube Shorts.")

def open_youtube_king_shorts():
    url = 'https://www.youtube.com/@King/shorts'
    webbrowser.open(url)
    speak("Opening YouTube Shorts of King.")

def open_youtube_channel():
    url = 'https://www.youtube.com/@King'
    webbrowser.open(url)
    speak("Opening YouTube Channel of King.")

def open_youtube():
    url = 'https://www.youtube.com/'
    webbrowser.open(url)
    speak("Opening YouTube.")

def search_youtube_channel(channel_name):
    search_url = f"https://www.youtube.com/results?search_query={channel_name}&sp=EgIQAg%253D%253D"
    webbrowser.open(search_url)
    speak(f"Searching for {channel_name} on YouTube.")

def open_youtube_trending():
    trending_url = "https://www.youtube.com/feed/trending"
    webbrowser.open(trending_url)
    speak("Opening YouTube trending section.")

def play_youtube_song(song_query):
    try:
        youtube_url = f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}"
        webbrowser.open(youtube_url)
        print(f"Playing song on YouTube: {song_query}")
    except Exception as e:
        print(f"Error playing the song on YouTube: {e}")

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)

def search_or_open_website(query):
    if query.lower() == "www.amazon.in":
        webbrowser.open("https://www.amazon.in")
    elif query.lower() == "www.google.in":
        webbrowser.open("https://www.google.in")
    elif query.startswith("www.") or query.startswith("http://") or query.startswith("https://"):
        # If the query looks like a website URL, open it directly
        webbrowser.open(query)
    else:
        # Otherwise, perform a Google search
        search_google(query)

def open_pdf(file_path):
    try:
        os.startfile(file_path)
    except FileNotFoundError:
        print("File not found or application not available.")

def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def voice_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)

        if "open youtube shorts" in command:
            open_youtube_shorts()
        elif "open king" in command:
            open_youtube_king_shorts()
        elif "open youtube channel" in command:
            open_youtube_channel()
        elif "open youtube" in command:
            open_youtube()
        elif "search for youtube" in command:
            query = command.replace("search for youtube", "").strip()
            search_youtube(query)
        elif 'search for' in command:
            query = command.replace("search for", "").strip()
            search_or_open_website(query)
        elif "open trending" in command:
            open_youtube_trending()
        elif 'play' in command:
            song_query = command.split('play')[1].strip()
            play_youtube_song(song_query)
        elif "pause" in command:
            pause_video()
            print("Pausing the video.")
        elif "resume" in command:
            resume_video()
            print("Resuming the video.")
        elif "skip forward" in command:
            skip_forward()
        elif "skip backward" in command:
            skip_backward()
        elif "scroll up" in command:
            scroll_up()
        elif "scroll down" in command:
            scroll_down()
        elif 'open pdf' in command:
            open_pdf("C:\Gesture_Project\gayatri part\hand\Java L10.pdf")  # Specify the file path here
        elif 'zoom in' in command:
            zoom_in()
        elif 'zoom out' in command:
            zoom_out()
        elif 'open whatsapp' in command:
            open_whatsapp()
        elif 'open settings' in command or 'settings' in command:
            open_whatsapp_settings()
        elif 'type message' in command:
            type_message()
        elif 'open status' in command or 'status' in command:
            open_whatsapp_status()
        elif 'open calls' in command or 'calls' in command:
            open_whatsapp_calls()
        elif 'exit' in command or 'quit' in command:
            sys.exit()
        else:
            print("Command not recognized. Try again.")

    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def zoom_in():
    pyautogui.keyDown('ctrl')
    pyautogui.press('=')
    pyautogui.keyUp('ctrl')

def zoom_out():
    pyautogui.keyDown('ctrl')
    pyautogui.press('-')
    pyautogui.keyUp('ctrl')

def open_whatsapp():
    pyautogui.click(600, 1046)  # Replace coordinates with your Start Menu button position
    time.sleep(1)
    pyautogui.write("WhatsApp")
    time.sleep(1)
    pyautogui.press('enter')

def open_whatsapp_settings():
    settings_icon_position = (230, 900)  # Example coordinates of the settings icon
    pyautogui.click(settings_icon_position)
    time.sleep(2)

def type_message():
    print("Please say the message to type.")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio_message = recognizer.listen(source)
        message = recognizer.recognize_google(audio_message)
        print(f"Typed message: {message}")

    time.sleep(3)  # Adjust delay to switch to the desired window

    # Type the recognized message into the active window
    pyautogui.write(message)
    pyautogui.press('enter')

def open_whatsapp_status():
    status_icon_position = (230, 180)  # Example coordinates of the status icon
    pyautogui.click(status_icon_position)
    time.sleep(2)

def open_whatsapp_calls():
    calls_icon_position = (230, 170)  # Example coordinates of the calls icon
    pyautogui.click(calls_icon_position)
    time.sleep(2)

def click_on_screen(x, y):
    pyautogui.click(x, y)

def pause_video():
    keyboard.press_and_release('k')  # Press the 'k' key to pause

def resume_video():
    keyboard.press_and_release('k')  # Press the 'k' key again to resume

def skip_forward():
    pyautogui.press("l")  # Simulate pressing the 'l' key to skip forward by 10 seconds

def skip_backward():
    pyautogui.press("j")  # Simulate pressing the 'j' key to skip backward by 10 seconds

def scroll_up():
    pyautogui.scroll(50)  # You can adjust the scroll amount as needed

def scroll_down():
    pyautogui.scroll(-50)  # You can adjust the scroll amount as needed

if __name__ == "__main__":
    print("Voice command activated...")
    while True:
        voice_command()
