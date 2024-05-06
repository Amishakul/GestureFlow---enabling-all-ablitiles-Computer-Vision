import os
import subprocess
import speech_recognition as sr
import time
import pyttsx3
import pyautogui
import win32com.client
import win32clipboard

def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
        print("Notepad opened successfully.")
        return True
    except Exception as e:
        print(f"Error opening Notepad: {e}")
        return False

def type_text_with_spaces(text):
    try:
        words = text.split()
        for word in words:
            word += ' '  # Add a space after each word
            subprocess.Popen(['powershell', f'$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys("{word}")'])
            time.sleep(0.1)  # Adjust the sleep time if needed
        print(f"Typed text with spaces: {text}")
        return True
    except Exception as e:
        print(f"Error typing text with spaces: {e}")
        return False

def paste_text():
    try:
        subprocess.Popen(['powershell', '$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys("^(v)")'])
        print("Text pasted successfully.")
        return True
    except Exception as e:
        print(f"Error pasting text: {e}")
        return False

def save_notepad(filename):
    try:
        pyautogui.hotkey("ctrl", "s")  # Open Save dialog using pyautogui
        time.sleep(1)

        pyautogui.write(filename)  # Type filename using pyautogui
        pyautogui.press("enter")
        time.sleep(1)

        pyautogui.hotkey("ctrl", "s")  # Open Save dialog again to focus on it
        time.sleep(1)

        print("Notepad document saved.")
        return True
    except Exception as e:
        print(f"Error saving Notepad document: {e}")
        return False

def print_notepad():
    try:
        pyautogui.hotkey("ctrl", "p")  # Press Ctrl+P to open the print dialog
        time.sleep(1)

        # This is a placeholder; you may need to adjust the code depending on your Notepad version
        pyautogui.press("enter")  # Press Enter to perform the print action
        print("Notepad print dialog opened.")
        time.sleep(1)

        # Assuming the "Print" button is the 7th tab after opening the print dialog
        for _ in range(6):  # Press Tab 6 times to reach the 9th tab
            pyautogui.press("tab")

        pyautogui.press("enter")  # Press Enter to click the "Print" button
        print("Notepad document printed.")

        return True
    except Exception as e:
        print(f"Error printing Notepad document: {e}")
        return False

def move_to_new_line():
    try:
        pyautogui.press("enter")  # Press Enter to move to a new line in Notepad
        print("Cursor moved to a new line.")
        return True
    except Exception as e:
        print(f"Error moving cursor to a new line: {e}")
        return False

def exit_notepad():
    try:
        pyautogui.hotkey("alt", "f4")  # Close Notepad using Alt+F4
        print("Notepad closed successfully.")
        return True
    except Exception as e:
        print(f"Error closing Notepad: {e}")
        return False

def open_microsoft_word():
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = True  # Make Word visible
        print("Microsoft Word opened successfully.")
        return word
    except Exception as e:
        print(f"Error opening Microsoft Word: {e}")
        return None

def create_blank_document(word):
    try:
        document = word.Documents.Add()
        print("Blank document created successfully.")
        return document
    except Exception as e:
        print(f"Error creating a blank document: {e}")
        return None

def save_document(document, filename, file_destination):
    try:
        full_path = fr"{file_destination}\{filename}.docx"
        document.SaveAs2(full_path)
        print(f"Document saved as: {full_path}")
        return True
    except Exception as e:
        print(f"Error saving document: {e}")
        return False

def close_microsoft_word(word):
    try:
        word.Quit()
        print("Microsoft Word closed successfully.")
        return True
    except Exception as e:
        print(f"Error closing Microsoft Word: {e}")
        return False

def print_document(word):
    try:
        word.ActiveDocument.PrintOut()
        print("Document printed successfully.")
        return True
    except Exception as e:
        print(f"Error printing document: {e}")
        return False

def type_paragraph(word, text, new_line=False, bold=False, font_size=None, italic=False, underline=False, font_style=None, alignment=None):
    try:
        if new_line:
            word.Selection.MoveDown()
            word.Selection.TypeParagraph()

        words = text.split()
        for word_text in words:
            word_text += ' '  # Add a space after each word
            word.Selection.TypeText(word_text)

        if bold:
            word.Selection.WholeStory()
            word.Selection.Font.Bold = True

        if font_size:
            word.Selection.WholeStory()
            word.Selection.Font.Size = font_size

        if italic:
            word.Selection.WholeStory()
            word.Selection.Font.Italic = True

        if underline:
            word.Selection.WholeStory()
            word.Selection.Font.Underline = True

        if font_style:
            word.Selection.WholeStory()
            word.Selection.Font.Name = font_style

        if alignment:
            alignment_lower = alignment.lower()
            print(f"Recognized alignment: {alignment_lower}")
            if alignment_lower == "left":
                word.Selection.ParagraphFormat.Alignment = 0  # Left
            elif alignment_lower == "right":
                word.Selection.ParagraphFormat.Alignment = 2  # Right
            elif alignment_lower in ["center", "centre"]:
                word.Selection.ParagraphFormat.Alignment = 1  # Center
            elif alignment_lower == "justify":
                word.Selection.ParagraphFormat.Alignment = 3  # Justify
            else:
                print(f"Invalid alignment: {alignment_lower}")

            # Add this line to ensure the alignment is applied immediately
            word.Selection.Collapse()

        print(f"Typed paragraph: {text}")
        return True

    except Exception as e:
        print(f"Error typing paragraph: {e}")
        return False

def paste_content(word):
    try:
        # Get content from clipboard
        win32clipboard.OpenClipboard()
        content = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        # Paste content into Word
        word.Selection.Paste()
        print("Content pasted successfully.")
        return True
    except Exception as e:
        print(f"Error pasting content: {e}")
        return False

