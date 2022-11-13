from tkinter import *
import mne
from tkinter import messagebox
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from collections import deque
import pandas as pd
from tkinter import ttk

def cancel():
   win.destroy()

global win

win = Tk()
win.title("Dashboard")
win.geometry("750x500")
win.configure(background="#ffffff")
win.minsize(width=1280, height=600)

def tab2():
   win.withdraw()
   data = mne.io.read_raw_edf(file, preload=True)
   raw_data = data.get_data()

   # Data information
   print(np.shape(raw_data))

   # Interactive plotting
   plt.ion()
   sfreq = 400  # sampling frequency
   visible = 2000  # time shown in plot (in samples) --> 4 seconds
   channels = ['FP1', 'FP2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'FZ',
               'CZ', 'PZ', 'EKG', 'A1', 'A2', 'T1', 'T2', 'SP1', 'SP2', 'LUC', 'RLC', "RESP1", 'RESP2', '31', '32']

   # initialize deques
   dy = [deque(np.zeros(visible), visible) for i in range(32)]
   print(dy)
   dx = deque(np.zeros(visible), visible)

   # get interval of entire time frame
   interval = np.linspace(0, raw_data.shape[1], num=raw_data.shape[1])
   interval /= sfreq  # from samples to seconds

   # define figure size
   fig = plt.figure(figsize=(20, 12))
   ax = fig.gca()
   ah = [0 for i in range(32)]
   mdy = [0 for i in range(32)]
   l = [0 for i in range(32)]

   # define axis1, labels, and legend
   for k in range(32):
      ah[k] = fig.add_subplot(32, 1, k + 1)
      l[k], = ah[k].plot(dx, dy[k], color='rosybrown', label=channels[k])
      ah[k].legend(loc="upper right", fontsize=12, fancybox=True, framealpha=0.5)

   ah[16].set_ylabel("Voltage [\u03BCV]", fontsize=14)

   start = 0
   df = pd.DataFrame(raw_data)
   df_t = df.transpose()  # transposed

   # simulate entire data
   while start + visible <= df.shape[1]:
      # extend deques (both x and y axes)
      for t in range(32):
         dy[t].extend(df_t[t].iloc[start:start + visible])
         dx.extend(interval[start:start + visible])
         # update plot
         l[t].set_ydata(dy[t])
         l[t].set_xdata(dx)
         # get mean of deques
         mdy[t] = np.mean(dy[t])
         # set x- and y-limits based on their mean
         ah[t].set_ylim(-0.0002 + mdy[t], 0.0002 + mdy[t])
         ah[t].set_xlim(interval[start], interval[start + visible])

      # control speed of moving time-series
      start += 25
      fig.canvas.draw()
      fig.canvas.flush_events()

def entry_to_csv():
   print()

def fileinput():
   global file
   file = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("EDF files","*.edf"),("all files","*.*")))

#Tab1

#Logos
pnecLogo_path = "D:/University/FYP/GUI/code/images/PNEC.png"   #Change the path value as required
plogo = Image.open(pnecLogo_path)
plogo_resized = plogo.resize((130,130), Image.Resampling.LANCZOS)
pnec_logo = ImageTk.PhotoImage(plogo_resized)
PNEClogo = Label(image=pnec_logo, bg = '#ffffff')
PNEClogo.place(x=1120, y=28)

navyLogo_path = "D:/University/FYP/GUI/code/images/NUST.png"   #Change the path value as required
nlogo = Image.open(navyLogo_path)
nlogo_resized = nlogo.resize((100,100), Image.Resampling.LANCZOS)
navy_logo = ImageTk.PhotoImage(nlogo_resized)
navyLogo = Label(image=navy_logo, bg = '#ffffff')
navyLogo.place(x=80, y=30)

# Content ---
title = Label(win, text="Welcome to EEG Signal Analysis", font=('Helvetica 17 bold'))
title.config(font=("Ariel", 20,  "bold"), bg="#ffffff", fg="navy blue")
title.place(x=400, y=40)

# Frame for input fields
frame1 = Frame(win, width=500, height=300, relief='groove')
frame1.place(x=100, y=200)
label = Label(frame1, text='Enter the details', font=("Helvetica", 18))
label.place(x=25, y=25)

label1 = Label(frame1, text='Type your Name:', font=("Normal", 13))
label1.place(x=25, y=100)
entry1 = tk.Entry(frame1)
entry1.place(x=250, y=100)

label2 = Label(frame1, text='Type your Roll Number:', font=("Normal", 13))
label2.place(x=25, y=150)
entry2 = tk.Entry(frame1)
entry2.place(x=250, y=150)

label3 = Label(frame1, text='Type the Hospital name:', font=("Normal", 13))
label3.place(x=25, y=200)
entry3 = tk.Entry(frame1)
entry3.place(x=250, y=200)

browse = Button(frame1, text="Browse File  ", command=fileinput)
print(browse)
browse.place(x=200, y=250)

#Save field inputs to entry_to_csv() function --- yet to be written

#Frame for buttons
frame2 = Frame(win, width=500, height=300, relief="groove")
frame2.place(x=700, y=200)

tab_2 = Button(frame2, text="NEXT", width=12, height=1, bd=0, command=tab2, activebackground="white", bg="red", fg=("white"), font=("Ariel", 12))
tab_2.place(x=100, y=250)

exit_button = Button(frame2, text="EXIT", width=12, height=1, bd=0, command=cancel, bg="navy blue", fg=("white"), font=("Ariel", 12))
exit_button.place(x=300, y=250)

img = Image.open("images/brain_eeg.jpg")
resized_img = img.resize((500,200), Image.Resampling.LANCZOS)
image = ImageTk.PhotoImage(resized_img)
img_lbl = Label(frame2, image = image)
img_lbl.place(x=0, y=0)

win.mainloop()