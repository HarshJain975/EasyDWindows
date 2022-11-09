import tkinter as tk
from tkinter import ttk
from tkinter import *
from collections import deque
import pygame


# initialize Pygame Mixer
pygame.mixer.init()


def stop_timer_sound():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("./frames/PS5 Intro Theme 2.mp3")
    pygame.mixer.music.play()


class Timer(ttk.Frame):  # we are calling super class to make self into the frame
    def __init__(self, parent, controller, show_settings, show_chatapp, show_welcome, background):
        super().__init__(parent)

        self["style"] = "Background.TFrame"  # assigning Background style

        # def play_sound_2():
        #     playsound("Music_2.mp3", block=False)
        #
        # play_sound_2()

        labelframe = LabelFrame(self, background=background, borderwidth=10)
        labelframe.pack(fill="both", expand=True, pady=(20, 0), padx=5)

        self.controller = controller
        pomodoro_time = int(controller.pomodoro.get())
        self.current_time = tk.StringVar(value=f"{pomodoro_time:02d}:00")
        self.current_timer_label = tk.StringVar(value=controller.timer_schedule[0])
        self.timer_running = False   # timer will be running only when this is true
        # allow us to create start and stop button
        self._timer_decrement_job = None    # private variable

        timer_description = ttk.Label(labelframe,
                                      textvariable=self.current_timer_label,
                                      style="LightText.TLabel",
                                      font="Courier 80")

        timer_description.pack(expand=True, fill="both", padx=50, pady=(10, 10))

        # Label Frame 1
        labelframe_1 = LabelFrame(labelframe)
        labelframe_1.pack(fill="both", expand=False, pady=(5, 50))

        # settings button calling show_settings function in app.py (lambda function)
        settings_button = ttk.Button(labelframe_1,
                                     text="Settings",
                                     command=show_settings,
                                     style="PomodoroButton.TButton",
                                     cursor="hand2")
        settings_button.pack(expand=True, fill="both", anchor="w", padx=50, pady=(30, 10))

        # back button calling show_timer function in app.py (lambda function)

        back_button = ttk.Button(labelframe_1,
                                    text="Back",
                                    command=lambda: [show_welcome(), stop_timer_sound()],
                                    style="PomodoroButton.TButton",
                                    cursor="hand2")
        back_button.pack(expand=True, fill="both", padx=50, pady=(10, 10))

        # chatapp button calling show_timer function in app.py (lambda function)

        chatapp_button = ttk.Button(labelframe_1,
                                    text="ChatApp",
                                    command=show_chatapp,
                                    style="PomodoroButton.TButton",
                                    cursor="hand2")
        chatapp_button.pack(expand=True, fill="both", padx=50, pady=(10, 30))

        # Timer Frame
        timer_frame = ttk.Frame(labelframe,
                                height="100",
                                style="Background.TFrame")  # frame for label
        timer_frame.pack(expand=True, fill="both", pady=(20, 0))   # added padding

        timer_counter = ttk.Label(timer_frame,
                                  textvariable=self.current_time,
                                  style="TimerText.TLabel")  # label inside timer frame
        timer_counter.place(relx=0.5, rely=0.5, anchor="center")  # to place frame at the center of the container timer_counter

        labelframe_1 = LabelFrame(labelframe)
        labelframe_1.pack(fill="both", expand=True, pady=(50, 0), padx=0)

        button_container = ttk.Frame(labelframe_1,
                                     padding=10,
                                     style="Background.TFrame")
        button_container.pack(expand=True, fill="both")
        button_container.columnconfigure((0, 1, 2), weight=1)

        self.start_button = ttk.Button(button_container,
                                       text="Start",
                                       command=self.start_timer,
                                       style="PomodoroButton.TButton",
                                       cursor="hand2")  # start button container
        self.start_button.grid(row=0, column=0, ipadx=80, ipady=10, pady=(50, 0))

        self.stop_button = ttk.Button(button_container,
                                      text="Stop",
                                      state="disabled",
                                      command=self.stop_timer,
                                      style="PomodoroButton.TButton",
                                      cursor="hand2")  # stop button container
        self.stop_button.grid(row=0, column=1, ipadx=80, ipady=10, pady=(50, 0))

        reset_button = ttk.Button(button_container,
                                  text="Reset",
                                  command=self.reset_timer,
                                  style="PomodoroButton.TButton",
                                  cursor="hand2")
        reset_button.grid(row=0, column=2, ipadx=80, ipady=10, pady=(50, 0))

    def start_timer(self):  # start timer function
        self.timer_running = True
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "enabled"
        self.decrement_time()

    def stop_timer(self):   # stop timer function
        self.timer_running = False
        self.start_button["state"] = "enabled"
        self.stop_button["state"] = "disabled"

        if self._timer_decrement_job:   # take care of bug where timer can have multiple different jobs running at the same time
            self.after_cancel(self._timer_decrement_job)
            self._timer_decrement_job = None

    def reset_timer(self):
        self.stop_timer()
        pomodoro_time = int(self.controller.pomodoro.get())
        self.current_time.set(f"{pomodoro_time:02d}:00")
        self.controller.timer_schedule = deque(self.controller.timer_order)
        self.current_timer_label.set(self.controller.timer_schedule[0])

    def decrement_time(self):   # decrement time function to reducing the time label
        current_time = self.current_time.get()  # string of the value inside self.current_Time

        if self.timer_running and current_time != "00:00":  # timer running and end not reached yet
            minutes, seconds = current_time.split(":")  # taking values of minutes seconds and
            # decreasing them separately

            if int(seconds) > 0:    # second = 0 that means seconds should be 59
                seconds = int(seconds) - 1
                minutes = int(minutes)
            else:
                seconds = 59
                minutes = int(minutes) - 1

            self.current_time.set(f"{minutes:02d}:{seconds:02d}")   # 02d to format them to 2 digits
            # 5 will be 05

            self._timer_decrement_job = self.after(1000, self.decrement_time)   # call after method of the frame
            # takes time in milliseconds that tells tkinter that after specified amount of time
            # it has to run the specified function.
        elif self.timer_running and current_time == "00:00":
            self.controller.timer_schedule.rotate(-1)  # takes the first value and move it to the end
            next_up = self.controller.timer_schedule[0]
            self.current_timer_label.set(next_up)   # changes the value in the label

            if next_up == "Pomodoro":
                pomodoro_time = int(self.controller.pomodoro.get())
                self.current_time.set(f"{pomodoro_time:02d}:00")
            elif next_up == "Short Break":
                short_break_time = int(self.controller.short_break.get())
                self.current_time.set(f"{short_break_time:02d}:00")
            elif next_up == "Long Break":
                long_break_time = int(self.controller.long_break.get())
                self.current_time.set(f"{long_break_time:02d}:00")

            self._timer_decrement_job = self.after(1000, self.decrement_time)

