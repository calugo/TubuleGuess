# Author Carlos Lugo to annotate the MT events.
# Copyright (c) 2023 Carlos A Lugo - SLCU University of Cambridge


import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from glob import glob
import pandas as pd

global events
global played
global current
global nj
global Nk
events=[]; played=[]; nj=0; Nk=0;



def undo_event():
    global current
    A=len(played);B=len(events);
    global nj
    print(A,B,nj,current)
    played.remove(played[A-1])
    events.remove(events[B-1])
    print(nj)
    if nj>=1:
        nj-=1
    else:
        nj=0
    current=mvs[nj]
    print(current)
    change_movie()

def load_video():
    """ loads the video """
    file_path = filedialog.askopenfilename()
    if file_path:
        vid_player.load(file_path)
        play_pause_btn["text"] = "Play"

def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Play"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Pause"

def find_all_movies():
    A=glob("*/", recursive = True)
    movies=[]
    for fn in A:
        B=glob(fn+"*/*.mp4",recursive=True)
        movies+=B
    mvxx=[j for j in movies if "__" in j]
    return mvxx

def choose():
    selection = "You selected the option " + str(collvar.get())
    label.config(text = selection)
    get_new()

def change_movie():
    print("---------")
    print("CHANGE_MOVIE")
    print(current)
    vid_player.load(current)
    play_pause()
    print(played)
    print(events)
    print("---------")

def get_new():
    ######
    print("GET_NEW")
    global nj,current
    events.append(collvar.get())
    played.append(current)
    U=pd.DataFrame(columns=['FILE','CHOICE'])
    U['FILE']=played;U['CHOICE']=events;
    U.to_csv("RESULTS.csv",index=False)

    nj+=1
    current=mvs[nj]
    change_movie()



mvs=find_all_movies()
Nk=len(mvs); 
current=mvs[0]

root = tk.Tk()
root.title("Collision Viewer")
root.geometry("350x350")

undo_btn = tk.Button(root, text="Undo", command=undo_event)
undo_btn.pack()

vid_player = TkinterVideo(scaled=False, master=root)
vid_player.pack(expand=True, fill="both")
vid_player.set_size((256,256),keep_aspect=True) 


play_pause_btn = tk.Button(root, text="Play", command=play_pause)
play_pause_btn.pack()

collvar = tk.StringVar(root,value='U')

R1 = tk.Radiobutton(root,text='X',variable=collvar,value='X',command=choose)
R1.pack(side='left')
R2 = tk.Radiobutton(root,text='Z',variable=collvar,value='Z',command=choose)
R2.pack(side='left')
R3 = tk.Radiobutton(root,text='K',variable=collvar,value='K',command=choose)
R3.pack(side='left')
R4 = tk.Radiobutton(root,text='U',variable=collvar,value='U',command=choose)
R4.pack(side='left')
label = tk.Label(root)
label.pack(side='left')

change_movie()

root.mainloop()