import pyttsx3
import speech_recognition as sr
import os
import requests
from datetime import datetime
import webbrowser
import tkinter as tk
import threading
import time
from tkinter import Canvas

# Replace with your Gemini API Key or set as environment variable
gemini_api_key = os.getenv("YOUR_GEMINI_API_KEY")

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis - Voice Assistant")
        self.root.geometry("600x600")
        self.root.configure(bg="black")

        self.canvas = Canvas(self.root, width=300, height=300, bg="black", highlightthickness=0)
        self.canvas.pack(pady=30)

        self.gradient_circle = self.canvas.create_oval(50, 50, 250, 250, fill="#0ff", outline="")

        self.subtitle = tk.Label(self.root, text="Hello! How can I help you?", fg="#00ccff", bg="black", font=("Helvetica", 18))
        self.subtitle.pack(pady=20)

        self.pulse = False
        self.animate_ball()

    def update_subtitle(self, text):
        self.subtitle.config(text=text)

    def start_pulse(self):
        self.pulse = True

    def stop_pulse(self):
        self.pulse = False

    def animate_ball(self):
        size = 0
        direction = 1
        colors = ["#00f0ff", "#00ffff", "#66b3ff", "#9999ff", "#cc66ff", "#ff66cc", "#ff9966"]

        def pulse_loop():
            nonlocal size, direction
            color_index = 0
            while True:
                if self.pulse:
                    size += direction
                    if size > 10 or size < 0:
                        direction *= -1
                        color_index = (color_index + 1) % len(colors)

                    self.canvas.coords(self.gradient_circle, 50 - size, 50 - size, 250 + size, 250 + size)
                    self.canvas.itemconfig(self.gradient_circle, fill=colors[color_index])
                time.sleep(0.05)

        threading.Thread(target=pulse_loop, daemon=True).start()

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 0.9)

def speak(text, gui=None):
    if gui:
        gui.update_subtitle(text)
        gui.start_pulse()
    engine.say(text)
    engine.runAndWait()
    if gui:
        gui.stop_pulse()
        gui.update_subtitle("Listening...")

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I did not catch that.")
    except sr.RequestError:
        speak("Could not connect to Google services.")
    return None

def get_gemini_data(endpoint):
    url = f"https://api.gemini.com/v1/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gemini_api_key}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print("Error:", err)
        speak("Sorry, I encountered a problem fetching the data.")
    return None

def run_jarvis(gui):
    speak("Hello sir, I am Jarvis, your personal assistant. How can I assist you today?", gui)

    while True:
        command = listen_command()
        if not command:
            continue

        command = command.lower()

        if "hello" in command:
            speak("Hello! How can I help you?", gui)
        elif "how are you" in command:
            speak("I am functioning as expected.", gui)
        elif "your name" in command:
            speak("I am Jarvis, your assistant.", gui)
        elif "time" in command:
            speak(datetime.now().strftime("The time is %I:%M %p"), gui)
        elif "date" in command:
            speak(datetime.now().strftime("Today's date is %B %d, %Y"), gui)
        elif "who made you" in command:
            speak("Kabir created me.", gui)
        elif "thank you" in command:
            speak("You're welcome!", gui)
        elif "google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google.", gui)
        elif "youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.", gui)
        elif "music" in command:
            os.startfile("C:\\Path\\To\\Your\\Music.mp3")
            speak("Playing music.", gui)
        elif "bitcoin price" in command or "price of bitcoin" in command:
            speak("Let me check the latest price.", gui)
            data = get_gemini_data("pubticker/btcusd")
            if data:
                price = data.get("last", "Unknown")
                speak(f"Bitcoin price is {price} dollars.", gui)
            else:
                speak("Unable to fetch price.", gui)
        elif "shutdown" in command:
            speak("Shutting down.", gui)
            os.system("shutdown /s /t 1")
        elif "restart" in command:
            speak("Restarting.", gui)
            os.system("shutdown /r /t 1")
        elif "lock" in command:
            speak("Locking system.", gui)
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif "calculator" in command:
            os.system("calc")
            speak("Opening calculator.", gui)
        elif "notepad" in command:
            os.system("notepad")
            speak("Opening notepad.", gui)
        elif "paint" in command:
            os.system("mspaint")
            speak("Opening Paint.", gui)
        elif "camera" in command:
            os.system("start microsoft.windows.camera:")
            speak("Opening camera.", gui)
        elif "settings" in command:
            os.system("start ms-settings:")
            speak("Opening settings.", gui)
        elif "control panel" in command:
            os.system("control")
            speak("Opening control panel.", gui)
        elif "capital of india" in command:
            speak("The capital of India is New Delhi.", gui)
        elif "repeat after me" in command:
            phrase = command.replace("repeat after me", "").strip()
            speak(phrase, gui)
        elif "what is ai" in command:
            speak("Artificial intelligence is machine intelligence.", gui)
        elif "fun fact" in command:
            speak("Did you know honey never spoils?", gui)
        elif "tell me a joke" in command:
            speak("Why did the computer sneeze? It had a virus!", gui)
        elif "good morning" in command:
            speak("Good morning!", gui)
        elif "good night" in command:
            speak("Good night, sweet dreams!", gui)
        elif "i love you" in command:
            speak("That's kind! I appreciate it.", gui)
        elif "do you love me" in command:
            speak("As a friend, yes!", gui)
        elif "open whatsapp" in command:
            webbrowser.open("https://web.whatsapp.com")
            speak("Opening WhatsApp Web.", gui)
        elif "facebook" in command:
            webbrowser.open("https://www.facebook.com")
            speak("Opening Facebook.", gui)
        elif "instagram" in command:
            webbrowser.open("https://www.instagram.com")
            speak("Opening Instagram.", gui)
        elif "github" in command:
            webbrowser.open("https://www.github.com")
            speak("Opening GitHub.", gui)
        elif "search" in command:
            query = command.replace("search", "").strip()
            speak(f"Searching for {query}", gui)
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "where is" in command:
            location = command.replace("where is", "").strip()
            speak(f"Showing location of {location}", gui)
            webbrowser.open(f"https://www.google.com/maps/place/{location}")
        elif "weather" in command:
            speak("Please use a weather API to get updates.", gui)
        elif "your purpose" in command:
            speak("To assist you with tasks and make life easier.", gui)
        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye sir. Shutting down.", gui)
            break
        else:
            speak("Sorry, I don't understand that command.", gui)

if __name__ == "__main__":
    root = tk.Tk()
    gui = JarvisGUI(root)
    threading.Thread(target=lambda: run_jarvis(gui), daemon=True).start()
    root.mainloop()
az
