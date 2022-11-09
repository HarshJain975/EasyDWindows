import tkinter as tk
from tkinter import ttk
import datetime
from PIL import Image, ImageTk
import os

MAX_MESSAGE_WIDTH = 800


class MessageWindow(tk.Canvas):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)  # container is the frame the canvas is gonna be in

        self.message_frame = ttk.Frame(self, style="Messages.TFrame")
        self.message_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.message_frame, anchor="nw")

        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.message_frame.bind("<Configure>", configure_scroll_region)
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")

        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)  # to make sure contents are always in the same place upon opening the application

    def _on_mousewheel(self, event):    # function for scrolling with mouse wheel
        self.yview_scroll(-int(event.delta/1200), "units")

    def update_message_widgets(self, messages, message_labels):
        existing_labels = [
            (message["text"], time["text"]) for message, time in message_labels]   # to find what labels we already have, will contain the text content of each label
        # the above method avoid duplicate messages

        for message in messages:    # loop going through all the messages received through server and adding a label for each message content
            message_time = datetime.datetime.fromtimestamp(message["date"]).strftime(
                "%d-%m-%Y %H:%M:%S"  # day-month-year Hour-Minute-Second
            )     # create a datetime object, and turn it into a string

            if (message["message"], message_time) not in existing_labels:
                self._create_message_container(message["message"], message_time, message_labels)    # call to create message container and message content

    def _create_message_container(self, message_content, message_time, message_labels): # responsible for creating container and calling the next methods that creates the actual contents
        container = ttk.Frame(self.message_frame, style="Messages.TFrame")  # new frame and time label
        container.columnconfigure(1, weight=1)
        container.grid(sticky="EW", padx=(10, 50), pady=10)

        def reconfigure_message_labels(event):  # checks whether the label should change size whenever container size varies
            for label, _ in message_labels:
                label.configure(wraplength=min(container.winfo_width() - 130, MAX_MESSAGE_WIDTH))

        container.bind("<Configure>", reconfigure_message_labels)
        self._create_message_bubble(container, message_content, message_time, message_labels)   # creates the actual contents

    def _create_message_bubble(self, container, message_content, message_time, message_labels):
        cd = os.getcwd()
        file_with_path = os.path.join("frames/male_img.jpg")
        avatar_image = Image.open(file_with_path)  # image
        avatar_photo = ImageTk.PhotoImage(avatar_image)  # create a tkinter compatible image

        avatar_label = ttk.Label(container,     # avatar label
                                 image=avatar_photo,
                                 style="Avatar.TLabel")
        avatar_label.image = avatar_photo   # creates image property inside avatar_label as a custom property
        # as long as the label is kept in tkinter the photo will not be garbage collected

        avatar_label.grid(row=0, column=0, rowspan=2, sticky="NEW", padx=(0, 10), pady=(5, 0))

        time_label = ttk.Label(container,  # time label
                               text=message_time,
                               style="Time.TLabel")
        time_label.grid(row=0, column=1, sticky="NEW")

        message_label = ttk.Label(container,  # message label
                                  text=message_content,
                                  wraplength=800,
                                  anchor="w",
                                  justify="left",
                                  style="Message.TLabel")
        message_label.grid(row=1, column=1, sticky="NSEW")

        message_labels.append(
            (message_label, time_label))  # list of tuples each containing two labels message and the time
