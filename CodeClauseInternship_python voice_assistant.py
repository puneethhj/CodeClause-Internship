import tkinter as tk
import speech_recognition as sr
import pyttsx3
import threading

class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("400x300")

        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets."""
        self.label = tk.Label(self.root, text="Click the button and speak a command", wraplength=300)
        self.label.pack(pady=20)

        self.button = tk.Button(self.root, text="Speak", command=self.start_listening)
        self.button.pack(pady=20)

        self.result_label = tk.Label(self.root, text="", wraplength=300)
        self.result_label.pack(pady=20)

    def start_listening(self):
        """Start a new thread to listen for a voice command."""
        self.result_label.config(text="Listening...")
        threading.Thread(target=self.listen_command).start()

    def listen_command(self):
        """Listen for a voice command and process it."""
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio)
                self.display_command(command)
                self.respond(command)
            except sr.UnknownValueError:
                self.display_command("Sorry, I could not understand what you said.")
            except sr.RequestError:
                self.display_command("Sorry, my speech service is down.")

    def display_command(self, command):
        """Display the interpreted command on the GUI."""
        self.result_label.config(text=f"Command: {command}")

    def respond(self, command):
        """Respond to the command with relevant information or feedback."""
        response = self.process_command(command)
        self.tts_engine.say(response)
        self.tts_engine.runAndWait()
        self.result_label.config(text=f"Command: {command}\nResponse: {response}")

    def process_command(self, command):
        """Process the command and return a response."""
        if "weather" in command.lower():
            return "I can't provide weather updates right now."
        elif "time" in command.lower():
            from datetime import datetime
            return f"The current time is {datetime.now().strftime('%H:%M')}."
        elif "your name" in command.lower():
            return "I am your voice assistant."
        else:
            return "I don't know how to respond to that."

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistant(root)
    root.mainloop()
