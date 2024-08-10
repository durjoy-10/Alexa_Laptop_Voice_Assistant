import pyttsx3
import speech_recognition as sr
import datetime
from datetime import date
import time
import wikipedia
import webbrowser
import pywhatkit as wk
import os
import random
import cv2
import sys
import pyautogui
import requests
import pyautogui as pi
import re
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


def speak(audio):
    SpeakImage = SPK("speaking.jpeg")
    engine.say(audio)
    engine.runAndWait()
    # Close the speaking 
    SpeakImage.destroy()


def SPK(image_path):
    root = tk.Tk()
    root.title("SPEAKING...")

    window_width = 300
    window_height = 150

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    
    root.geometry("300x150+10+800")

    img = Image.open(image_path)
    img=img.resize((300,150))
    img=ImageTk.PhotoImage(img)
    label = tk.Label(root,image=img)
    label.img=img
    label.pack()
    root.update()

    return root


def takeCommand():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        # print("Listening...")
        time.sleep(1)
        # speak("Listening sir...")
        r.pause_threshold = 1
         # Show the listening picture
        ListeningImage = LSN("listening.jpeg")
        audio = r.listen(source)
        
        # Close the listening GIF window after the command is received
        ListeningImage.destroy()
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        
    except Exception as e:
        print("Say that again please...")
        return "None"
    
    return query


def LSN(image_path):
    root = tk.Tk()
    root.title("LISTENING...")

    window_width = 300
    window_height = 150

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    
    root.geometry("300x150+10+800")

    img = Image.open(image_path)
    img=img.resize((300,150))
    img=ImageTk.PhotoImage(img)
    label = tk.Label(root,image=img)
    label.img=img
    label.pack()
    root.update()

    return root


def wishme():
    hour = int(datetime.datetime.now().hour)
    
    if hour >= 0 and hour < 12:
        speak("Good Morning, Sir")
        
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, Sir")
        
    else:
        speak("Good Evening, Sir")
    speak("Ready for the service. Please tell your password....")
 
 
def password():
    lock_key=takeCommand().lower()
    return lock_key


