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
import pyautogui as pi
import requests
import re
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
from sklearn.dummy import DummyClassifier
import string
import pickle
import numpy as np
from mtcnn import MTCNN
import tensorflow as tf
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from keras_facenet import FaceNet
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import threading

# Global variables for camera (to fix undefined cap in commands)
cap = None
recording = False
out = None

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    # Speak in background and display speaking animation in foreground
    animation_data = SPK("gif/speaking_new.gif")
    if animation_data is None:
        # Fallback if can't load
        engine.say(audio)
        engine.runAndWait()
        return
    root, label, frames, durations, frame_index = animation_data
    
    # Start TTS in a separate thread (non-blocking for GUI)
    tts_done = [False]
    def tts_thread():
        engine.say(audio)
        engine.runAndWait()
        tts_done[0] = True
    thread = threading.Thread(target=tts_thread, daemon=True)
    thread.start()
    
    # Run animation in main thread with manual updates
    sleep_interval = 0.1  # Fixed interval for frame advance (adjust for smoothness)
    try:
        while not tts_done[0]:
            if root and root.winfo_exists():
                if frames is not None and len(frames) > 0:
                    # Advance frame
                    idx = frame_index[0]
                    frame = frames[idx]
                    frame_resized = frame.resize((300, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(frame_resized)
                    label.config(image=photo)
                    label.image = photo  # Keep reference
                    frame_index[0] = (idx + 1) % len(frames)
                root.update()
            time.sleep(sleep_interval)
    except tk.TclError:
        pass
    finally:
        if root:
            try:
                root.destroy()
            except tk.TclError:
                pass

def SPK(image_path):
    try:
        root = tk.Tk()
        root.title("SPEAKING...")
        window_width = 300
        window_height = 150
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
       
        root.geometry("300x150+10+800")
        label = tk.Label(root)
        label.pack()
        
        # Load GIF frames and durations
        frames = []
        durations = []
        try:
            img = Image.open(image_path)
            i = 0
            while True:
                try:
                    frame = img.copy()
                    duration = img.info.get('duration', 100)
                    frames.append(frame)
                    durations.append(duration)
                    img.seek(i + 1)
                    i += 1
                except EOFError:
                    break
        except Exception:
            frames = []
            durations = []
        
        frame_index = [0]  # Mutable for closure
        
        if len(frames) == 0:
            # Fallback static image
            try:
                static_img = Image.open(image_path).resize((300, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(static_img)
                label.config(image=photo)
                label.image = photo
            except Exception:
                pass
            root.update()
            return root, label, None, None, None
        
        root.update()
        return root, label, frames, durations, frame_index
    except Exception as e:
        print(f"Error loading speaking GIF: {e}")
        return None

def takeCommand():
    r = sr.Recognizer()
   
    animation_data = LSN("gif/listening.gif")
    if animation_data is None:
        # Fallback without animation
        with sr.Microphone() as source:
            time.sleep(1)
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query
    
    root, label, frames, durations, frame_index = animation_data
    
    # Start listening in a separate thread
    query_holder = [None]
    def listen_thread():
        with sr.Microphone() as source:
            time.sleep(1)
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            query_holder[0] = query
        except Exception as e:
            print("Say that again please...")
            query_holder[0] = "None"
    thread = threading.Thread(target=listen_thread, daemon=True)
    thread.start()
    
    # Run animation in main thread with manual updates until listen done
    sleep_interval = 0.1
    try:
        while query_holder[0] is None and thread.is_alive():
            if root and root.winfo_exists():
                if frames is not None and len(frames) > 0:
                    # Advance frame
                    idx = frame_index[0]
                    frame = frames[idx]
                    frame_resized = frame.resize((300, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(frame_resized)
                    label.config(image=photo)
                    label.image = photo  # Keep reference
                    frame_index[0] = (idx + 1) % len(frames)
                root.update()
            time.sleep(sleep_interval)
    except tk.TclError:
        pass
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass
   
    return query_holder[0]

def LSN(image_path):
    try:
        root = tk.Tk()
        root.title("LISTENING...")
        window_width = 300
        window_height = 150
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
       
        root.geometry("300x150+10+800")
        label = tk.Label(root)
        label.pack()
        
        # Load GIF frames and durations
        frames = []
        durations = []
        try:
            img = Image.open(image_path)
            i = 0
            while True:
                try:
                    frame = img.copy()
                    duration = img.info.get('duration', 100)
                    frames.append(frame)
                    durations.append(duration)
                    img.seek(i + 1)
                    i += 1
                except EOFError:
                    break
        except Exception:
            frames = []
            durations = []
        
        frame_index = [0]  # Mutable for closure
        
        if len(frames) == 0:
            # Fallback static image
            try:
                static_img = Image.open(image_path).resize((300, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(static_img)
                label.config(image=photo)
                label.image = photo
            except Exception:
                pass
            root.update()
            return root, label, None, None, None
        
        root.update()
        return root, label, frames, durations, frame_index
    except Exception as e:
        print(f"Error loading listening GIF: {e}")
        return None

def wishme():
    hour = int(datetime.datetime.now().hour)
   
    if hour >= 0 and hour < 12:
        speak("Good Morning, Sir.")
        # speak("Ready for the service.For security, Please verify your face")
       
    if hour >= 12 and hour < 18:
        speak("Good Afternoon, Sir. ")
       
    else:
        speak("Good Evening, Sir. ")

def face_lock():
    # Load FaceNet model in background to avoid blocking Tkinter UI and allow progress UI.
    facenet_container = {'model': None, 'error': None}
    def load_facenet():
        try:
            facenet_container['model'] = FaceNet()
        except Exception as e:
            facenet_container['error'] = e
    loader_thread = threading.Thread(target=load_facenet, daemon=True)
    loader_thread.start()
    print("Loading FaceNet model in background, please wait...")
    # Show a minimal loading UI while model loads; reuse listening GIF for animation.
    animation_data = LSN("gif/listening.gif")
    if animation_data is None:
        # Wait without animation
        load_timeout = 120  # seconds
        start_time = time.time()
        while loader_thread.is_alive() and (time.time() - start_time) < load_timeout:
            time.sleep(0.05)
    else:
        root, label, frames, durations, frame_index = animation_data
        load_timeout = 120  # seconds
        start_time = time.time()
        sleep_interval = 0.1
        try:
            while loader_thread.is_alive() and (time.time() - start_time) < load_timeout:
                if root and root.winfo_exists():
                    if frames is not None and len(frames) > 0:
                        # Advance frame
                        idx = frame_index[0]
                        frame = frames[idx]
                        frame_resized = frame.resize((300, 150), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(frame_resized)
                        label.config(image=photo)
                        label.image = photo  # Keep reference
                        frame_index[0] = (idx + 1) % len(frames)
                    root.update()
                time.sleep(sleep_interval)
        except tk.TclError:
            pass
        finally:
            if root:
                try:
                    root.destroy()
                except tk.TclError:
                    pass
    # At this point, either model loaded, an error occurred, or we timed out
    if facenet_container['error'] is not None:
        # If model load failed, log and exit gracefully
        print(f"Error loading FaceNet: {facenet_container['error']}")
        return None
    if facenet_container['model'] is None:
        print("FaceNet model not loaded within timeout. Exiting face lock.")
        return None
    facenet = facenet_container['model']
    print("FaceNet model loaded successfully.")
    try:
        faces_embeddings = np.load("face_net_embedding.npz") # file1
    except Exception as e:
        print(f"Error loading embeddings file: {e}")
        return None
    labelEncoder_new = LabelEncoder()
    labelEncoder_new.fit(faces_embeddings['arr_1'])
    haarcascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") # file2
    try:
        model = pickle.load(open("svm_face_verification_model.pkl", 'rb'))
    except Exception as e:
        print(f"Error loading SVM model: {e}")
        return None
    UNKNOWN_THRESHOLD = 0.92
    local_cap = cv2.VideoCapture(0)
    last_detection_time = 0
    detection_duration = 20
    door_closing_warning = 3
    final_name = None # to store the recognized name
    try:
        while local_cap.isOpened():
            current_time = time.time()
            ret, frame = local_cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            frame = cv2.flip(frame, 1)
            rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = haarcascade.detectMultiScale(gray_img, 1.3, 5)
            for x, y, w, h in faces:
                img = rgb_img[y:y+h, x:x+w]
                img = cv2.resize(img, (160, 160))
                img = np.expand_dims(img, axis=0)
                ypred = facenet.embeddings(img)
                proba = model.predict_proba(ypred)
                max_proba_index = np.argmax(proba)
                confidence = proba[0][max_proba_index]
                print(confidence)
                face_name = model.classes_[max_proba_index]
                if confidence > UNKNOWN_THRESHOLD:
                    final_name = labelEncoder_new.inverse_transform([face_name])[0]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
                    cv2.putText(frame, str(final_name), (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                    # Special case: Immediate access for "durjoy"
                    if final_name.lower() in ["durjoy"]:
                        time.sleep(2)
                        print(f"Access granted to {final_name}.")
                        speak(f"Access granted to {final_name}.")
                        local_cap.release()
                        cv2.destroyAllWindows()
                        return final_name
                    if current_time - last_detection_time < detection_duration:
                        processing_name = f"processing for {final_name}"
                        cv2.putText(frame, processing_name, (50, 50),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                    if (current_time - last_detection_time) >= detection_duration:
                        print(f"Command sent to Arduino: OPEN {final_name}")
                        say_name = str(f"Door is opening for {final_name} about 10 second")
                        speak(say_name)
                        last_detection_time = current_time
                        time.sleep(2) # Brief pause after granting access
                        local_cap.release()
                        cv2.destroyAllWindows()
                        return final_name
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
                    cv2.putText(frame, "Unknown Person", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                    final_name = "Unknown Person"
                    if current_time - last_detection_time >= detection_duration:
                        print("Access denied for unknown person.")
                        speak("Access denied. Unknown person detected.")
                        last_detection_time = current_time
                        time.sleep(2) # Brief pause after denial
                        local_cap.release()
                        cv2.destroyAllWindows()
                        return final_name
            cv2.imshow("Face Recognition:", frame)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, closing camera feed.")
    finally:
        try:
            local_cap.release()
        except Exception:
            pass
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
    return final_name

def password():
    lock_key=takeCommand().lower()
    return lock_key

def f_lock_speak():
    speak("Ready for the service")
    speak("For security purpose Please verify your face")

def f_lock_varified():
    speak("You are Verified")
    speak(" Now give your password for second verification")

if __name__ == "__main__":
    wishme()
    f_lock_speak()
    face = face_lock()
    if face is None:
        speak("Face verification failed or timed out. Please try again later.")
        sys.exit(1)

    f_lock_varified()

    # -----------------------------
    #   New Password Option Added
    # -----------------------------
    speak("Press K for keyboard password or V for voice password.")
    print("Choose password input method:")
    print("K = Keyboard")
    print("V = Voice")

    choice = input("Enter your choice (K/V): ").strip().lower()

    if choice == "k":
        pas = input("Enter your password: ")
        speak("Keyboard password received.")
    elif choice == "v":
        pas = password()   # Calling your existing function
        speak("Voice password received.")
    else:
        speak("Invalid input. Exiting.")
        print("Invalid choice!")
        sys.exit(1)

    # Now you can use 'pas' variable normally

    if pas == "7747":
        from intro import play_video
        play_video()
        try:
            speak("Welcome Sir. I am Jarvis, your voice assistant. How can I help you?")
        except Exception as e:
            print(f"Error in welcome message: {e}")
            speak("Sorry, an error occurred while initializing.")
        while True:
            query = takeCommand().lower()
            # 1: Respond to 'jarvis'
            try:
                if 'jarvis' in query:
                    print("YES SIR")
                    speak("YES SIR")
            except Exception as e:
                print(f"Error in 'jarvis' command: {e}")
                speak("Sorry, an error occurred while processing your command.")
            # 2: Who are you
            try:
                if "who are you" in query:
                    speak("My name is Jarvis. I can do everything that my creator programmed me to do.")
            except Exception as e:
                print(f"Error in 'who are you' command: {e}")
                speak("Sorry, an error occurred while processing your command.")
            # 3: Who created you
            try:
                if "who created you" in query:
                    speak("I was created by Durjoy using Python code.")
            except Exception as e:
                print(f"Error in 'who created you' command: {e}")
                speak("Sorry, an error occurred while processing your command.")
            # 4: Wikipedia search
            try:
                if 'what is' in query or 'who is' in query:
                    speak('Searching Wikipedia...')
                    results = wikipedia.summary(query, sentences=1)
                    speak("According to Wikipedia")
                    speak(results)
                    print(results)
            except Exception as e:
                print(f"Error in Wikipedia search: {e}")
                speak("Sorry, I couldn't find any results on Wikipedia.")
            # 5: Open Google
            try:
                if 'just open google' in query:
                    webbrowser.open('https://www.google.com')
            except Exception as e:
                print(f"Error in 'just open google' command: {e}")
                speak("Sorry, I couldn't open Google.")
            # 6: Search on Google
            try:
                if 'open google' in query:
                    speak("What should I search?")
                    qry = takeCommand().lower()
                    if qry != "None":
                        webbrowser.open(f"https://www.google.com/search?q={qry}")
                    else:
                        speak("No search query provided.")
            except Exception as e:
                print(f"Error in 'open google' command: {e}")
                speak("Sorry, I couldn't perform the Google search.")
            # 7: Open YouTube
            try:
                if 'just open youtube' in query:
                    webbrowser.open('https://www.youtube.com')
            except Exception as e:
                print(f"Error in 'just open youtube' command: {e}")
                speak("Sorry, I couldn't open YouTube.")
            # 8: Play on YouTube
            try:
                if 'open youtube' in query:
                    speak("What would you like to watch?")
                    qrry = takeCommand().lower()
                    if qrry != "None":
                        wk.playonyt(qrry)
                    else:
                        speak("No video query provided.")
            except Exception as e:
                print(f"Error in 'open youtube' command: {e}")
                speak("Sorry, I couldn't play the video on YouTube.")
            # 9: Search on YouTube
            try:
                if 'search on youtube' in query:
                    query = query.replace("search on youtube", "").strip()
                    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            except Exception as e:
                print(f"Error in 'search on youtube' command: {e}")
                speak("Sorry, I couldn't search on YouTube.")
            # 10: Close browser
            try:
                if 'close browser' in query:
                    os.system("taskkill /f /im msedge.exe")
            except Exception as e:
                print(f"Error in 'close browser' command: {e}")
                speak("Sorry, I couldn't close the browser.")
            # 11: Close Chrome
            try:
                if 'close chrome' in query:
                    os.system("taskkill /f /im chrome.exe")
            except Exception as e:
                print(f"Error in 'close chrome' command: {e}")
                speak("Sorry, I couldn't close Chrome.")
            # 12: Open CMD
            try:
                if 'open cmd' in query:
                    os.system('start cmd')
            except Exception as e:
                print(f"Error in 'open cmd' command: {e}")
                speak("Sorry, I couldn't open the command prompt.")
            # 13: Close CMD
            try:
                if 'close cmd' in query:
                    os.system("taskkill /f /im cmd.exe")
            except Exception as e:
                print(f"Error in 'close cmd' command: {e}")
                speak("Sorry, I couldn't close the command prompt.")
            # 14: Play music
            try:
                if 'play music' in query:
                    music_dir = 'E:\\PHONE\\SnapTube Audio'
                    songs = os.listdir(music_dir)
                    if songs:
                        os.startfile(os.path.join(music_dir, random.choice(songs)))
                    else:
                        speak("No songs found in the directory.")
            except FileNotFoundError:
                print("Music directory not found.")
                speak("Sorry, I couldn't find the music directory.")
            except Exception as e:
                print(f"Error in 'play music' command: {e}")
                speak("Sorry, an error occurred while playing music.")
            # 15: Close music
            try:
                if 'close music' in query:
                    os.system("taskkill /f /im vlc.exe")
            except Exception as e:
                print(f"Error in 'close music' command: {e}")
                speak("Sorry, I couldn't close the music player.")
            # 16: Play video
            try:
                if 'play video' in query:
                    video_dir = 'E:\\PHONE\\mp4'
                    videos = os.listdir(video_dir)
                    if videos:
                        os.startfile(os.path.join(video_dir, random.choice(videos)))
                    else:
                        speak("No videos found in the directory.")
            except FileNotFoundError:
                print("Video directory not found.")
                speak("Sorry, I couldn't find the video directory.")
            except Exception as e:
                print(f"Error in 'play video' command: {e}")
                speak("Sorry, an error occurred while playing the video.")
            # 17: Close video
            try:
                if 'close video' in query:
                    os.system("taskkill /f /im vlc.exe")
            except Exception as e:
                print(f"Error in 'close video' command: {e}")
                speak("Sorry, I couldn't close the video player.")
            # 18: Open favorite folder and play video
            try:
                if 'favourite folder' in query:
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
            except FileNotFoundError:
                print("Favorite folder or video not found.")
                speak("Sorry, I couldn't find the favorite folder or video.")
            except Exception as e:
                print(f"Error in 'favourite folder' command: {e}")
                speak("Sorry, an error occurred while accessing the favorite folder.")
            # 19: Tell time
            try:
                if 'time' in query:
                    strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
                    speak(f"Sir, the time is {strTime}")
            except Exception as e:
                print(f"Error in 'time' command: {e}")
                speak("Sorry, I couldn't retrieve the time.")
            # 20: Tell date
            try:
                if 'date' in query:
                    current_date = date.today()
                    formatted_date = current_date.strftime("%B %d, %Y")
                    speak(f"Today's date is: {formatted_date}")
            except Exception as e:
                print(f"Error in 'date' command: {e}")
                speak("Sorry, I couldn't retrieve the date.")
            # 21: Shut down
            try:
                if 'shut down' in query:
                    os.system('shutdown /s /t 5')
            except Exception as e:
                print(f"Error in 'shut down' command: {e}")
                speak("Sorry, I couldn't initiate shutdown.")
            # 22: Restart
            try:
                if 'restart' in query:
                    os.system('shutdown /r /t 5')
            except Exception as e:
                print(f"Error in 'restart' command: {e}")
                speak("Sorry, I couldn't initiate restart.")
            # 23: Lock
            try:
                if 'lock' in query:
                    os.system('rundll32.exe user32.dll,LockWorkStation')
            except Exception as e:
                print(f"Error in 'lock' command: {e}")
                speak("Sorry, I couldn't lock the workstation.")
            # 24: Start screen recording
            try:
                if 'start screen recording' in query:
                    pi.hotkey('win', 's')
                    pi.typewrite("OBS studio", 0.15)
                    pi.press('enter')
                    time.sleep(2)
                    pi.hotkey('ctrl', '1')
                    time.sleep(2)
                    pi.hotkey('win', 'down')
                    speak("Screen recording started...")
            except Exception as e:
                print(f"Error in 'start screen recording' command: {e}")
                speak("Sorry, I couldn't start screen recording.")
            # 25: Stop screen recording
            try:
                if 'stop screen recording' in query:
                    time.sleep(1)
                    pi.hotkey('ctrl', '0')
                    os.system("taskkill /f /im obs64.exe")
                    speak("Screen recording stopped")
            except Exception as e:
                print(f"Error in 'stop screen recording' command: {e}")
                speak("Sorry, I couldn't stop screen recording.")
            # 26: Pause recording
            try:
                if 'pause recording' in query:
                    time.sleep(1)
                    pi.hotkey('ctrl', '4')
                    speak("Screen recording paused")
            except Exception as e:
                print(f"Error in 'pause recording' command: {e}")
                speak("Sorry, I couldn't pause screen recording.")
            # 27: Unpause recording
            try:
                if 'unpause recording' in query:
                    time.sleep(1)
                    speak("Screen recording unpaused")
                    pi.hotkey('ctrl', '5')
            except Exception as e:
                print(f"Error in 'unpause recording' command: {e}")
                speak("Sorry, I couldn't unpause screen recording.")
            # 28: Open camera
            try:
                if "open camera" in query:
                    if cap is None:
                        cap = cv2.VideoCapture(0)
                        if not cap.isOpened():
                            speak("Error: Could not open camera.")
                            cap = None
                        else:
                            speak("Camera opened.")
                    else:
                        speak("Camera is already open.")
            except Exception as e:
                print(f"Error in 'open camera' command: {e}")
                speak("Sorry, an error occurred while opening the camera.")
            # 29: Capture photo
            try:
                if "capture photo" in query:
                    if cap is not None and cap.isOpened():
                        ret, frame = cap.read()
                        if ret:
                            random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                            filename = f"capture_photo/photo_{random_name}.jpg"
                            cv2.imwrite(filename, frame)
                            speak("Photo captured and saved successfully.")
                        else:
                            speak("Error: Could not read frame from camera.")
                    else:
                        speak("Camera is not open.")
            except Exception as e:
                print(f"Error in 'capture photo' command: {e}")
                speak("Sorry, an error occurred while capturing the photo.")
            # 30: Start video recording
            try:
                if "start video recording" in query:
                    if cap is None:
                        cap = cv2.VideoCapture(0)
                        if not cap.isOpened():
                            speak("Error: Could not open camera.")
                            cap = None
                        else:
                            fourcc = cv2.VideoWriter_fourcc(*'XVID')
                            out = cv2.VideoWriter('saved_video_recording/output.avi', fourcc, 20.0, (640, 480))
                            recording = True
                            speak("Video recording started.")
                    else:
                        if not recording:
                            fourcc = cv2.VideoWriter_fourcc(*'XVID')
                            out = cv2.VideoWriter('saved_video_recording/output.avi', fourcc, 20.0, (640, 480))
                            recording = True
                            speak("Video recording started.")
                        else:
                            speak("Video recording is already in progress.")
            except Exception as e:
                print(f"Error in 'start video recording' command: {e}")
                speak("Sorry, an error occurred while starting video recording.")
            # 31: Stop video recording
            try:
                if "stop video recording" in query:
                    if recording:
                        recording = False
                        if out:
                            out.release()
                            out = None
                        speak("Video recording stopped and saved successfully.")
                    else:
                        speak("No video recording in progress.")
            except Exception as e:
                print(f"Error in 'stop video recording' command: {e}")
                speak("Sorry, an error occurred while stopping video recording.")
            # 32: Close camera
            try:
                if "close camera" in query:
                    if cap is not None:
                        cap.release()
                        cap = None
                        if recording:
                            if out:
                                out.release()
                                out = None
                            recording = False
                        speak("Camera closed.")
                        cv2.destroyAllWindows()
                    else:
                        speak("Camera is not open.")
            except Exception as e:
                print(f"Error in 'close camera' command: {e}")
                speak("Sorry, an error occurred while closing the camera.")
            # 33: Take screenshot
            try:
                if "take a screenshot" in query:
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    img.save("saved_screensort/ss.png")
                    speak("Screenshot saved.")
            except Exception as e:
                print(f"Error in 'take a screenshot' command: {e}")
                speak("Sorry, I couldn't take a screenshot.")
            # 34: Get IP address
            try:
                if "ip address" in query:
                    speak("Checking...")
                    ipadd = requests.get('https://api.ipify.org').text
                    speak(f"Your IP address is: {ipadd}")
                    print(f"Your IP address is: {ipadd}")
            except requests.RequestException:
                print("Network error while fetching IP address.")
                speak("Network is weak, please try again later.")
            except Exception as e:
                print(f"Error in 'ip address' command: {e}")
                speak("Sorry, an error occurred while fetching the IP address.")
            # 35: Volume up
            try:
                if "volume up" in query:
                    for _ in range(5):
                        pyautogui.press("volumeup")
            except Exception as e:
                print(f"Error in 'volume up' command: {e}")
                speak("Sorry, I couldn't adjust the volume.")
            # 36: Volume down
            try:
                if "volume down" in query:
                    for _ in range(5):
                        pyautogui.press("volumedown")
            except Exception as e:
                print(f"Error in 'volume down' command: {e}")
                speak("Sorry, I couldn't adjust the volume.")
            # 37: Mute/Unmute
            try:
                if "mute" in query or "unmute" in query:
                    pyautogui.press("volumemute")
            except Exception as e:
                print(f"Error in 'mute/unmute' command: {e}")
                speak("Sorry, I couldn't toggle mute.")
            # 38: Open notepad
            try:
                if "open notepad" in query:
                    pi.press('win')
                    time.sleep(1)
                    pi.typewrite('notepad', 0.1)
                    pi.press('enter')
                    time.sleep(2)
                    pi.hotkey('ctrl', 'n')
                    speak('Please say what you have to note. I am ready to write')
                    tell = takeCommand()
                    pi.typewrite(tell, 0.1)
                    time.sleep(1)
                    pi.hotkey('ctrl', 's')
                    time.sleep(0.5)
                    pi.press('enter')
                    pi.press('enter')
                    speak("Your note is saved successfully")
            except Exception as e:
                print(f"Error in 'open notepad' command: {e}")
                speak("Sorry, I couldn't open or write to Notepad.")
            # 39: Close notepad
            try:
                if 'close notepad' in query:
                    os.system("taskkill /f /im notepad.exe")
            except Exception as e:
                print(f"Error in 'close notepad' command: {e}")
                speak("Sorry, I couldn't close Notepad.")
            # 40: Open calendar
            try:
                if "open calendar" in query:
                    pi.press('win')
                    time.sleep(1)
                    pi.typewrite('calendar', 0.1)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open calendar' command: {e}")
                speak("Sorry, I couldn't open the calendar.")
            # 41: Close calendar
            try:
                if "close calendar" in query:
                    os.system("taskkill /f /im HxCalendarAppImm.exe")
            except Exception as e:
                print(f"Error in 'close calendar' command: {e}")
                speak("Sorry, I couldn't close the calendar.")
            # 42: Open Word
            try:
                if "open word" in query:
                    pi.press('win')
                    time.sleep(1)
                    pi.typewrite('word', 0.1)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open word' command: {e}")
                speak("Sorry, I couldn't open Word.")
            # 43: Close Word
            try:
                if 'close word' in query:
                    os.system("taskkill /f /im winword.exe")
            except Exception as e:
                print(f"Error in 'close word' command: {e}")
                speak("Sorry, I couldn't close Word.")
            # 44: Open Excel
            try:
                if "open excel" in query:
                    pi.press('win')
                    time.sleep(1)
                    pi.typewrite('excel', 0.1)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open excel' command: {e}")
                speak("Sorry, I couldn't open Excel.")
            # 45: Close Excel
            try:
                if 'close excel' in query:
                    os.system("taskkill /f /im excel.exe")
            except Exception as e:
                print(f"Error in 'close excel' command: {e}")
                speak("Sorry, I couldn't close Excel.")
            # 46: Open PowerPoint
            try:
                if "open powerpoint" in query:
                    pi.press('win')
                    time.sleep(1)
                    pi.typewrite('power', 0.1)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open powerpoint' command: {e}")
                speak("Sorry, I couldn't open PowerPoint.")
            # 47: Close PowerPoint
            try:
                if 'close powerpoint' in query:
                    os.system("taskkill /f /im powerpnt.exe")
            except Exception as e:
                print(f"Error in 'close powerpoint' command: {e}")
                speak("Sorry, I couldn't close PowerPoint.")
            # 48: Audio call via WhatsApp
            try:
                if "audio call" in query:
                    qry = query.replace("audio call", "").strip()
                    if qry in ["yasin", "hadi", "shuvo", "benoy", "tushar","tuktuki"]:
                        pi.press('win')
                        time.sleep(2)
                        pi.typewrite('whatsapp', 0.1)
                        time.sleep(2)
                        pi.press('enter')
                        time.sleep(5)
                        image_path = 'picture/searching.png'
                        searchImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                        if searchImage:
                            pyautogui.click(searchImage)
                            time.sleep(1)
                            pi.typewrite(qry)
                            time.sleep(2)
                            pi.click(x=201, y=231, clicks=1, interval=0, button="left")
                            time.sleep(1)
                            pi.click(x=1823, y=95, clicks=1, interval=0, button="left")
                        else:
                            speak("Could not locate search icon on WhatsApp.")
                    else:
                        speak(f"There is no contact of {qry}'s name in WhatsApp.")
            except pyautogui.ImageNotFoundException:
                print("Search icon not found on WhatsApp.")
                speak("Sorry, I couldn't locate the search icon on WhatsApp.")
            except Exception as e:
                print(f"Error in 'audio call' command: {e}")
                speak("Sorry, I couldn't initiate the audio call.")
            # 49: Video call via WhatsApp
            try:
                if "video call" in query:
                    qry = query.replace("video call", "").strip()
                    if qry in ["yasin", "hadi", "shuvo", "benoy", "tushar"]:
                        pi.press('win')
                        time.sleep(2)
                        pi.typewrite('whatsapp', 0.1)
                        time.sleep(2)
                        pi.press('enter')
                        time.sleep(5)
                        image_path = 'picture/searching.png'
                        searchImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                        if searchImage:
                            pyautogui.click(searchImage)
                            time.sleep(1)
                            pi.typewrite(qry)
                            time.sleep(2)
                            pi.click(x=201, y=231, clicks=1, interval=0, button="left")
                            time.sleep(1)
                            pi.click(x=1767, y=86, clicks=1, interval=0, button="left")
                        else:
                            speak("Could not locate search icon on WhatsApp.")
                    else:
                        speak(f"There is no contact of {qry}'s name in WhatsApp.")
            except pyautogui.ImageNotFoundException:
                print("Search icon not found on WhatsApp.")
                speak("Sorry, I couldn't locate the search icon on WhatsApp.")
            except Exception as e:
                print(f"Error in 'video call' command: {e}")
                speak("Sorry, I couldn't initiate the video call.")
            # 50: Cut call
            try:
                if "cut the call" in query:
                    image_path = 'picture/call_ending.png'
                    searchImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if searchImage:
                        pyautogui.click(searchImage)
                    else:
                        speak("Could not locate call end button.")
            except pyautogui.ImageNotFoundException:
                print("Call end button not found.")
                speak("Sorry, I couldn't locate the call end button.")
            except Exception as e:
                print(f"Error in 'cut the call' command: {e}")
                speak("Sorry, I couldn't end the call.")
            # 51: Open Facebook
            try:
                if 'open facebook' in query:
                    pi.press('win')
                    time.sleep(2)
                    pi.typewrite('facebook', 0.1)
                    time.sleep(2)
                    pi.press('enter')
                    time.sleep(5)
            except pyautogui.ImageNotFoundException:
                print("Facebook icon not found.")
                speak("Sorry, I couldn't locate the Facebook icon.")
            except Exception as e:
                print(f"Error in 'open facebook' command: {e}")
                speak("Sorry, I couldn't open Facebook.")
            # 52: Check/Close notification
            try:
                if 'check notification' in query or 'close notification' in query:
                    pi.click(x=1796, y=81, clicks=1, interval=0, button="left")
            except Exception as e:
                print(f"Error in 'check/close notification' command: {e}")
                speak("Sorry, I couldn't handle the notification.")
            # 53: Unread notification
            try:
                if 'unread notification' in query:
                    pi.click(x=1561, y=181, clicks=1, interval=0, button="left")
            except Exception as e:
                print(f"Error in 'unread notification' command: {e}")
                speak("Sorry, I couldn't access unread notifications.")
            # 54: Previous notification
            try:
                if 'previous notification' in query:
                    pi.click(x=1632, y=953, clicks=1, interval=0, button="left")
            except Exception as e:
                print(f"Error in 'previous notification' command: {e}")
                speak("Sorry, I couldn't access previous notifications.")
            # 55: Scroll down
            try:
                if 'scroll down' in query:
                    pyautogui.moveTo(800, 700, duration=1)
                    for _ in range(30):
                        pyautogui.scroll(-20)
            except Exception as e:
                print(f"Error in 'scroll down' command: {e}")
                speak("Sorry, I couldn't scroll down.")
            # 56: Scroll up
            try:
                if 'scroll up' in query:
                    pyautogui.moveTo(800, 700, duration=1)
                    for _ in range(30):
                        pyautogui.scroll(20)
            except Exception as e:
                print(f"Error in 'scroll up' command: {e}")
                speak("Sorry, I couldn't scroll up.")
            # 57: Refresh
            try:
                if 'refresh' in query:
                    pi.hotkey('ctrl', 'r')
                    time.sleep(2)
            except Exception as e:
                print(f"Error in 'refresh' command: {e}")
                speak("Sorry, I couldn't refresh the page.")
            # 58: See story
            try:
                if 'see story' in query or 'story' in query or 'stories' in query:
                    pi.click(x=1080, y=960, interval=0, clicks=1, button='left')
            except Exception as e:
                print(f"Error in 'see story' command: {e}")
                speak("Sorry, I couldn't view the story.")
            # 59: Back story
            try:
                if 'back story' in query or 'back' in query or 'back stories' in query:
                    pi.click(x=1585, y=555, interval=0, clicks=1, button='left')
            except Exception as e:
                print(f"Error in 'back story' command: {e}")
                speak("Sorry, I couldn't go back to the previous story.")
            # 60: Next story
            try:
                if 'next story' in query or 'next' in query or 'next stories' in query:
                    pi.click(x=782, y=586, interval=0, clicks=1, button='left')
            except Exception as e:
                print(f"Error in 'next story' command: {e}")
                speak("Sorry, I couldn't go to the next story.")
            # 61: Profile
            try:
                if 'profile' in query:
                    time.sleep(2)
                    image_path = 'picture/profile.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                    else:
                        speak("I could not find the profile icon on the screen.")
                        print("I could not find the profile icon on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Profile icon not found.")
                speak("Sorry, I couldn't locate the profile icon.")
            except Exception as e:
                print(f"Error in 'profile' command: {e}")
                speak("Sorry, an error occurred while accessing the profile.")
            # 62: Home
            try:
                if 'home' in query:
                    time.sleep(2)
                    image_path = 'picture/home.png'
                    homeImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if homeImage:
                        pyautogui.click(homeImage)
                    else:
                        speak("I could not find the home icon on the screen.")
                        print("I could not find the home icon on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Home icon not found.")
                speak("Sorry, I couldn't locate the home icon.")
            except Exception as e:
                print(f"Error in 'home' command: {e}")
                speak("Sorry, an error occurred while accessing the home page.")
            # 63: Friends
            try:
                if 'friends' in query or 'friendlist' in query or 'friend list' in query:
                    time.sleep(2)
                    image_path = 'picture/profile.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                        time.sleep(2)
                        FriendList = pyautogui.locateCenterOnScreen("friend.png", confidence=0.8)
                        pi.click(FriendList)
                    else:
                        speak("I could not find the friends icon on the screen.")
                        print("I could not find the friends icon on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Friends icon not found.")
                speak("Sorry, I couldn't locate the friends icon.")
            except Exception as e:
                print(f"Error in 'friends' command: {e}")
                speak("Sorry, an error occurred while accessing the friends list.")
            # 64: Birthday
            try:
                if 'birthday' in query or 'birthdays' in query:
                    time.sleep(2)
                    image_path = 'picture/profile.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                        time.sleep(2)
                        FriendList = pyautogui.locateCenterOnScreen("friend.png", confidence=0.8)
                        pi.click(FriendList)
                        time.sleep(1)
                        birthdays = pyautogui.locateCenterOnScreen("birthday.png", confidence=0.8)
                        pi.click(birthdays)
                    else:
                        speak("I could not find the birthdays.")
                        print("I could not find the birthdays.")
            except pyautogui.ImageNotFoundException:
                print("Birthday icon not found.")
                speak("Sorry, I couldn't locate the birthdays.")
            except Exception as e:
                print(f"Error in 'birthday' command: {e}")
                speak("Sorry, an error occurred while accessing birthdays.")
            # 65: Friend request
            try:
                if 'friend request' in query:
                    time.sleep(2)
                    image_path = 'picture/friends.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                        time.sleep(2)
                        RequestList = pyautogui.locateCenterOnScreen("SeeAll.png", confidence=0.8)
                        pi.click(RequestList)
                    else:
                        speak("I could not find friend request list on the screen.")
                        print("I could not find friend request list on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Friend request icon not found.")
                speak("Sorry, I couldn't locate the friend request list.")
            except Exception as e:
                print(f"Error in 'friend request' command: {e}")
                speak("Sorry, an error occurred while accessing friend requests.")
            # 67: Memory
            try:
                if 'memory' in query or "memories" in query:
                    time.sleep(2)
                    image_path = 'picture/memory.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                    else:
                        speak("I could not find the memory icon on the screen.")
                        print("I could not find the memory icon on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Memory icon not found.")
                speak("Sorry, I couldn't locate the memory icon.")
            except Exception as e:
                print(f"Error in 'memory' command: {e}")
                speak("Sorry, an error occurred while accessing memories.")
            # 68: Saved
            try:
                if 'saved' in query or "save" in query:
                    time.sleep(2)
                    image_path = 'picture/saved.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                    else:
                        speak("I could not find the saved icon on the screen.")
                        print("I could not find the saved icon on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Saved icon not found.")
                speak("Sorry, I couldn't locate the saved icon.")
            except Exception as e:
                print(f"Error in 'saved' command: {e}")
                speak("Sorry, an error occurred while accessing saved items.")
            # 69: Groups
            try:
                if 'group' in query or "groups" in query:
                    time.sleep(2)
                    image_path = 'picture/groups.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                    else:
                        speak("I could not find the group icon on the screen.")
                        print("I could not find the group icon on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Groups icon not found.")
                speak("Sorry, I couldn't locate the group icon.")
            except Exception as e:
                print(f"Error in 'groups' command: {e}")
                speak("Sorry, an error occurred while accessing groups.")
            # 70: Videos
            try:
                if 'videos' in query:
                    time.sleep(2)
                    image_path = 'picture/vid.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                    else:
                        speak("I could not find the video icon on the screen.")
                        print("I could not find the video icon on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Videos icon not found.")
                speak("Sorry, I couldn't locate the video icon.")
            except Exception as e:
                print(f"Error in 'videos' command: {e}")
                speak("Sorry, an error occurred while accessing videos.")
            # 71: Play upper video
            try:
                if 'play upper video' in query:
                    pi.click(x=773, y=206, clicks=1, interval=0, button="left")
                    time.sleep(1)
                    pi.click(x=1138, y=644, clicks=1, interval=0, button="left")
            except Exception as e:
                print(f"Error in 'play upper video' command: {e}")
                speak("Sorry, I couldn't play the upper video.")
            # 72: Play the video
            try:
                if "play the video" in query:
                    pi.click(x=1138, y=644, clicks=1, interval=0, button="left")
            except Exception as e:
                print(f"Error in 'play the video' command: {e}")
                speak("Sorry, I couldn't play the video.")
            # 73: Play lower video
            try:
                if 'play lower video' in query:
                    pi.click(x=773, y=967, clicks=1, interval=0, button="left")
                    time.sleep(1)
                    pi.click(x=1138, y=644, clicks=1, interval=0, button="left")
            except Exception as e:
                print(f"Error in 'play lower video' command: {e}")
                speak("Sorry, I couldn't play the lower video.")
            # 74: Sound the video
            try:
                if 'sound' in query or 'sound the video' in query:
                    pi.click(x=1700, y=920, clicks=1, interval=0, button="left")
            except Exception as e:
                print(f"Error in 'sound the video' command: {e}")
                speak("Sorry, I couldn't toggle the video sound.")
            # 75: Open/Close Messenger
            try:
                if 'open messenger' in query or "close messenger" in query or "messenger" in query:
                    time.sleep(2)
                    image_path = 'picture/messanger.png'
                    image = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if image:
                        pyautogui.click(image)
                    else:
                        speak("I could not find the messenger icon on the screen.")
                        print("I could not find the messenger icon on the screen.")
            except pyautogui.ImageNotFoundException:
                print("Messenger icon not found.")
                speak("Sorry, I couldn't locate the messenger icon.")
            except Exception as e:
                print(f"Error in 'messenger' command: {e}")
                speak("Sorry, an error occurred while accessing Messenger.")
            # 76: Open first conversation and text
            try:
                if 'open first conversation and text' in query:
                    pi.click(x=1600, y=335, clicks=1, interval=0, button="left")
                    query = query.replace("open first conversation and text", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open first conversation and text' command: {e}")
                speak("Sorry, I couldn't send the message in the first conversation.")
            # 77: Open second conversation and text
            try:
                if 'open second conversation and text' in query:
                    pi.click(x=1600, y=420, clicks=1, interval=0, button="left")
                    query = query.replace("open second conversation and text", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open second conversation and text' command: {e}")
                speak("Sorry, I couldn't send the message in the second conversation.")
            # 78: Open third conversation and text
            try:
                if 'open third conversation and text' in query:
                    pi.click(x=1600, y=505, clicks=1, interval=0, button="left")
                    query = query.replace("open third conversation and text", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open third conversation and text' command: {e}")
                speak("Sorry, I couldn't send the message in the third conversation.")
            # 79: Open fourth conversation and text
            try:
                if 'open fourth conversation and text' in query:
                    pi.click(x=1600, y=590, clicks=1, interval=0, button="left")
                    query = query.replace("open fourth conversation and text", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open fourth conversation and text' command: {e}")
                speak("Sorry, I couldn't send the message in the fourth conversation.")
            # 80: Open fifth conversation and text
            try:
                if 'open fifth conversation and text' in query:
                    pi.click(x=1600, y=675, clicks=1, interval=0, button="left")
                    query = query.replace("open fifth conversation and text", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open fifth conversation and text' command: {e}")
                speak("Sorry, I couldn't send the message in the fifth conversation.")
            # 81: Open sixth conversation and text
            try:
                if 'open six conversation and text' in query:
                    pi.click(x=1600, y=760, clicks=1, interval=0, button="left")
                    query = query.replace("open six conversation and text", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open six conversation and text' command: {e}")
                speak("Sorry, I couldn't send the message in the sixth conversation.")
            # 82: Open seventh conversation and text
            try:
                if 'open seven conversation and text' in query:
                    pi.click(x=1600, y=845, clicks=1, interval=0, button="left")
                    query = query.replace("open seven conversation and text", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open seven conversation and text' command: {e}")
                speak("Sorry, I couldn't send the message in the seventh conversation.")
            # 83: Open eighth conversation and text
            try:
                if 'open 8 conversation and text' in query:
                    pi.click(x=1600, y=930, clicks=1, interval=0, button="left")
                    query = query.replace("open 8 conversation and text", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'open 8 conversation and text' command: {e}")
                speak("Sorry, I couldn't send the message in the eighth conversation.")
            # 84: Send message
            try:
                if 'message' in query:
                    query = query.replace("message", "").strip()
                    pi.typewrite(query, 0.2)
                    pi.press('enter')
            except Exception as e:
                print(f"Error in 'message' command: {e}")
                speak("Sorry, I couldn't send the message.")
            # 85: Close first open chat
            try:
                if 'close first open chat' in query or 'close fast open chat' in query:
                    pi.click(x=934, y=538, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'close first open chat' command: {e}")
                speak("Sorry, I couldn't close the first chat.")
            # 86: Close second open chat
            try:
                if 'close second open chat' in query:
                    pi.click(x=1352, y=538, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'close second open chat' command: {e}")
                speak("Sorry, I couldn't close the second chat.")
            # 87: Close third open chat
            try:
                if 'close third open chat' in query:
                    pi.click(x=1781, y=538, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'close third open chat' command: {e}")
                speak("Sorry, I couldn't close the third chat.")
            # 88: Close all open chats
            try:
                if 'close all open chat' in query:
                    pi.click(x=934, y=538, clicks=1, interval=0, button='left')
                    pi.click(x=1352, y=538, clicks=1, interval=0, button='left')
                    pi.click(x=1781, y=538, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'close all open chat' command: {e}")
                speak("Sorry, I couldn't close all open chats.")
            # 89: Voice call on first open conversation
            try:
                if 'voice call on first open conversation' in query or 'voice call on fast open conversation' in query:
                    pi.click(x=827, y=540, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'voice call on first open conversation' command: {e}")
                speak("Sorry, I couldn't initiate the voice call on the first conversation.")
            # 90: Video chat on first open conversation
            try:
                if 'video chat on first open conversation' in query or 'video chat on fast open conversation' in query:
                    pi.click(x=861, y=540, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'video chat on first open conversation' command: {e}")
                speak("Sorry, I couldn't initiate the video chat on the first conversation.")
            # 91: Voice call on second open conversation
            try:
                if 'voice call on second open conversation' in query or 'voice call on 2nd open conversation' in query:
                    pi.click(x=1245, y=540, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'voice call on second open conversation' command: {e}")
                speak("Sorry, I couldn't initiate the voice call on the second conversation.")
            # 92: Video chat on second open conversation
            try:
                if 'video chat on second open conversation' in query or 'video chat on 2nd open conversation' in query:
                    pi.click(x=1279, y=540, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'video chat on second open conversation' command: {e}")
                speak("Sorry, I couldn't initiate the video chat on the second conversation.")
            # 93: Voice call on third open conversation
            try:
                if 'voice call on third open conversation' in query or 'voice call on 3rd open conversation' in query:
                    pi.click(x=1670, y=540, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'voice call on third open conversation' command: {e}")
                speak("Sorry, I couldn't initiate the voice call on the third conversation.")
            # 94: Video chat on third open conversation
            try:
                if 'video chat on third open conversation' in query or 'video chat on 3rd open conversation' in query:
                    pi.click(x=1704, y=540, clicks=1, interval=0, button='left')
            except Exception as e:
                print(f"Error in 'video chat on third open conversation' command: {e}")
                speak("Sorry, I couldn't initiate the video chat on the third conversation.")
            # 95: Cut this call
            try:
                if "cut this call" in query:
                    image_path = 'picture/CutThisCall.png'
                    pi.click(x=1500, y=540, clicks=1, interval=0, button='left')
                    searchImage = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                    if searchImage:
                        pyautogui.click(searchImage)
                    else:
                        speak("Could not locate call end button.")
            except pyautogui.ImageNotFoundException:
                print("Call end button not found.")
                speak("Sorry, I couldn't locate the call end button.")
            except Exception as e:
                print(f"Error in 'cut this call' command: {e}")
                speak("Sorry, I couldn't end the call.")
            # 96: Wait for minutes
            try:
                if "wait for " in query:
                    num = int(re.search(r'\d+', query).group())
                    speak("Ok Sir...")
                    time.sleep(num * 60)
            except ValueError:
                print("Invalid number in wait command.")
                speak("Sorry, I couldn't understand the wait duration.")
            except Exception as e:
                print(f"Error in 'wait for' command: {e}")
                speak("Sorry, an error occurred while waiting.")
            # 97: Minimize
            try:
                if "minimise" in query:
                    pyautogui.hotkey('win', 'down')
            except Exception as e:
                print(f"Error in 'minimise' command: {e}")
                speak("Sorry, I couldn't minimize the window.")
            # 98: Maximize
            try:
                if "maximize" in query:
                    pyautogui.hotkey('win', 'up')
            except Exception as e:
                print(f"Error in 'maximize' command: {e}")
                speak("Sorry, I couldn't maximize the window.")
            # 99: Go back
            try:
                if "go back" in query:
                    pi.hotkey('alt', 'left')
                    time.sleep(1)
            except Exception as e:
                print(f"Error in 'go back' command: {e}")
                speak("Sorry, I couldn't go back.")
            # 100: Close this window
            try:
                if "close this window" in query:
                    pyautogui.hotkey('alt', 'f4')
            except Exception as e:
                print(f"Error in 'close this window' command: {e}")
                speak("Sorry, I couldn't close the window.")
            # 101: Go to sleep
            try:
                if "go to sleep" in query:
                    speak("Sir, I'm going to sleep.")
                    speak("Please run the code whenever you need me.")
                    # Clean up globals
                    if cap:
                        cap.release()
                    if out:
                        out.release()
                    cv2.destroyAllWindows()
                    sys.exit()
            except Exception as e:
                print(f"Error in 'go to sleep' command: {e}")
                speak("Sorry, an error occurred while shutting down.")
    else:
        try:
            speak("You entered the wrong password. Please run the code again and enter the right password.")
        except Exception as e:
            print(f"Error in wrong password message: {e}")
            speak("Sorry, an error occurred while processing the password.")