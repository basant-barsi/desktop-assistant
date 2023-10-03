import speech_recognition as sr
import os
import webbrowser
import win32com.client
import response
import openai
import requests
from config import apikey
import datetime


speaker = win32com.client.Dispatch("SAPI.SPvoice")
"""while 1:
    print("enter the word you want to speak it out by computer")
    s=input()
    speaker.Speak(s)"""

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from shakti"

'''def get_chatgpt_response(query):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": query,
        "max_tokens": 50  # Adjust this as needed for the desired response length
    }

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "ChatGPT encountered an error."'''

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')


if __name__ ==  '__main__':
    print("Welcome to Shakti Ai ")
    speaker.Speak("Shakti A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        speaker.Speak(query)
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
         # todo: Add a feature to play a specific song
        if "open music" in query:
            musicURL = "https://www.jiosaavn.com/"
            webbrowser.open(musicURL)

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speaker.Speak(f"Sir time is {hour} and {min} minutes")

        elif "open facetime".lower() in query.lower():
            facetimeURL=("https://support.apple.com/en-in/HT204380")
            webbrowser.open(facetimeURL)

        elif "artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Shakti Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
