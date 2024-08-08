from tkinter import *
from PIL import Image,ImageTk,ImageSequence
import time
import pygame
from pygame import mixer
mixer.init()

root=Tk()
root.title("**WELCOME**")

window_width = 600
window_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_x = (screen_width // 2) - (window_width // 2)
# print(position_x)
position_y = (screen_height // 2) - (window_height // 2)
# print(position_y)

root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
# root.geometry("400x300+564+282")



def play_gif():
    root.lift()
    root.attributes("-topmost",True)
    global img
    img=Image.open("Welcome.gif")
    lbl=Label(root)
    lbl.place(x=0,y=0)
    i=0
    mixer.music.load("OpeningMusic.mp3")
    mixer.music.play()
    
    for img in ImageSequence.Iterator(img):
        img=img.resize((600,400))
        img=ImageTk.PhotoImage(img)
        lbl.config(image=img)
        root.update()
        time.sleep(0.3)
    root.destroy()

play_gif()

root.mainloop()
      