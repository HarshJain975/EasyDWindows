from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import os

# def play_sound_4():
#     playsound("PS5 Intro Theme Start Page 3.mp3", block=False)
#
# play_sound_4()


def start_welcome_sound():
    pygame.mixer.music.load("./frames/PS5 Intro Theme 2.mp3")
    pygame.mixer.music.play()


def start_media_player_sound():
    pygame.mixer.music.load("./frames/PSP Startup 2.mp3")
    pygame.mixer.music.play()


def stop_sound():
    pygame.mixer.music.stop()


def stop_welcome_sound():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("./frames/PS5 Intro Theme Start Page 4.mp3")
    pygame.mixer.music.play()


def play_timer_sound():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("./frames/Playstation 2 System Menu Ambience.mp3")
    pygame.mixer.music.play()
    # playsound("PS2 Startup Sound.mp3", block=False)


class Welcome(ttk.Frame):  # we are calling super class to make self into the frame
    def __init__(self, parent, controller, show_timer, show_chatapp, show_map, media_player, exit, background):
        super().__init__(parent)

        self["style"] = "Background.TFrame"  # assigning Background style

        labelframe = LabelFrame(self, background=background, borderwidth=10)
        labelframe.pack(fill="both", expand=True, pady=(20, 0), padx=5)

        cd = os.getcwd()
        file_with_path = os.path.join(cd, os.sep, r'Project MA\Assets\3.jpeg')
        welcome_image = Image.open(file_with_path)
        welcome_image_resized = welcome_image.resize(size=(500, 180))
        welcome_photo = ImageTk.PhotoImage(welcome_image_resized)

        # image_label = ttk.Label(labelframe, image=welcome_photo, style="Avatar.TLabel")
        # image_label.pack(expand=True, fill="both")

        welcome_photo_label = ttk.Label(labelframe, image=welcome_photo)
        welcome_photo_label.image = welcome_photo

        # label1.place(x=35, y=10)
        welcome_photo_label.pack(expand=True, padx=40, pady=(47, 20))

        welcome_description = ttk.Label(labelframe,
                                        text="Welcome! Click on the buttons below to navigate. Enjoy......!",
                                        style="LightText.TLabel",
                                        )
        welcome_description.pack(expand=True, anchor="center")

        # timer button
        timer_button = ttk.Button(labelframe,
                                  text="Timer",
                                  command=lambda: [show_timer(), play_timer_sound()],
                                  style="PomodoroButton.TButton",
                                  cursor="hand2")
        timer_button.pack(expand=True, fill="y", pady=(20, 10), ipadx=200)

        # chatapp button calling show_timer function in app.py (lambda function)
        chatapp_button = ttk.Button(labelframe,
                                    text="ChatApp",
                                    command=lambda: [show_chatapp(), stop_sound()],
                                    style="PomodoroButton.TButton",
                                    cursor="hand2")
        chatapp_button.pack(expand=True, fill="y", pady=(10,10), ipadx=200)

        # map button calling show_timer function in app.py (lambda function)
        map_button = ttk.Button(labelframe,
                                text="Navigator",
                                command=lambda: [show_map(), stop_sound()],
                                style="PomodoroButton.TButton",
                                cursor="hand2")
        map_button.pack(expand=True, fill="y", pady=(10, 10), ipadx=200)

        # media player button calling show_media_player function in app.py (lambda function)
        media_player_button = ttk.Button(labelframe,
                                         text="Media Player",
                                         command=lambda: [media_player(), start_media_player_sound()],
                                         style="PomodoroButton.TButton",
                                         cursor="hand2")
        media_player_button.pack(expand=True, fill="y", pady=(10, 10), ipadx=200)

        # chatapp button calling exit_function function in app.py (lambda function)
        back_button = ttk.Button(labelframe,
                                 text="<-",
                                 command=lambda: [exit(), stop_welcome_sound()],
                                 style="PomodoroButton.TButton",
                                 cursor="hand2")
        back_button.pack(expand=True, fill="y", pady=(10, 20), ipadx=200)

        labelframe_1 = LabelFrame(labelframe)
        labelframe_1.pack(fill="both", expand=True, pady=(20, 0), padx=0)

        # plat button calling exit_function function in app.py (lambda function)
        play_button = ttk.Button(labelframe_1,
                                 text="|> PLAY",
                                 command=lambda: [start_welcome_sound()],
                                 style="PomodoroButton.TButton",
                                 cursor="hand2")
        play_button.grid(row=0, column=0, padx=20, pady=(30, 10))

        # pause button calling exit_function function in app.py (lambda function)
        pause_button = ttk.Button(labelframe_1,
                                  text="|| PAUSE",
                                  command=lambda: [stop_sound()],
                                  style="PomodoroButton.TButton",
                                  cursor="hand2")
        pause_button.grid(row=0, column=1, padx=650, pady=(30, 10))



