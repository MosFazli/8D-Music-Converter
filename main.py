# This app programmed by Mostafa Fazli
# for using this program, alongside added belows libraries you should add FFMPEG Files
# 28 January 2022

import soundfile as sf
from os import remove as removeFile
from pydub import AudioSegment
from pedalboard import Pedalboard,Reverb
from tkinter import *
from tkinter.filedialog import askopenfilename

outputFile = "8DMusic"
cycleTime = 8000
jumpingPrecent = 5
panBoundary = 100
maxVol = 6
speedMusic = 0.98
addressFile = ""

win = Tk()

# Set the size of the tkinter window
win.geometry("700x800")
win.configure(bg='grey')
win.title('MP3 8D Converter')
win.attributes("-fullscreen", True)
#win.wm_attributes('-transparentcolor','black')


label = Label(win, text="8D Music Converter",bg='grey', font=('Calibri 30'))
label.pack(pady=20)

label2 = Label(win, text="About program",bg='grey', font=('Calibri 20')).pack()
label2 = Label(win, text="This app make customized 8D Music\n"
                         "for using program suggest you that set this set:\n"
                         "Cycle time between 6,000 to 10,000 (Best 8,000)\n"
                         "Pan boundary between 96 to 100 (Best 100)\n"
                         "Speed of file between 92 to 105 (Best 97)",bg='grey', font=('Calibri 15')).pack(pady=5)
label2 = Label(win, text="programmed by MosFazli",bg='grey', font=('Calibri 10')).pack()

Label(win, text="Output file name:", font=('Calibri 15'),bg='grey' ).pack(pady=(10, 0))
outputFileGet = (Entry(win, width=35))
outputFileGet.pack(pady=(0,5))

Label(win, text="Cycle time: (ms)", font=('Calibri 15'),bg='grey' ).pack(pady=(10, 0))
cycleTimeGet = (Entry(win, width=20))
cycleTimeGet.pack(pady=(0,5))

Label(win, text="Pan boundary: (Percentage)", font=('Calibri 15'),bg='grey' ).pack(pady=(10, 0))
panBoundaryGet = (Entry(win, width=20))
panBoundaryGet.pack(pady=(0,5))

Label(win, text="Speed music: (Percentage)", font=('Calibri 15'),bg='grey' ).pack(pady=(10, 0))
speedMusicGet = (Entry(win, width=20))
speedMusicGet.pack(pady=(0,10))


def convert():
    label = Label(win, text="progress:", bg='grey', font=('Calibri 15')).pack(pady=(5,0))
    win.update()
    try:
        musicFile = AudioSegment.from_file(addressFile)
    except:
        try:
            musicFile = AudioSegment.from_file(addressFile)
        except:
            print("File not Found, Please try again !")
            exit()
    label = Label(win, text="10%", bg='grey', font=('Calibri 15')).pack()
    win.update()
    segmentLenth = int(cycleTime / (panBoundary / jumpingPrecent * 2))
    arr = musicFile[0]
    panLimit = []
    leftLimit = -panBoundary

    for i in range(100):
        if int(leftLimit) >= panBoundary:
            break
        panLimit.append(leftLimit)
        leftLimit += jumpingPrecent

    panLimit.append(panBoundary)

    for i in range(0, len(panLimit)):
        panLimit[i] = panLimit[i] / 100

    temp = 0
    flag = True
    label = Label(win, text="30%", bg='grey', font=('Calibri 15')).pack()
    win.update()

    for i in range(0,len(musicFile) - segmentLenth, segmentLenth):

        frame = musicFile[i:i+segmentLenth]

        if temp == 0 and (not flag):
            flag = True
            temp += 2

        if temp == len(panLimit):
            temp -= 2
            flag = False

        adjust = maxVol - (abs(panLimit[temp]) / (panBoundary / 100) * maxVol)
        frame -= adjust

        if flag:
            panned = frame.pan(panLimit[temp])
            temp += 1

        else:
            panned = frame.pan(panLimit[temp])
            temp -= 1
        arr = arr + panned
    label = Label(win, text="60%", bg='grey', font=('Calibri 15')).pack()
    win.update()

    def changeSpeed(music, speed=1.0):
        soundFrameRate = music._spawn(music.raw_data, overrides={"frame_rate": int(music.frame_rate * speed)})
        global arr
        return soundFrameRate.set_frame_rate(music.frame_rate)

    arr = changeSpeed(arr, speedMusic)
    label = Label(win, text="90%", bg='grey', font=('Calibri 15')).pack()
    with open(f"{outputFile}.wav", "wb") as out_f:
        arr.export(out_f, format="wav")
    audio, sample_rate = sf.read(f"{outputFile}.wav")

    board = Pedalboard(
        [Reverb(room_size=0.75, damping=1, width=0.5, wet_level=0.15, dry_level=0.75)],
        sample_rate=sample_rate,
    )
    effected = board(audio)
    win.update()
    with sf.SoundFile(
        f"./{outputFile}.wav",
        "w",
        samplerate=sample_rate,
        channels=effected.shape[1],
    ) as f:
        f.write(effected)
    win.update()
    AudioSegment.from_wav(f"{outputFile}.wav").export(f"{outputFile}.mp3", format="mp3")
    removeFile(f"{outputFile}.wav")
    # ----------------------------------------------
    label = Label(win, text="Finished", bg='grey', font=('Calibri 15')).pack()
    win.update()
    print("Done!")

def getFile():
    Tk().withdraw()
    global addressFile
    addressFile = askopenfilename()
    print("address of selected file : " + addressFile)
    label = Label(win, text=addressFile, bg='grey', font=('Calibri 20')).pack()
    win.update()

def start():
    global outputFile, cycleTime, panBoundary, speedMusic
    if outputFileGet.get() == "" or cycleTimeGet.get() == "" or panBoundaryGet.get() == "" or speedMusicGet.get() == "":
        label = Label(win, text="Please fill all fields", bg='grey', font=('Calibri 20')).pack(pady=5)
        win.update()
    else:
        outputFile = outputFileGet.get()
        cycleTime = int(cycleTimeGet.get())
        panBoundary = int(panBoundaryGet.get())
        speedMusic = int(speedMusicGet.get()) / 100
        convert()


Button(win, text="Get File" ,font=('Calibri 15') ,bg='blue', command=getFile,pady = 5).pack()
label2 = Label(win, text="",bg='grey', font=('Calibri 5')).pack(pady=2)

Button(win, text="Start Convert" ,font=('Calibri 15') ,bg='green', command=start,pady = 5).pack()
label3 = Label(win, text="",bg='grey', font=('Calibri 5')).pack(pady=2)

Button(win, text="Exit",font=('Calibri 15') ,bg='red', command=win.destroy,pady = 5).pack()

win.mainloop()