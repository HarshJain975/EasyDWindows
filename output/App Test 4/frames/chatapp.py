import tkinter as tk
from tkinter import ttk
import requests
from frames.message_window import MessageWindow
import pygame

messages = [{"message": "Hello, world", "date": 15498487}]
message_labels = []  # will contain labels


def message_sent_sound():
    pygame.mixer.music.load("./frames/iPhone Text Message Sent.mp3")
    pygame.mixer.music.play()


def start_welcome_sound():
    pygame.mixer.music.load("./frames/PS5 Intro Theme 2.mp3")
    pygame.mixer.music.play()


class Chat(ttk.Frame):
    def __init__(self, parent, show_welcome, background):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.message_window = MessageWindow(self, background=background)
        self.message_window.grid(row=0, column=0, sticky="NSEW", pady=5)

        input_frame = ttk.Frame(self, style="Controls.TFrame", padding=10)  # input frame
        input_frame.grid(row=1, column=0, sticky="EW")

        self.message_input = tk.Text(input_frame, height=3)
        self.message_input.pack(expand=True, fill="both", side="left", padx=(0, 10))

        message_submit = ttk.Button(input_frame,
                                    style="SendButton.TButton",
                                    text="Send",
                                    command=lambda: [self.post_message(), message_sent_sound()])
        message_submit.pack()

        message_fetch = ttk.Button(input_frame,
                                   text="Fetch",
                                   command=self.get_messages,
                                   style="FetchButton.TButton",
                                   cursor="hand2")  # fetch button
        message_fetch.pack()

        welcome_button = ttk.Button(input_frame,
                                    text="Back",
                                    command=lambda: [show_welcome(), start_welcome_sound()],
                                    style="PomodoroButton.TButton",
                                    cursor="hand2")
        welcome_button.pack()

        self.message_window.update_message_widgets(messages, message_labels)

    def post_message(self):
        body = self.message_input.get("1.0", "end").strip()
        requests.post("http://167.99.63.70/message", json={"message": body})
        self.message_input.delete("1.0", "end")
        self.get_messages()

    def get_messages(self):
        global messages
        messages = requests.get(
            "http://167.99.63.70/messages").json()  # """http://167.99.63.70/messages""" address of API, as data comes back as object, all we want is the message
        self.message_window.update_message_widgets(messages, message_labels)
        self.after(150, lambda: self.message_window.yview_moveto(1.0))