if __name__ == "__main__":
    
    wishme()
    cap = None  # Initialize cap here to make it accessible globally
    out = None  # Initialize out here to make it accessible globally
    recording = False  # To keep track of recording state
    pas=password()
    
    if(pas=="774789"):
        from intro import play_gif
        play_gif
        speak("Welcome Sir. I am alexa, your voice assistant. How can I help you?")
        
        while True:
            query = takeCommand().lower()
    
            if 'alexa' in query:  #1
                print("YES SIR")
                speak("YES SIR")
             
             
            elif "who are you" in query: #2
                speak("My name is Alexa. I can do everything that my creator programmed me to do.")
                
                
            elif "who created you" in query: #3
                speak("I was created by Durjoy using Python in Visual Studio Code.")
                
                
            elif 'what is' in query or 'who is' in query:#4
                try:
                    speak('Searching Wikipedia...')
                    results = wikipedia.summary(query, sentences=1)
                    speak("According to Wikipedia")
                    speak(results)
                    print(results)
                except Exception as e:
                    speak("Sorry, I couldn't find any results on Wikipedia.")
            
            
            elif 'just open google' in query:#5
                webbrowser.open('https://www.google.com')
            
            
            elif 'open google' in query:#6
                speak("What should I search?")
                qry = takeCommand().lower()
                if qry != "None":
                    webbrowser.open(f"https://www.google.com/search?q={qry}")
            
            
            elif 'just open youtube' in query:#7
                webbrowser.open('https://www.youtube.com')
            
            
            elif 'open youtube' in query:#8
                speak("What would you like to watch?")
                qrry = takeCommand().lower()
                if qrry != "None":
                    wk.playonyt(qrry)
            
            
            elif 'search on youtube' in query:#9
                query = query.replace("search on youtube", "").strip()
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            
            
            elif 'close browser' in query:#10
                os.system("taskkill /f /im msedge.exe")
                
                
            elif 'close chrome' in query:#11
                os.system("taskkill /f /im chrome.exe")
                
                
            elif 'open cmd' in query:#12
                os.system('start cmd')
                
                
            elif 'close cmd' in query:#13
                os.system("taskkill /f /im cmd.exe")
                
                
            elif 'play music' in query:#14
                music_dir = 'E:\\PHONE\\SnapTube Audio'
                
                try:
                    songs = os.listdir(music_dir)
                    if songs:
                        os.startfile(os.path.join(music_dir, random.choice(songs)))
                    else:
                        speak("No songs found in the directory.")
                        
                except Exception as e:
                    speak("Sorry, I couldn't find the music directory.")
                    
                    
            elif 'close music' in query:#15
                os.system("taskkill /f /im vlc.exe")
                
                
            elif 'play video' in query:#16
                video_dir = 'E:\\PHONE\\mp4'
                
                try:
                    videos = os.listdir(video_dir)
                    if videos:
                        os.startfile(os.path.join(video_dir, random.choice(videos)))
                    else:
                        speak("No videos found in the directory.")
                        
                except Exception as e:
                    speak("Sorry, I couldn't find the video directory.")
                    
                    
            elif 'close video' in query:#17
                os.system("taskkill /f /im vlc.exe")
                 
                 
            elif 'favourite folder' in query:#18
                hri_fol = 'E:\\PHONE\\HRIDI'
                os.startfile(hri_fol)
                speak("Which video do you want to watch?")
                qu = takeCommand().lower()
                print(qu)
                video_map = {
                    'favourite one': '1.mp4',
                    'favourite 2': '2.mp4',
                    'favourite 3': '3.mp4',
                    'favourite 4': '4.mp4',
                    'favourite 5': '5.mp4',
                    'favourite 6': '6.mp4',
                    'favourite 7': '7.mp4',
                    'favourite 8': '8.mp4',
                    'favourite 9': '9.mp4',
                    'favourite 10': '10.mp4'
                }
                if qu in video_map:
                    video_path = os.path.join(hri_fol, video_map[qu])
                    os.startfile(video_path)
                else:
                    speak("Sorry, I couldn't find the video.")
            
            
            elif 'time' in query:#19
                strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
                speak(f"Sir, the time is {strTime}")

                 
                 
            elif 'date' in query:#20
                # Get the current date
                current_date = date.today()
                
                # Format the date
                formatted_date = current_date.strftime("%B %d, %Y")
                
                # Print the formatted date
                speak(f"Today's date is:{formatted_date}")
                
                
            elif 'shut down' in query:#21
                os.system('shutdown /s /t 5')
            
            
            elif 'restart' in query:#22
                os.system('shutdown /r /t 5')
            
            
            elif 'lock' in query:#23
                os.system('rundll32.exe user32.dll,LockWorkStation')
               
                
            elif 'start screen recording' in query:#24
                pi.hotkey('win','s')
                pi.typewrite("OBS studio",0.15)
                pi.press('enter')
                time.sleep(2)
                pi.hotkey('ctrl','1')
                time.sleep(2)
                pi.hotkey('win','down')
                speak("screen recording started...")
            
            
            
            elif 'stop screen recording' in query:#25
                time.sleep(1)
                pi.hotkey('ctrl','0')
                os.system("taskkill /f /im obs64.exe")
                speak("screen recording stopped")
                
                
                
            elif 'pause recording' in query: #poz 26
                time.sleep(1)
                pi.hotkey('ctrl','4')
                speak("screen recording paused")
                
                
            elif 'unpause recording' in query: #unpoz 27
                time.sleep(1)
                speak("screen recording unpaused")
                pi.hotkey('ctrl','5')
                
            
            elif "open camera" in query: #28
                if cap is None:
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        speak("Error: Could not open camera.")
                        cap = None
                    else:
                        speak("Camera opened.")      
                else:
                    speak("Camera is already open.")
    
    
    
            elif "capture photo" in query: #29
                if cap is not None:
                    ret, frame = cap.read()
                    if ret:
                        # cv2.imshow('webcam',frame)
                        cv2.imwrite("captured_photo.jpg", frame)
                        speak("Photo captured and saved successfully.")
                    else:
                        speak("Error: Could not read frame from camera.")
                else:
                    speak("Camera is not open.")
            
            
            
            elif "start video recording" in query: #30
                if cap is None:
                    cv2.imshow('webcam',frame)
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        speak("Error: Could not open camera.")
                        cap = None
                    else:
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
                        recording = True
                        speak("Video recording started.")
                else:
                    if not recording:
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
                        recording = True
                        speak("Video recording started.")
                    else:
                        speak("Video recording is already in progress.")
            
            
            
            elif "stop video recording" in query: #31
                if recording:
                    recording = False
                    out.release()
                    speak("Video recording stopped and saved successfully.")
                else:
                    speak("No video recording in progress.")
            
            
            
            elif "close camera" in query: #32
                if cap is not None:
                    cap.release()
                    cap = None
                    if recording:
                        out.release()
                        recording = False
                    speak("Camera closed.")
                    cv2.destroyAllWindows()
                else:
                    speak("Camera is not open.")
                
                
            elif "take a screenshot" in query: #33
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save("ss.png")
                speak("screenshot saved.")
                
                
            elif "ip address" in query: #34
                speak("checking....")
                try:
                    ipadd=requests.get('https//api.ipify.org').text
                    speak("your ip address is:",ipadd)
                    print("your ip address is:",ipadd)
                
                except Exception as e:
                    speak("Network is wear,please try again some time later")
                
                
            elif "volume up" in query: #35
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
            
            
            elif "volume down" in query: #36
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                
                
            elif "mute" in query or "unmute" in query: #37
                pyautogui.press("volumemute")
                
                
            elif "open notepad" in query: #38
                pi.press('win')
                time.sleep(1)
                pi.typewrite('notepad',0.1)
                pi.press('enter')
                time.sleep(2)
                pi.hotkey('ctrl','n')
                speak('Please say what you have to note. I am ready to write')
                tell=takeCommand()
                pi.typewrite(tell,0.1)
                time.sleep(1)
                pi.hotkey('ctrl','s')
                time.sleep(0.5)
                pi.press('enter')
                speak("Your note is saved successfully")
            
            # elif 'open notepad' in query:
            #     npath = 'C:\\Windows\\notepad.exe'
            #     os.startfile(npath)
            
            
            
            elif 'close notepad' in query: #39
                os.system("taskkill /f /im notepad.exe")
            
            
            
            elif "open calendar" in query: #40
                pi.press('win')
                time.sleep(1)
                pi.typewrite('calendar',0.1)
                pi.press('enter')  
                 
                 
            elif "close calendar" in query: #41
                os.system("taskkill /f /im HxCalendarAppImm.exe") 
            
            
            elif "open word" in query: #42
                pi.press('win')
                time.sleep(1)
                pi.typewrite('word',0.1)
                pi.press('enter')  
        
                
            elif 'close word' in query: #43
                os.system("taskkill /f /im winword.exe") 
                 
                 
            elif "open excel" in query: #44
                pi.press('win')
                time.sleep(1)
                pi.typewrite('excel',0.1)
                pi.press('enter')  
                
                
            elif 'close excel' in query: #45
                os.system("taskkill /f /im excel.exe") 
                 
                 
            elif "open powerpoint" in query: #46
                pi.press('win')
                time.sleep(1)
                pi.typewrite('power',0.1)
                pi.press('enter')  
                
                
            elif 'close powerpoint' in query: #47
                os.system("taskkill /f /im powerpnt.exe")  
            
            
            elif "audio call" in query: #48
                qry = query.replace("audio call", "").strip()
                
                if qry=="abir" or qry=="soumi" or qry=="oni" or qry=="didi" or qry=="tubelight" or qry=="tushar" or qry=="shilpy":
                    pi.press('win')
                    time.sleep(2)
                    pi.typewrite('whatsapp',0.1)
                    time.sleep(2)
                    pi.press('enter')
                    time.sleep(5)
                    image_path = 'search.png'  
                    searchImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                    pyautogui.click(searchImage)
                    time.sleep(1)
                    pi.typewrite(qry)
                    time.sleep(2)
                    # pi.press('enter')
                    pi.click(x=201,y=231,clicks=1,interval=0,button="left")
                    time.sleep(1)
                    # pi.click(x=1258,y=227,clicks=1,interval=0,button="left")
                    # time.sleep(1)
                    pi.click(x=1823,y=95,clicks=1,interval=0,button="left")
                else:
                    speak(f"there is no contact of {qry}'s name in whatsapp")
            
            
            
            elif "video call" in query: #49
                qry = query.replace("video call", "").strip()
                
                if qry=="abir" or qry=="soumi" or qry=="oni" or qry=="Didi" or qry=="didi" or qry=="tubelight" or qry=="tushar" or qry=="shilpy":
                    pi.press('win')
                    time.sleep(2)
                    pi.typewrite('whatsapp',0.1)
                    time.sleep(2)
                    pi.press('enter')
                    time.sleep(5)
                    image_path = 'search.png'  
                    searchImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                    pyautogui.click(searchImage)
                    time.sleep(1)
                    pi.typewrite(qry)
                    time.sleep(2)
                    # pi.press('enter')
                    pi.click(x=201,y=231,clicks=1,interval=0,button="left")
                    time.sleep(1)
                    # pi.click(x=1258,y=227,clicks=1,interval=0,button="left")
                    # time.sleep(1)
                    pi.click(x=1767,y=86,clicks=1,interval=0,button="left")
                else:
                    speak(f"there is no contact of {qry}'s name in whatsapp")



            elif "cut the call" in query: #50
                image_path = 'CallEnd.png' 
                searchImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                pyautogui.click(searchImage)
            
            
            elif 'open facebook' in query: #51
                pyautogui.hotkey('win', 's')
                time.sleep(2)
                image_path = 'fb.png' 
                facebookImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)  
                pyautogui.click(facebookImage)
                time.sleep(3)
                
                
            elif 'check notification' in query or 'close notification' in query: #52
                pi.click(x=1796,y=81,clicks=1,interval=0,button="left")
            
            
            elif 'unread notification' in query: #53
                pi.click(x=1561,y=181,clicks=1,interval=0,button="left")
                
                
            elif 'previous notification' in query: #54
                pi.click(x=1632,y=953,clicks=1,interval=0,button="left")
            
            
            elif 'scroll down' in query: #55
                # Move the mouse to the specific coordinates (800, 700)
                pyautogui.moveTo(800, 700, duration=1)
                # Scroll down
                for i in range(0,30):
                    pyautogui.scroll(-20)
                    
                    
            elif 'scroll up' in query: #56
                # Move the mouse to the specific coordinates (800, 700)
                pyautogui.moveTo(800, 700, duration=1)
                # Scroll down
                for i in range(0,30):
                    pyautogui.scroll(20)
    
                     
            elif 'refresh' in query: #57
                pi.hotkey('ctrl','R')
                time.sleep(2)
                
                
            elif 'see story' in query or 'story' in query or 'stories' in query: #58
                pi.click(x=1080,y=960,interval=0,clicks=1,button='left')
                
                
            elif 'back story' in query or 'back' in query or 'back stories' in query: #59
                pi.click(x=1585,y=555,interval=0,clicks=1,button='left')
                
                
            elif 'next story' in query or 'next' in query or 'next stories' in query: #60
                pi.click(x=782,y=586,interval=0,clicks=1,button='left')
                
                
            elif 'profile' in query: #61
                try:
                    time.sleep(2)
                    image_path = 'profile.png'  
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                    if image is not None:
                       pyautogui.click(image)
                    else:
                       speak("I could not find the profile icon on the screen.")
                       print("I could not find the profile icon on the screen.")
                except Exception as e:
                    speak("An error occurred while trying to locate or click the profile icon.")
                    print(f"An error occurred: {e}")
                   
                   
                   
            elif 'home' in query: #62
                try:
                    time.sleep(2)
                    image_path = 'home.png' 
                    homeImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                    if homeImage is not None:
                       pyautogui.click(homeImage)
                    else:
                       speak("I could not find the home icon on the screen.")
                       print("I could not find the home icon on the screen.")
                except Exception as e:
                    speak("An error occurred while trying to locate or click the home icon.")
                    print(f"An error occurred: {e}")
                   
                   
                   
            elif 'friends' in query or 'friendlist' in query or 'friend list' in query: #63
                try:
                    time.sleep(2)
                    image_path = 'profile.png'  
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)  
                    if image is not None:
                       pyautogui.click(image)
                       time.sleep(2)
                       FriendList = pyautogui.locateCenterOnScreen("friend.png", confidence=0.8)
                       pi.click(FriendList)   
                    else:
                       speak("I could not find the friends icon on the screen.")
                       print("I could not find the friends icon on the screen.")
                except Exception as e:
                   speak("An error occurred while trying to locate or click the friends icon.")
                   print(f"An error occurred: {e}")
                   
                   
                   
            elif 'birthday' in query or 'birthdays' in query: #64
                try:
                    time.sleep(2)
                    image_path = 'profile.png' 
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)  
                    if image is not None:
                       pyautogui.click(image)
                       time.sleep(2)
                       FriendList = pyautogui.locateCenterOnScreen("friend.png", confidence=0.8)
                       pi.click(FriendList) 
                       time.sleep(1)
                       birthdays = pyautogui.locateCenterOnScreen("birthday.png", confidence=0.8)
                       pi.click(birthdays) 
                    else:
                       speak("I could not find the birthdays .")
                       print("I could not find the birthdays .")
                except Exception as e:
                   speak("An error occurred while trying to birthdays.")
                   print(f"An error occurred: {e}")
                   
                   
                   
            elif 'friend request' in query: #65
                try:
                     # pyautogui.hotkey('win', 's')
                     time.sleep(2)
                     # Ensure the image file path is correct
                     image_path = 'friends.png'  # Update with the correct path if needed
                     image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)  # Adjust confidence as needed
                     if image is not None:
                        pyautogui.click(image)
                        time.sleep(2)
                        RequestList = pyautogui.locateCenterOnScreen("SeeAll.png", confidence=0.8)
                        pi.click(RequestList)
                     else:
                        speak("I could not find friend request list on the screen.")
                        print("I could not find friend request list on the screen.")
                except Exception as e:
                   speak("An error occurred while trying to find friend request list.")
                   print(f"An error occurred: {e}")
                   
            
            
            elif 'memory' in query or "memories" in query: #67
                try:
                    time.sleep(2)
                    image_path = 'memory.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                    if image is not None:
                       pyautogui.click(image)
                    else:
                       speak("I could not find the memory icon on the screen.")
                       print("I could not find the memory icon on the screen.")
                except Exception as e:
                   speak("An error occurred while trying to locate or click the memory icon.")
                   print(f"An error occurred: {e}")
                   
                   
            
            elif 'saved' in query or "save" in query: #68
                try: 
                    time.sleep(2)
                    image_path = 'saved.png'  
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                    if image is not None:
                       pyautogui.click(image)
                    else:
                       speak("I could not find the saved icon on the screen.")
                       print("I could not find the saved icon on the screen.")
                except Exception as e:
                   speak("An error occurred while trying to locate or click the saved icon.")
                   print(f"An error occurred: {e}")
                   
                   
                   
            elif 'group' in query or "groups" in query: #69
                try:
                    time.sleep(2)
                    image_path = 'groups.png'  
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)  
                    if image is not None:
                       pyautogui.click(image)
                    else:
                       speak("I could not find the group icon on the screen.")
                       print("I could not find the group icon on the screen.")
                except Exception as e:
                   speak("An error occurred while trying to locate or click the group icon.")
                   print(f"An error occurred: {e}")
                   
                   
                   
            elif 'videos' in query: #70
                try:
                    time.sleep(2)
                    image_path = 'vid.png' 
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)  
                    if image is not None:
                       pyautogui.click(image) 
                    else:
                       speak("I could not find the video icon on the screen.")
                       print("I could not find the video icon on the screen.")
                except Exception as e:
                   speak("An error occurred while trying to locate or click the video icon.")
                   print(f"An error occurred: {e}")
            
            
            
            elif 'play upper video' in query: #71
                pi.click(x=773,y=206,clicks=1,interval=0,button="left")
                time.sleep(1)
                pi.click(x=1138,y=644,clicks=1,interval=0,button="left")
            
            
            
            elif "play the video" in query: #72
                pi.click(x=1138,y=644,clicks=1,interval=0,button="left")
            
            
            elif 'play lower video' in query: #73
                pi.click(x=773,y=967,clicks=1,interval=0,button="left")
                time.sleep(1)
                pi.click(x=1138,y=644,clicks=1,interval=0,button="left")
            
            
            
            elif 'sound' in query or 'sound the video' in query: #74
                pi.click(x=1700,y=920,clicks=1,interval=0,button="left")
                
                
            elif 'open messenger' in query or "close messenger" in query or " messenger" in query: #75
                try: 
                    time.sleep(2)
            
                    image_path = 'messanger.png'  
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                    if image is not None:
                       pyautogui.click(image)
                    else:
                       speak("I could not find the messenger icon on the screen.")
                       print("I could not find the messenger icon on the screen.")
                except Exception as e:
                   speak("An error occurred while trying to locate or click the messenger icon.")
                   print(f"An error occurred: {e}")
            
            
                   
            elif 'open first conversation and text' in query: #76
                pi.click(x=1600,y=335,clicks=1,interval=0,button="left")
                query = query.replace("open first conversation and text", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
                   
                   
                   
            elif 'open second conversation and text' in query: #77
                pi.click(x=1600,y=420,clicks=1,interval=0,button="left")
                query = query.replace("open second conversation and text", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
                   
                   
                   
            elif 'open third conversation and text' in query: #78
                pi.click(x=1600,y=505,clicks=1,interval=0,button="left")
                query = query.replace("open third conversation and text", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
                   
                   
                   
                   
            elif 'open fourth conversation and text' in query: #79
                pi.click(x=1600,y=590,clicks=1,interval=0,button="left")
                query = query.replace("open fourth conversation and text", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
                
                
                
            elif 'open fifth conversation and text' in query: #80
                pi.click(x=1600,y=675,clicks=1,interval=0,button="left")
                query = query.replace("open fifth conversation and text", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
                
                
                
            elif 'open six conversation and text' in query : #81
                pi.click(x=1600,y=760,clicks=1,interval=0,button="left")
                query = query.replace("open six conversation and text", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
                  
                  
                  
            elif 'open seven conversation and text' in query : #82
                pi.click(x=1600,y=845,clicks=1,interval=0,button="left")
                query = query.replace("open seven conversation and text", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
                  
                  
                  
            elif 'open 8 conversation and text' in query : #83
                pi.click(x=1600,y=930,clicks=1,interval=0,button="left")
                query = query.replace("open 8 conversation and text", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
                
                
                
            elif 'message' in query: #84
                query = query.replace("message", "").strip()
                pi.typewrite(query,0.2)
                pi.press('enter')
            
            
            
            elif 'close first open chat' in query or 'close fast open chat' in query: #85
                pi.click(x=934,y=538,clicks=1,interval=0,button='left')
                     
                     
            elif 'close second open chat' in query: #86
                pi.click(x=1352,y=538,clicks=1,interval=0,button='left')
                     
                      
            elif 'close third open chat' in query: #87
                pi.click(x=1781,y=538,clicks=1,interval=0,button='left')
            
            
            elif 'close all open chat' in query: #88
                pi.click(x=934,y=538,clicks=1,interval=0,button='left')
                pi.click(x=1352,y=538,clicks=1,interval=0,button='left')
                pi.click(x=1781,y=538,clicks=1,interval=0,button='left')
            
            
            # elif 'voice on first open chat' in query or 'voice on fast open chat':
            #     pi.click(x=572,y=1038,interval=0,clicks=1,button='left')
            #     time.sleep(20)
            #     pi.click(x=926,y=1038,interval=0,clicks=1,button='left')
            #     speak("voice message send")
            
            # elif 'voice on second open chat' in query:
            #     pi.click(x=1000,y=1038,interval=0,clicks=1,button='left')
            #     time.sleep(20)
            #     pi.click(x=1352,y=1038,interval=0,clicks=1,button='left')
            #     speak("voice message send")
            
            # elif 'voice on third open chat' in query:
            #     pi.click(x=1426,y=1038,interval=0,clicks=1,button='left')
            #     time.sleep(20)
            #     pi.click(x=1776,y=1038,interval=0,clicks=1,button='left')
            #     speak("voice message send")
            
            
            elif 'voice call on first open conversation'in query or 'voice call on fast open conversation'in query: #89
                pi.click(x=827,y=540,clicks=1,interval=0,button='left')
                 
                 
            elif 'video chat on first open conversation'in query or 'video chat on fast open conversation'in query: #90
                pi.click(x=861,y=540,clicks=1,interval=0,button='left')
                
                
            elif 'voice call on second open conversation'in query or 'voice call on 2nd open conversation'in query:#91
                pi.click(x=1245,y=540,clicks=1,interval=0,button='left')
                
                
            elif 'video chat on second open conversation'in query or 'video chat on 2nd open conversation'in query:#92
                pi.click(x=1279,y=540,clicks=1,interval=0,button='left')
                
                
            elif 'voice call on third open conversation'in query or 'voice call on 3rd open conversation'in query:#93
                pi.click(x=1670,y=540,clicks=1,interval=0,button='left')
                
                
            elif 'video chat on third open conversation'in query or 'video chat on 3rd open conversation'in query:#94
                pi.click(x=1704,y=540,clicks=1,interval=0,button='left')
                
                
            elif "cut this call" in query: #95
                image_path = 'CutThisCall.png'  
                pi.click(x=1500,y=540,clicks=1,interval=0,button='left')
                searchImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8) 
                pyautogui.click(searchImage)
                
                
                
            elif "wait for " in query: #96
                # number= re.search(r'\d+', query)
                # num=int(number.group())
                num=int(re.search(r'\d+',query).group())
                speak("Ok Sir...")
                time.sleep(num*60)
             
             
             
            elif "minimise" in query: #97
                # pi.click(x=1777,y=30,clicks=1,interval=0,button="left")
                pyautogui.hotkey('win','down')
                
                
            elif "maximize" in query: #98
                pyautogui.hotkey('win','up')
                # time.sleep(1)
                # pyautogui.press('enter')
                
                
            elif "go back" in query: #99
                pi.hotkey('alt','left')
                time.sleep(1)
                
                
            elif "close this window" in query: #100
                pyautogui.hotkey('alt','f4')
            
            
            elif "go to sleep" in query: #101
                speak("sir,I'm going to sleep.")
                speak("Please run the code whenever you need me.")
                sys.exit()
                
                
    else:
        speak("You enter the wrong password. Please run the code again and Enter the right password:")
           
