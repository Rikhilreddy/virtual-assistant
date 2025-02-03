import speech_recognition as sr
import pyttsx3
import pandas as pd
import wikipedia
import webbrowser

def speak(text):
    """Convert text to speech (audio response)."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust the speech speed
    engine.setProperty('volume', 1)  # Set the volume level (1 is the max)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for user input and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (Say 'stop' to exit)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Audio captured")
    
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        speak("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError:
        print("Could not request results. Check your internet.")
        speak("Could not request results. Check your internet.")
        return None

def load_responses(filename):
    """Load responses from a CSV file into a dictionary."""
    try:
        df = pd.read_csv('rules.csv')
        if df.empty or 'Prompt' not in df.columns or 'Response' not in df.columns:
            raise ValueError("CSV file is empty or missing required columns.")
        return dict(zip(df['Prompt'].str.lower(), df['Response']))
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        speak(f"Error: The file {filename} was not found.")
        return {}
    except ValueError as e:
        print(f"Error: {e}")
        speak(f"Error: {e}")
        return {}



def search_wikipedia(query):
    """Search Wikipedia for a summary of the query."""
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:3]}... Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find anything on Wikipedia for that."

def search_google(query):
    """Search Google using the web browser."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return "I have opened a Google search for you."

def main():
    """Main loop to listen and respond with predefined answers."""
    responses = load_responses("./rules.csv")
    speak("Hello, I am your virtual assistant. How can I help you today?")
    
    while True:
        command = listen()
        if command:
            if "stop" in command:
                speak("Goodbye!")
                print("Goodbye!")
                break
            elif "search wikipedia for" in command:
                query = command.replace("search wikipedia for", "").strip()
                response = search_wikipedia(query)
            elif "search google for" in command:
                query = command.replace("search google for", "").strip()
                response = search_google(query)
            else:
                response = responses.get(command, "I'm sorry, I don't have a response for that.")
            
            print(f"AI says: {response}")
            speak(response)

if __name__ == "__main__":
    main()
