from tkinter import *
from PIL import Image, ImageTk
import time
import pygame
from pygame import mixer
import cv2  # Requires: pip install opencv-python

mixer.init()

def play_video():
    root = Tk()
    root.title("**WELCOME**")

    window_width = 600
    window_height = 400

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    root.lift()
    root.attributes("-topmost", True)
    
    # Initialize video capture
    cap = cv2.VideoCapture("gif/welcome.mp4")
    if not cap.isOpened():
        print("Error: Could not open video file.")
        root.destroy()
        return
    
    # Get FPS for proper playback speed
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30  # Default fallback
    delay = 1.0 / fps
    
    # Create label for displaying frames
    lbl = Label(root)
    lbl.place(x=0, y=0)
    
    # Play audio
    mixer.music.load("audio/OpeningMusic.mp3")
    mixer.music.play()
    
    # Read and display frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize frame
        frame = cv2.resize(frame, (window_width, window_height))
        
        # Convert to PIL Image and then PhotoImage
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(img)
        
        # Update label
        lbl.config(image=photo)
        lbl.image = photo  # Keep a reference to avoid garbage collection
        
        root.update()
        time.sleep(delay)
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    mixer.music.stop()  # Stop music if still playing
    root.destroy()

if __name__ == "__main__":
    play_video()