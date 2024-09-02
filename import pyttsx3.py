import pyttsx3
import speech_recognition as sr

def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """Listen for a voice command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        command = None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        command = None
    return command

def jarvis():
    """Main function to run Jarvis."""
    speak("Hello SIR, I am Jarvis. How can I assist you today?")
    command = listen_command()
    if command:
        if "hello" in command.lower():
            speak("Hello! How can I help you?")
        elif "how are you" in command.lower():
            speak("I am just a program, but I am functioning as expected.")
        elif "what is your name" in command.lower():
            speak("I am Jarvis, your personal assistant.")
        else:
            speak("Sorry, I don't understand that command.")

if __name__ == "__main__":
    jarvis()
