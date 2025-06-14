import speech_recognition as sr                  # Recognize speech using your microphone
import pyttsx3                                   # Text to speech conversion
import webbrowser                                # Open a web browser
import os                                        # For file and directory operations
import getpass                                   # To get current username
from datetime import datetime, timedelta         # For handling date and time
import random                                    # For generating random numbers
import threading                                 # For running tasks in parallel
import time                                      # For time-related functions
import playsound                                 # To play sound files
import tkinter as tk                             # GUI for robot animation
from tkvideo import tkvideo                      # Play video in Tkinter label

# MP3 file path for alarm and reminder
MP3_PATH = r"C:\\Users\\LENOVO\\OneDrive\\Desktop\\as\\reminder.mp3"
# Robot video path
ROBOT_VIDEO_PATH = r"C:\\Users\\LENOVO\\OneDrive\\Desktop\\Voice assistant\\Robot.mp4"

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"Suman said: {query}")
        return query.lower()
    except Exception:
        print("Sorry, I did not catch that.")
        return ""


# ------------- Robot Animation -------------

def play_robot_video_anytime():
    """Displays the robot animation in a non‑blocking window for ~5 min."""

    def run_video():
        window = tk.Tk()
        window.title("Chiku the Robot Assistant")
        window.geometry("400x500")
        window.resizable(False, False)

        label = tk.Label(window)
        label.pack()

        player = tkvideo(ROBOT_VIDEO_PATH, label, loop=1, size=(400, 500))
        player.play()

        window.after(300000, window.destroy)  # Auto‑close after 5 min
        window.mainloop()

    threading.Thread(target=run_video, daemon=True).start()


# ------------- Alarm & Reminder Threads -------------

def alarm_thread(alarm_time):
    speak(f"Alarm set for {alarm_time.strftime('%H:%M:%S')}")
    while datetime.now() < alarm_time:
        time.sleep(1)
    playsound.playsound(MP3_PATH)
    speak("Alarm time reached. Do you want to snooze for 5 minutes?")
    response = listen()
    if "yes" in response:
        snooze_time = datetime.now() + timedelta(minutes=5)
        speak("Snoozing for 5 minutes.")
        threading.Thread(target=alarm_thread, args=(snooze_time,), daemon=True).start()


def reminder_thread(reminder_time, message):
    speak(f"Reminder set for {reminder_time.strftime('%H:%M:%S')} with message: {message}")
    while datetime.now() < reminder_time:
        time.sleep(1)
    playsound.playsound(MP3_PATH)
    speak(f"Reminder: {message}")


# ------------- Main Assistant Loop -------------

if __name__ == "__main__":
    play_robot_video_anytime()  # Show robot at startup
    speak("Hello! I am your voice assistant. How can I help you?")

    while True:
        command = listen()

        # ---------- Small-talk ----------
        if "hello" in command or "hi" in command:
            play_robot_video_anytime()  # Show robot whenever greeted
            speak("Hi Suman! I'm Chiku 1.0, your personal assistant. How can I help you today?")

        elif "your name" in command or "what is your name" in command:
            speak("I'm Chiku, the voice assistant built just for you, Suman.")
        elif "who are you" in command:
            speak("I’m Chiku version 1.0, your smart and helpful assistant, Suman.")
        elif "what can you do" in command:
            speak("I can open apps, tell jokes, give you the time and date, and answer your questions, Suman.")
        elif "tell me a joke" in command:
            speak("Why did the computer go to therapy? It had too many bytes of trauma!")
        elif "tell me about yourself" in command:
            speak("I'm Chiku, a voice‑driven assistant powered by Python. I may be code, but I’ve got a heart for helping you, Suman!")
        elif "help" in command:
            speak("Just say commands like 'open YouTube', 'what's the time', or 'play music'. I'm here to assist you, Suman.")
        elif "tell me a story" in command:
            speak("Once upon a time, Suman created a voice assistant named Chiku... and together, they conquered the digital world!")
        elif "thanks" in command:
            speak("Always a pleasure, Suman! Let me know if you need anything else.")

        # ---------- Utility Commands ----------
        elif "play music" in command:
            speak("Playing your favorite song on Spotify, Suman.")
            webbrowser.open("https://open.spotify.com/track/2TYxwTH2HhL6OLVkZlsDLV?si=421621d29d64465a")

        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "open whatsapp" in command:
            speak("Opening WhatsApp.")
            try:
                username = getpass.getuser()
                whatsapp_path = f"C:\\Users\\{username}\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
                os.startfile(whatsapp_path)
            except Exception:
                speak("WhatsApp Desktop not found. Opening WhatsApp Web.")
                webbrowser.open("https://web.whatsapp.com")

        elif "open website" in command:
            speak("Please tell me the name of the website you want to open.")

        elif "search" in command:
            speak("What would you like to search for?")

        elif "what time is it" in command:
            current_time = datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}.")

        elif "what is the date" in command:
            current_date = datetime.now().strftime("%Y-%m-%d")
            speak(f"Today's date is {current_date}.")

        elif "current weather" in command:
            speak("Here’s the current weather in your location, Suman.")
            webbrowser.open("https://www.google.com/search?q=current+weather+in+my+location")

        elif "set alarm" in command:
            speak("Please say the time for the alarm in HH:MM:SS format.")
            alarm_input = listen()
            try:
                alarm_time = datetime.strptime(alarm_input, "%H:%M:%S")
                now = datetime.now()
                alarm_time = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=alarm_time.second, microsecond=0)
                if alarm_time < now:
                    alarm_time += timedelta(days=1)
                threading.Thread(target=alarm_thread, args=(alarm_time,), daemon=True).start()
            except ValueError:
                speak("Sorry, I couldn't understand the time format.")

        elif "reminder" in command:
            speak("What would you like to be reminded about?")
            reminder_message = listen()
            speak("At what time should I remind you? Please say it in HH:MM:SS format.")
            reminder_time_input = listen()
            try:
                reminder_time = datetime.strptime(reminder_time_input, "%H:%M:%S")
                now = datetime.now()
                reminder_time = now.replace(hour=reminder_time.hour, minute=reminder_time.minute, second=reminder_time.second, microsecond=0)
                if reminder_time < now:
                    reminder_time += timedelta(days=1)
                threading.Thread(target=reminder_thread, args=(reminder_time, reminder_message), daemon=True).start()
            except ValueError:
                speak("Sorry, I couldn't understand the time format.")

        # ---------- Exit ----------
        elif "goodbye" in command or "bye" in command or "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day, Suman!")
            break

        # ---------- Fallback ----------
        elif command:
            speak("You said: " + command)
