import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
from pydub.playback import play
from math import ceil
import threading
import os
import pygame.mixer as mix
import shutil
# import ctypes

# ctypes.windll.shcore.SetProcessDpiAwareness(1)

print(os.getcwd())
if os.path.exists('tmp'):
    shutil.rmtree('tmp')
os.mkdir('tmp')

def load_():
    root.filename = filedialog.askopenfilename(title="Select file", filetypes=(("WAV fies","*.wav"),))
    print('Recall file :'+root.filename)
    global sound, entry_windows, num_rows, play_each
    sound = AudioSegment.from_wav(root.filename)
    sound = sound.set_channels(1)
    num_rows = ceil(len(sound)/2000)
    for i in range(num_rows):
        sound[i*2000:(i+1)*2000].export('tmp/'+str(i)+'.wav', format='wav')
    entry_windows = []
    for i in range(num_rows):
        tk.Label(canvasFrame, text=str(i * 2) + ' - ' + str((i + 1) * 2)).grid(row=i + 1, column=0)
        tk.Button(canvasFrame, text="Play",bg='white',fg='red', command=lambda i=i: play_(i)).grid(row=i + 1, column=1)
        entry_windows.append(tk.Entry(canvasFrame))
        entry_windows[i].grid(row=i + 1, column=2, ipadx=85)


def play_(i):
    t = threading.Thread(target=play_threading_, args=(i,))
    t.start()

def play_threading_(i):
    #tmp_sound = AudioSegment.from_wav('tmp/'+str(i)+'.wav')
    #play(tmp_sound)
    mix.init()
    mix.music.load('tmp/'+str(i)+'.wav')
    mix.music.play()

def save_():
    string = []
    for i in range(num_rows):
        string.append(entry_windows[i].get())
    f= open('tmp/temporal_save.txt', 'w', encoding='utf-8')
    for s in string:
        f.write("{}\n".format(s))
    f.close()
    return

def saveas_():
    directory = filedialog.asksaveasfilename(defaultextension='.txt',filetypes=(("Text fies","*.txt"),))
    string = []
    for i in range(num_rows):
        string.append(entry_windows[i].get())
    f= open(directory, 'w', encoding='utf-8')
    for s in string:
        f.write("{}\n".format(s))
    f.close()
    return

def quit_():
    root.quit()

def update_scrollregion(event):
    mainCanvas.configure(scrollregion=mainCanvas.bbox("all"))

root = tk.Tk()
root.title("FilmMemory_dictation_nogada")

mainFrame = tk.Frame(root, width=450, height=550, bg="white")
mainFrame.grid()
mainFrame.rowconfigure(0, weight=1)
mainFrame.columnconfigure(0, weight=1)


tk.Button(mainFrame, text="Load_recall",bg='white',fg='red', command=load_).grid(row=0, column=0, sticky='w')
tk.Button(mainFrame, text="Save(tmp)",bg='white',fg='blue', command=save_).grid(row=1, column=0,sticky='w')
tk.Button(mainFrame, text="Save as",bg='white',fg='blue',command=saveas_).grid(row=7, column=0,sticky='w')
tk.Button(mainFrame, text="Quit",bg='white',fg='red', command=quit_).grid(row=8, column=0,sticky='e')


mainCanvas = tk.Canvas(mainFrame, bg="white", width=450, height=550)
mainCanvas.grid(row=2, column=0, sticky="nsew", pady=20, ipady=20)

canvasFrame = tk.Frame(mainCanvas, bg="white")
mainCanvas.create_window(0, 0, window=canvasFrame, anchor='nw')



mainScroll = tk.Scrollbar(mainFrame, orient=tk.VERTICAL)
mainScroll.config(command=mainCanvas.yview)
mainCanvas.config(yscrollcommand=mainScroll.set)
mainScroll.grid(row=2, column=1,sticky="ns")

canvasFrame.bind("<Configure>", update_scrollregion)

root.mainloop()
