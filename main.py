import datetime
import time
import webbrowser
import pywhatkit
import pyttsx3 #!pip install pyttsx3
import speech_recognition as sr

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



if __name__ == "__main__":
    wishMe()
    
    while True:
        # query = command().lower()
        query =input("Enter your command -> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif 'play' in query and 'youtube' in query:
            play_youtube_video(query)
        elif any(phrase in query for phrase in ["university timetable", "schedule", "today's plan", "daily routine", "what's the schedule", "what's my plan","today's schedule", "things to do today", "my plans for today"]):
            schedule()

    
    
# speak("Hello,I'm Friday")