import datetime,calendar
import webbrowser
import wikipedia
import speech_recognition as sr
import pyttsx3
import os
import pickle
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import calendar_event as ce
count=0
engine = pyttsx3.init('sapi5')  # sapi5 is microsoft speech API
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[len(voices)-1].id)  # setting voice to engine either voices[0] or [1].

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning, Sir!")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon, Sir!")
    else:
        speak("good evening, sir!")
    speak("How may i help you")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 350
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio,language='en-in')
        print('You said : {}\n'.format(query))
    except:
        speak("Sorry coud not recognize your voice, Say that again please!")
        return "None"
    print("Listened Your Command")
    return query

def remove_stopwords(query):

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(query)
    not_require = ["I","He","She","This","That","Would","would","like","please"]
    filtered_sentence = [i for i in word_tokens if not i in not_require]
    filtered_sentences = [w for w in filtered_sentence if not w in stop_words]
    return filtered_sentences

if __name__ == '__main__':
    wishme()
    while(1):
        query = take_command().lower()

        if "wikipedia" in query:
            speak("Searching Wikipdia...")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")
        elif "open google" in query:
            webbrowser.open("google.com")
        elif "open stackoverflow" in query:
            webbrowser.open("stackoverflow.com")
        
        elif "search" in query:
            query = query.replace("hello jarvis can you","")
            query = query.replace("search","")
            if "for me" in query:
                query = query.replace("for me","")

            url = "https://www.google.co.in/search?q=" +query+ "&oq="+query+"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
            webbrowser.open_new(url)
        
        elif "play movie" in query:
            
            speak("Which movie you like to watch, from available ones")
            q= take_command().lower()
            video_dir = r"C:\Users\Asus\Downloads\Video"
            video_list = os.listdir(video_dir)
            query_list = remove_stopwords(q)
            print(query_list)
            for j in query_list:
                for i in video_list:
                    if i.lower().find(j)>=0:
                        count+=1
                        print("i am in")
                        os.startfile(os.path.join(video_dir,i))
                        break
                    else:
                        continue
            if count==0:
                speak("Sorry Sir, Video not found!")


        elif "the time" in query:
            hour = int(datetime.datetime.now().hour)
            time = datetime.datetime.now().strftime("%I:%M:%S")   # strftime("%I:%M:%S") is for formatting the time. %I is use for 12-hour format and %H is for 24 hour format.
            if hour>=12:
                speak(f"Sir,the time is {time}PM")
            else:
                speak(f"Sir,the time is {time}AM")
        elif "the date" in query:
            date = datetime.date.today()
            speak(str(date))

        elif "set" in query and "event" in query:
            
            speak("Sure Sir! What's the title of the event?")
            summary = take_command().lower()
            while(1):
                speak("Ok! When is the event?")
                start_date_str = take_command().lower()

                if int(datetime.datetime.strftime(list(ce.datefinder.find_dates(start_date_str))[0],"%H%S"))==0:    # this is done for checking if the previous command contains time as well or not        
                    speak("What's the time of the event?")
                    start_time_string = take_command().lower()
                    start_time_str = start_date_str+start_time_string
                else:
                    start_time_str=start_date_str
                
                catch_event = ce.create_event(start_time_str,summary,duration=1)
                if catch_event != 'None':
                    speak("Alright! the respected event has been added to the Google calendar, you will be notify by an email before 24 hours")
                    break
                else:
                    speak("Sorry, couldn't recognize date and time correctly..")
                    continue
        
        elif "show" in query and "event" in query:
            events_lst = ce.get_event()
            if len(events_lst)==1:
                speak(f"I have found one event...That is..")
                speak(events_lst[0])
            elif len(events_lst) > 1:    
                speak(f"I have found {len(events_lst)} events...The First one is..")
                for i in range(len(events_lst)): 
                    speak(events_lst[i])
                    if i!=(len(events_lst)-1):
                        speak("Next One is.")
            else:
                speak("Sorry, You don't have any event in your calendar.")
        
        elif "update" in query and "event" in query:
            speak("What's the new title sir!")
            summary = take_command().lower()
            ce.update_event(summary)
        
        elif "delete" in query and "event" in query:
            speak("Are you sure you wanna delete all events?")
            clear_str = take_command().lower()
            if "yes" in clear_str or "sure" in clear_str:
                speak("Alright! Deleting..")
                clear_catch = ce.clear_events()
                if len(clear_catch)==0:
                    speak("Events Deleted")
                else:
                    speak("Sorry, Can't delete your events..There Might be some problems in API servers.")
            else:
                speak("Okay! I haven't done that yet.")
        



        if query.find("exit alexa") or query.find("go alexa") or query.find("take rest") or query.find("turn off")== 0:
            break
    print("done")