def get_filename():
    speak("Listening for filename...")
    return speech_to_text()

def get_file_destination():
    speak("Listening for file destination...")
    file_destination = speech_to_text()

    if file_destination is None:
        return fr"C:\Users\91913\Dropbox\PC\Downloads"  # Replace 'YourUsername' with your actual Windows username

    if "downloads" in file_destination.lower():
        return fr"C:\Users\91913\Dropbox\PC\Downloads"
    elif "desktop" in file_destination.lower():
        return fr"C:\Users\91913\Dropbox\PC\\Desktop"

    speak("Destination not recognized. Using default Downloads folder.")
    return fr"C:\Users\91913\Dropbox\PC\Downloads"

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command: {command}")
        return command
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def exit_word(word):
    if word.ActiveDocument.Saved:
        if close_microsoft_word(word):
            speak("Microsoft Word closed successfully. Exiting...")
            return True
        else:
            speak("Error closing Microsoft Word. Exiting...")
            return False
    else:
        speak("Document not saved. Saving with an unknown name...")
        filename = "Unknown_Document"
        destination = get_file_destination()
        if save_document(word.ActiveDocument, filename, destination):
            speak("Document saved successfully.")
        else:
            speak("Error saving document.")
        if close_microsoft_word(word):
            speak("Microsoft Word closed successfully. Exiting...")
            return True
        else:
            speak("Error closing Microsoft Word. Exiting...")
            return False

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        voice_command = speech_to_text()

        if voice_command == "open notepad":
            if open_notepad():
                speak("Notepad opened successfully.")
                time.sleep(2)

                while True:
                    additional_command = speech_to_text()

                    if additional_command is not None:
                        if additional_command == "type paragraph":
                            speak("Type what you want to type in Notepad.")
                            text_to_type = speech_to_text()
                            type_text_with_spaces(text_to_type)
                            speak("Text typed successfully.")
                        elif additional_command == "paste":
                            paste_text()
                            speak("Text pasted successfully.")
                        elif additional_command == "save document":
                            speak("Please specify the filename.")
                            filename = get_filename()
                            if filename:
                                save_notepad(filename)
                                speak("Notepad document saved.")
                        elif additional_command == "print document":
                            print_notepad()
                            speak("Document is printed successfully")
                        elif additional_command == "move to new line":
                            move_to_new_line()
                            speak("Cursor moved to a new line.")
                        elif additional_command == "exit":
                            if exit_notepad():
                                speak("Notepad closed successfully.")
                                break
                        else:
                            speak("Command not recognized. Please try again.")
            else:
                speak("Error opening Notepad. Please try again.")
        elif voice_command == "open word":
            word_app = open_microsoft_word()
            if word_app:
                speak("Microsoft Word opened successfully.")
                time.sleep(2)

                while True:
                    additional_command = speech_to_text()

                    if additional_command is not None:
                        if additional_command == "create blank document":
                            create_blank_document(word_app)
                            speak("Blank document created successfully.")
                        elif additional_command == "type paragraph":
                            paragraph_text = speech_to_text()
                            type_paragraph(word_app, paragraph_text)
                            speak("Paragraph typed successfully.")
                        elif additional_command.startswith("increase font size to"):
                            try:
                                font_size = int(additional_command.split()[-1])
                                type_paragraph(word_app, "", font_size=font_size)
                                speak(f"Font size increased to {font_size}.")
                            except ValueError:
                                speak("Invalid font size. Please specify a number.")
                        elif additional_command == "type bold paragraph":
                            paragraph_text = speech_to_text()
                            type_paragraph(word_app, paragraph_text, bold=True)
                            speak("Bold paragraph typed successfully.")
                        elif additional_command == "type italic paragraph":
                            paragraph_text = speech_to_text()
                            type_paragraph(word_app, paragraph_text, italic=True)
                            speak("Italic paragraph typed successfully.")
                        elif additional_command == "type underline paragraph":
                            paragraph_text = speech_to_text()
                            type_paragraph(word_app, paragraph_text, underline=True)
                            speak("Underline paragraph typed successfully.")
                        elif additional_command == "paste":
                            if paste_content(word_app):
                                speak("Content pasted successfully.")
                            else:
                                speak("Error pasting content.")
                        elif additional_command.startswith("align"):
                            alignment = additional_command.split()[-1]
                            type_paragraph(word_app, "", alignment=alignment)
                            speak(f"Text aligned to {alignment}.")
                        elif additional_command == "move to new line":
                            type_paragraph(word_app, "", new_line=True)
                            speak("Moved to a new line.")
                        elif additional_command == "save document":
                            filename = get_filename()
                            if filename:
                                destination = get_file_destination()
                                if save_document(word_app.ActiveDocument, filename, destination):
                                    speak("Document saved successfully.")
                                else:
                                    speak("Error saving document.")
                        elif additional_command == "print":
                            if print_document(word_app):
                                speak("Document printed successfully.")
                            else:
                                speak("Error printing document.")
                        elif additional_command.startswith("change font style"):
                            speak("Please specify the font style.")
                            font_style = speech_to_text()
                            type_paragraph(word_app, "", font_style=font_style)
                            speak(f"Font style changed to {font_style}.")
                        elif additional_command == "exit":
                            if exit_word(word_app):
                                break
                        else:
                            speak("Command not recognized. Please try again.")
            else:
                speak("Error opening Word. Please try again.")
        elif voice_command == "exit":
            speak("Exiting...")
            break
        else:
            speak("Command not recognized. Please try again.")
