import os
import sys
import turtle
import random
from turtle import Canvas
from tkinter import (
    Label,
    Button,
    PhotoImage,
    Listbox,
    filedialog,
    ttk,
    END,
    BOTTOM,
    HORIZONTAL,
    ACTIVE,
    Tk,
    LEFT,
    E,
    Y,
    StringVar,
)
from tkinter import messagebox as mb

import pygame
from pygame import mixer

mixer.init()

playing = False
paused = False
mute = False
cur_playing = ""
con_style = "rand"
to_break = False
current_time = 0


class Main_class:
    songs = []
    play_thread = None

    def about(self):
        mb.showinfo()

    def set_playlist(self):
        music_ex = ["mp3", "wav", "mpeg", "m4a", "wma", "ogg"]
        dir_ = filedialog.askdirectory(initialdir="D:\\", title="Select Directory")
        os.chdir(dir_)
        status_bar["text"] = "Playlist Updated."
        dir_files = os.listdir(dir_)
        self.songs.clear()
        for file in dir_files:
            exten = file.split(".")[-1]
            for ex in music_ex:
                if exten == ex:
                    self.songs.append(file)
        self.songsvar.set(self.songs)

    def con_func(self, con):
        global cur_playing
        global current_time
        current_time = 0
        if con == "rand":
            in_ = random.randint(0, len(self.songs))
            next_play = self.songs[in_]
            self.play_next(next_play)
        elif con == "rep_all":
            in_ = self.songs.index(cur_playing)
            next_play = self.songs[in_ + 1]
            self.play_next(next_play)
        else:
            self.play_next(cur_playing)

    def shuffle_list(self):
        random.shuffle(self.songs)
        self.songsvar.set(self.songs)

    def play_next(self, song):
        global playing
        global cur_playing
        global file
        file = song
        cur_playing = file
        mixer.music.load(file)
        mixer.music.play()
        status_bar["text"] = "Playing - " + file
        playing = True

    def playSongInitial(self, *args):
        self.stop()
        self.play_music()

    def play_music(self):
        global playing
        global cur_playing
        if not playing:
            global file
            file = play_list.get(ACTIVE)
            cur_playing = file
            mixer.music.load(file)
            mixer.music.play()
            status_bar["text"] = "Playing - " + file
            play_button["image"] = play_img
            playing = True
        if not pygame.mixer.music.get_busy():
            mixer.music.play()
        else:
            global paused
            if paused:
                mixer.music.unpause()
                paused = False
                status_bar["text"] = "Playing - " + file

    def stop(self):
        mixer.music.stop()
        global playing
        global paused
        global dur_start
        global progress_bar
        global cur_playing
        global current_time
        global to_break
        to_break = True
        current_time = 0
        cur_playing = ""
        playing = False
        paused = False
        progress_bar["value"] = 0.0
        progress_bar.update()
        play_button["image"] = play_img
        status_bar["text"] = "Music Stopped"
        to_break = False

        return None

    def next_prev(self, num):
        global file
        global playing
        global to_break
        global dur_start
        to_break = True
        dur_start["text"] = "00:00"
        try:
            if num == 1:
                index = self.songs.index(file) - 1
                file = self.songs[index]
                mixer.music.load(file)
                mixer.music.play()
                status_bar["text"] = "Playing - " + file
                play_button["image"] = play_img
                playing = True
            else:
                index = self.songs.index(file) + 1
                file = self.songs[index]
                mixer.music.load(file)
                mixer.music.play()
                status_bar["text"] = "Playing - " + file
                play_button["image"] = play_img
                playing = True
        except IndexError:
            self.play_music()
        except ValueError:
            global paused
            playing = False
            paused = False
            self.play_music()

    def open_file(self):
        dir_ = filedialog.askopenfilename(initialdir="D:/", title="Select File")
        cng_dir = dir_.split("/")[0:-1]
        cng_dir = "".join(cng_dir)
        os.chdir(cng_dir)
        self.songs.append(dir_)
        filename = os.path.basename(dir_)
        play_list.insert(END, filename)
        global playing
        playing = False

    def speaker_func(self):
        global mute
        global status_bar
        if not mute:
            speaker["image"] = mute_img
            mixer.music.set_volume(0.0)
            mute = True
        else:
            speaker["image"] = speaker_img
            num = scale.get()
            mixer.music.set_volume(float(num) / 100)
            mute = False

    def set_vol(self, num):
        global mute
        global status_bar
        if num == float(0):
            speaker["image"] = mute_img
            mixer.music.set_volume(0.0)
            mute = True
        elif mute:
            speaker["image"] = speaker_img
            num = scale.get()
            mixer.music.set_volume(float(num) / 100)
            mute = False
        else:
            volume = float(num) / 100
            mixer.music.set_volume(volume)

    def exit(self):
        self.stop()
        app.destroy()
        sys.exit()

    # GUI
    def __init__(self):
        global app
        app = Tk()
        app.geometry("800x520")
        app.configure(bg="#3b4954")
        app.resizable(0, 0)
        app.title("VikPlayer")
        app.wm_attributes("-alpha", 0.95)
        self.songs = []
        self.songsvar = StringVar(value=self.songs)
        # for turtle-Visualiser
        canvas = Canvas(app)
        canvas.config(width=500, height=200)
        canvas.pack(side=LEFT)
        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor("#1d2226")
        go_turtle = turtle.RawTurtle(screen, shape="circle")

        # Playlist Frame
        Label(app, text="", bg="Black", height=19, width=35, relief_="ridge").place(
            x=543, y=0
        )

        Button(
            app,
            text="Add a Folder.",
            bd=2,
            font=("arialblack", 13),
            width=25,
            command=self.set_playlist,
        ).place(x=552, y=10)

        global play_list
        play_list = Listbox(app, listvariable=self.songsvar, height=21, width=41)
        play_list.place(x=544, y=50)
        play_list.bind("<Double-Button>", self.playSongInitial)

        Label(app, bg="#373e42", text="", height=5, relief_="raised", width=200).place(
            x=0, y=395
        )

        global play_img
        play_img = PhotoImage(file="icons/play.png")

        global play_button
        play_button = Button(app, image=play_img, bd=0, command=self.play_music)
        play_button.place(x=10, y=433)

        prev_img = PhotoImage(file="icons/prev.png")
        prev_button = Button(
            app, image=prev_img, bd=0, command=lambda: self.next_prev(1)
        )
        prev_button.place(x=50, y=433)

        stop_img = PhotoImage(file="icons/stop.png")
        stop_button = Button(app, image=stop_img, bd=1, command=self.stop)
        stop_button.place(x=90, y=433)

        next_img = PhotoImage(file="icons/next.png")
        next_button = Button(
            app, image=next_img, bd=0, command=lambda: self.next_prev(2)
        )
        next_button.place(x=130, y=433)

        global pause_img
        pause_img = PhotoImage(file="icons/pause.png")

        global speaker_img
        speaker_img = PhotoImage(file="icons/vol.png")

        global mute_img
        mute_img = PhotoImage(file="icons/mute.png")

        global speaker
        speaker = Button(app, image=speaker_img, bd=0, command=self.speaker_func)
        speaker.place(x=650, y=442)

        shuffle_img = PhotoImage(file="icons/shuffle.png")
        shuffle_button = Button(app, image=shuffle_img, bd=0, command=self.shuffle_list)
        shuffle_button.place(x=170, y=433)

        # Volume Scale - adjust volume
        global scale
        scale = ttk.Scale(app, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol)
        scale.set(70)  # implement the default value of scale when music player starts
        mixer.music.set_volume(0.7)
        scale.place(x=680, y=440)

        # Time Durations
        global dur_start, dur_end
        dur_start = Label(app, text="--:--", font=("Calibri", 10, "bold"))
        dur_start.place(x=5, y=400)
        dur_end = Label(app, text="--:--", font=("Calibri", 10, "bold"))
        dur_end.place(x=750, y=400)

        # # Progress Bar - The progress bar which indicates the running music
        global progress_bar
        progress_bar = ttk.Progressbar(app, orient="horizontal", length=705)
        progress_bar.place(x=42, y=400)

        # Status Bar - at the bottom of window
        global status_bar
        status_bar = Label(
            app, text="Welcome to ViksMusicPlayer!", relief_="raised", anchor=E
        )
        status_bar.pack(side=BOTTOM, fill=Y)
        app.protocol("WM_DELETE_WINDOW", self.exit)

        # visualiser

        def visualiser():
            go_turtle.hideturtle()
            go_turtle.speed(450)
            r = 5
            colors = [
                "purple",
                "red",
                "teal",
                "pink",
                "orange",
                "white",
                "blue",
                "green",
            ]
            for x in range(90):
                x = random.randint(-100, 150)
                options = [1, 2, 3, 4, 5, 6]
                for g in range(50):
                    go_turtle.pencolor(colors[g % 8])
                    movement = random.choice(options)
                    if movement == 1:
                        go_turtle.forward(x)
                    if movement == 2:
                        go_turtle.backward(x)
                    if movement == 3:
                        go_turtle.left(x)
                    if movement == 4:
                        go_turtle.right(x)
                    if movement == 5:
                        for c in range(10):
                            go_turtle.circle(r + x, 25)
                    else:
                        go_turtle.setposition(x, g)
                go_turtle.clear()

        visualiser()

        app.mainloop()


music_player = Main_class()
