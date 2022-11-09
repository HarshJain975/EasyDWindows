from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import os


# initialize Pygame Mixer
pygame.mixer.init()


def play_sound_start_page():
    pygame.mixer.music.load("./frames/PS5 Intro Theme Start Page 4.mp3")
    pygame.mixer.music.play()


def play_sound_start_button():
    pygame.mixer.music.load("./frames/PS5 Intro Theme 2.mp3")
    pygame.mixer.music.play()


class Start(ttk.Frame):  # we are calling super class to make self into the frame
    def __init__(self, parent, controller, show_welcome, exit, background):
        super().__init__(parent)

        self["style"] = "Background.TFrame"  # assigning Background style

        play_sound_start_page()

        labelframe = LabelFrame(self, background=background, borderwidth=10)
        labelframe.pack(fill="both", expand=True, pady=(20, 0), padx=5)

        cd = os.getcwd()
        file_with_path = os.path.join(cd, os.sep, r'Project MA\Assets\3.jpeg')
        welcome_image = Image.open(file_with_path)
        welcome_image.resize(size=(10, 10))
        welcome_photo = ImageTk.PhotoImage(welcome_image)

        # image_label = ttk.Label(labelframe, image=welcome_photo, style="Avatar.TLabel")
        # image_label.pack(expand=True, fill="both")

        welcome_photo_label = ttk.Label(labelframe, image=welcome_photo)
        welcome_photo_label.image = welcome_photo

        # label1.place(x=35, y=10)
        welcome_photo_label.pack(expand=True, padx=0, pady=(50, 20))

        welcome_description = ttk.Label(labelframe,
                                        text="Welcome! Click on the buttons below to navigate. Enjoy......!",
                                        style="LightText.TLabel",
                                        )
        welcome_description.pack(expand=True, anchor="center")

        # start button
        start_button = ttk.Button(labelframe,
                                  text="Start",
                                  command=lambda: [show_welcome(), play_sound_start_button()],
                                  style="PomodoroButton.TButton",
                                  cursor="hand2")
        start_button.pack(expand=True, fill="y", pady=(30, 10), ipadx=200)

        # chatapp button calling exit_function function in app.py (lambda function)
        exit_button = ttk.Button(labelframe,
                                 text="Exit",
                                 command=exit,
                                 style="PomodoroButton.TButton",
                                    cursor="hand2")
        exit_button.pack(expand=True, fill="y", pady=(10, 60), ipadx=200)

