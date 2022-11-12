import sounddevice as sd
import tkinter
import queue
import soundfile as sf
import threading
from tkinter import messagebox
import uuid
import codecs
import os
import shutil
import customtkinter

# Create a queue to contain the audio data
q = queue.Queue()
# Declare variables and initialise them
recording = False
file_exists = False
mytext = "Hello"
currentID = 0


def callback(indata, frames, time, status):
    q.put(indata.copy())


arrayi = ["Hello", "Will this work?"]
i = 0


def threading_rec(x):
    global recording, i, mytext, file_exists, record_btn
    if x == 1:
        # Start Recording
        t1 = threading.Thread(target=record_audio)
        t1.start()
        record_btn.set_text("Recording")
    elif x == 2:
        # Stop Recording
        recording = False
        # messagebox.showinfo(message="Recording finished")
        record_btn.set_text("Record")
    elif x == 3:
        # Play Recording
        #stop recording to play
        recording = False

        if file_exists:
            readFrom = "NLP/TempOutputSpeech/" + currentID + ".wav"
            data, fs = sf.read(readFrom, dtype='float32')
            sd.play(data, fs)
            sd.wait()
            record_btn.set_text("Record")
        else:
            messagebox.showerror(message="Record something to play")
    elif x == 5:
        # Upload Recording
        if not file_exists:
            messagebox.showerror(message="Record something to upload")
        else:
            source = "NLP/TempOutputSpeech/"+currentID+".wav"
            destination = 'NLP/OutputSpeech'
            shutil.copy2(source, destination)
            nametext = "NLP/OutputText/" + currentID + ".txt"
            textfile = codecs.open(nametext, 'w', 'utf-8')
            textfile.write(mytext)
            #Auto Next text display on Upload
            mytext = arrayi[i]
            title_lbl.configure(text=mytext)
            i += 1
            record_btn.set_text("Record")
    elif x == 4:
        # Next
        #Add to skipped files
        nametext = "NLP/SkippedFiles.txt"
        textfile = codecs.open(nametext, 'a', 'utf-8')
        textfile.write(mytext)
        
        mytext = arrayi[i]
        title_lbl.configure(text=mytext)
        i += 1
        record_btn.set_text("Record")
        file_exists = False

# Recording function


def record_audio():
    # Declare global variables
    global recording
    global currentID

    # Set to True to record
    recording = True
    global file_exists

    # messagebox.showinfo(message="Recording Audio. Speak into the mic")
    currentID = str(uuid.uuid4())
    name = "NLP/TempOutputSpeech/" + currentID + ".wav"

    with sf.SoundFile(name, mode='w', samplerate=44100,
                      channels=2) as file:
        # Create an input stream to record audio without a preset time
        with sd.InputStream(samplerate=44100, channels=2, callback=callback):
            while recording == True:
                # Set the variable to True to allow playing the audio later
                file_exists = True
                # write into file
                file.write(q.get())

# To clear the TempOutputSpeech file


def on_closing():
    folder = 'NLP/TempOutputSpeech'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    voice_rec.destroy()


def change_appearance_mode(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)


def getInput():
    global arrayi
    file1 = codecs.open('NLP/input1.txt', 'r', 'utf-8')
    Lines = file1.readlines()
    arrayi = Lines


getInput()

voice_rec = customtkinter.CTk()

voice_rec.geometry("780x520")
voice_rec.title("Medical Data Collection")
voice_rec.grid_columnconfigure(0, weight=1)
voice_rec.grid_rowconfigure((0, 1), weight=1)

frame_info = customtkinter.CTkFrame(master=voice_rec, corner_radius=20)
frame_info.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
frame_info.columnconfigure(0, weight=1)
frame_info.rowconfigure(0, weight=1)
title_lbl = customtkinter.CTkLabel(master=frame_info,
                                   text=mytext,
                                   text_font=("Roboto Medium", -16),
                                   height=50,
                                   corner_radius=6,
                                   fg_color=("white", "gray38"))
title_lbl.grid(column=0, row=0, sticky="nswe", padx=15, pady=15)
frame_down = customtkinter.CTkFrame(
    master=voice_rec, width=180, corner_radius=20)
frame_down.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
frame_down.columnconfigure((0, 1, 2, 3, 4), weight=1)
frame_down.rowconfigure(0, weight=1)

record_btn = customtkinter.CTkButton(master=frame_down,
                                     text="Record",  
                                     command=lambda m=1: threading_rec(m))
record_btn.grid(row=0, column=0, pady=10, padx=20)

stop_btn = customtkinter.CTkButton(master=frame_down,
                                   text="Stop",
                                   command=lambda m=2: threading_rec(m) )
stop_btn.grid(row=0, column=1, pady=10, padx=20)

play_btn = customtkinter.CTkButton(master=frame_down,
                                   text="Play",
                                   command=lambda m=3: threading_rec(m))
play_btn.grid(row=0, column=2, pady=10, padx=20)

next_btn = customtkinter.CTkButton(master=frame_down,
                                   text="Next/Skip",
                                   command=lambda m=4: threading_rec(m))
next_btn.grid(row=0, column=4, pady=10, padx=20)

upload_btn = customtkinter.CTkButton(master=frame_down,
                                     text="Upload",
                                     command=lambda m=5: threading_rec(m))
upload_btn.grid(row=0, column=3, pady=10, padx=20)

label_mode = customtkinter.CTkLabel(text="Appearance Mode:")
label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

optionmenu_1 = customtkinter.CTkOptionMenu(values=["Light", "Dark", "System"],
                                           command=change_appearance_mode)
optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")
optionmenu_1.set("Dark")
voice_rec.protocol("WM_DELETE_WINDOW", on_closing)
voice_rec.mainloop()
