import datetime
import sys
import time
import webbrowser
import pywhatkit
import pyautogui
import pyttsx3 #!pip install pyttsx3
import speech_recognition as sr
import os
import re
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)


def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()
    
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query


def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning Ahmad, it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon Ahmad, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Ahmad, it's {day} and the time is {t}")
        
        
def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")
        
        

def play_youtube_video(command):
    try:
        query = command.replace("play", "").strip()
        speak(f"Playing {query}")
        pywhatkit.playonyt(query)
    except Exception as e:
        speak("Sorry, I couldn't play that video.")
        
        
def schedule():
    day = cal_day().lower()
    speak("Boss, here’s your personalized home study schedule for today.")

    week = {
        "monday": "Morning (9:00 - 11:00): ML/AI Course Study\nLate Morning (11:30 - 1:00): Project Development (JARVIS / Capstone)\nAfternoon (2:00 - 4:00): Coding Practice (DSA or LeetCode)\nEvening (5:00 - 6:30): Light Reading or UI Design Work\nNight (8:00 - 9:00): Recap and Plan for Tomorrow.",
        
        "tuesday": "Morning: Deep Work on AI/ML Concepts\nLate Morning: Work on Portfolio / GitHub Push\nAfternoon: Watch 1-2 YouTube Tech Talks or Lectures\nEvening: Practice Python or Java Problems\nNight: Quick Journal + Light Meditation.",
        
        "wednesday": "Morning: Read Research Papers / Articles\nLate Morning: Implement small AI project module\nAfternoon: Take mock interviews or contests\nEvening: UI/UX Design (Figma or React UI polish)\nNight: Free time or anime break!",
        
        "thursday": "Morning: Explore new tools/libraries (e.g., LangChain, PyTorch)\nLate Morning: Work on personal assistant features (JARVIS upgrades)\nAfternoon: Resume polishing / LinkedIn updates\nEvening: Code review or open source contribution\nNight: Plan weekend learning goals.",
        
        "friday": "Morning: Revise the week's topics\nLate Morning: Build or polish a side project\nAfternoon: UI/UX improvements or blog writing\nEvening: Chill session – music or gaming\nNight: Reflect and set weekend priorities.",
        
        "saturday": "Morning: Capstone or main project focus\nLate Morning: Attend webinars or courses\nAfternoon: Design + Code sprint (no distractions)\nEvening: Review Git commits and update Trello/Notion\nNight: Watch AI documentaries or inspiration videos.",
        
        "sunday": "Boss, today is recharge day 🧘‍♂️\nSleep well, eat well, relax.\nLight review if you want: Read or revise topics casually.\nPlan the upcoming week and do what brings you joy!"
    }

    if day in week:
        speak(week[day])
    else:
        speak("Boss, schedule unavailable. Maybe time-travel messed with the calendar!")
        
def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return interface.QueryInterface(IAudioEndpointVolume)

def get_current_volume_percent():
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    return int(current * 100)

def set_volume(percent):
    percent = max(0, min(100, percent))  # Clamp between 0–100
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
    speak(f"Volume set to {percent} percent")

def increase_volume(step=10):
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current + step / 100.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak(f"Volume increased to {int(new_volume * 100)} percent")

def decrease_volume(step=10):
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current - step / 100.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak(f"Volume decreased to {int(new_volume * 100)} percent")

def mute_volume():
    volume = get_volume_interface()
    volume.SetMute(1, None)
    speak("Volume muted")

def unmute_volume():
    volume = get_volume_interface()
    volume.SetMute(0, None)
    speak("Volume unmuted")

def process_volume_command(query):
    query = query.lower()
    
    if "mute" in query and "unmute" not in query:
        mute_volume()
    elif "unmute" in query:
        unmute_volume()
    elif "increase volume" in query or "volume up" in query:
        increase_volume()
    elif "decrease volume" in query or "volume down" in query:
        decrease_volume()
    elif "current volume" in query or "what's the volume" in query:
        current = get_current_volume_percent()
        speak(f"Current volume is {current} percent")
    elif "set volume to" in query:
        match = re.search(r"set volume to (\d+)", query)
        if match:
            vol = int(match.group(1))
            if 0 <= vol <= 100:
                set_volume(vol)
            else:
                speak("Please provide a volume between 0 and 100")
        else:
            speak("I didn't catch the volume level. Try saying: set volume to 50")
    else:
        speak("Please say a valid volume command like 'set volume to 70' or 'mute volume'")
        

apps = {
    "calculator": {
        "path": "C:\\Windows\\System32\\calc.exe",
        "process": "calc.exe"
    },
    "notepad": {
        "path": "C:\\Windows\\System32\\notepad.exe",
        "process": "notepad.exe"
    },
    "paint": {
        "path": "C:\\Windows\\System32\\mspaint.exe",
        "process": "mspaint.exe"
    }
}

def openApp(command):
    for app in apps:
        if f"open {app}" in command:
            speak(f"Opening {app}")
            os.startfile(apps[app]["path"])
            return
    speak("Application not recognized to open.")

def closeApp(command):
    for app in apps:
        if f"close {app}" in command:
            speak(f"Closing {app}")
            os.system(f'taskkill /f /im {apps[app]["process"]}')
            return
    speak("Application not recognized to close.")



if __name__ == "__main__":
    # wishMe()
    
    while True:
        # query = command().lower()
        query =input("Enter your command -> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif 'play' in query and 'youtube' in query:
            play_youtube_video(query)
        elif any(phrase in query for phrase in ["university timetable", "schedule", "today's plan", "daily routine", "what's the schedule", "what's my plan","today's schedule", "things to do today", "my plans for today"]):
            schedule()
        elif any(kw in query for kw in ["volume", "sound", "mute", "unmute"]):
            process_volume_command(query)
        elif any(f"open {app}" in query for app in apps):
            openApp(query)
        elif any(f"close {app}" in query for app in apps):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        speak(np.random.choice(i['responses']))
        elif "exit" in query:
            sys.exit()


    
    
# speak("Hello,I'm Friday")