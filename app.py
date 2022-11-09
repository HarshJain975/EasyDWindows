import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from collections import deque
from windows import set_dpi_awareness
from frames import Timer, Settings, Chat, Welcome, MediaPlayer, Start, Maps


"""*************************************"""
# other way of importing the frames
# from frames.timer import Timer
# from frames.settings import Settings
"""*************************************"""

set_dpi_awareness()

# colors
COLOR_PRIMARY = "#2e3f4f"
COLOR_SECONDARY = "#293846"
COLOR_LIGHT_BACKGROUND = "#fff"
COLOR_LIGHT_TEXT = "#eee"
COLOR_DARK_TEXT = "#8095a8"

# chatapp style

COLOR_LIGHT_BACKGROUND_1 = "#fff"
COLOR_LIGHT_BACKGROUND_2 = "#f2f3f5"
COLOR_LIGHT_BACKGROUND_3 = "#e3e5e8"

COLOR_LIGHT_TEXT_CHATAPP = "#aaa"

COLOR_BUTTON_NORMAL = "#5fba7d"
COLOR_BUTTON_ACTIVE = "58c77c"
COLOR_BUTTON_PRESSED = "#44e378"


def exit_function():
    app.destroy()


class PomodoroTimer(tk.Tk):  # class that inherits from tk.Tk
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # super class init method which makes self == tk object.

        # STYLE DATABASE

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Timer.TFame", background=COLOR_LIGHT_BACKGROUND)  # new style Timer.TFrame
        style.configure("Background.TFrame", background=COLOR_PRIMARY)
        style.configure("TimerText.TLabel",
                        background=COLOR_LIGHT_BACKGROUND,
                        foreground=COLOR_DARK_TEXT,
                        font="Courier 80")  # countdown time text, for specific element
        style.configure("LightText.TLabel",
                        background=COLOR_PRIMARY,
                        foreground=COLOR_DARK_TEXT, )  # can be used universally in app
        style.configure("PomodoroButton.TButton",
                        background=COLOR_SECONDARY,
                        foreground=COLOR_LIGHT_TEXT)    # color for button
        style.map("PomodoroButton.TButton",
                  background=[("active", COLOR_PRIMARY), ("disabled", COLOR_LIGHT_TEXT)])

        style.configure("PomodoroButton_1.TButton",
                        background=COLOR_SECONDARY,
                        foreground=COLOR_LIGHT_TEXT,
                        font="Courier 20")  # color for button
        style.map("PomodoroButton_1.TButton",
                  background=[("active", COLOR_PRIMARY), ("disabled", COLOR_LIGHT_TEXT)])

        font.nametofont("TkDefaultFont").configure(size=14)

        # chatapp style
        style_1 = ttk.Style(self)
        style_1.theme_use("clam")

        style_1.configure("Message.TFrame", background=COLOR_LIGHT_BACKGROUND_3)

        style_1.configure("Controls.TFrame", background=COLOR_LIGHT_BACKGROUND_2)

        style_1.configure("SendButton.TButton", borderwidth=0, background=COLOR_BUTTON_NORMAL)

        style_1.map("SendButton.TButton", background=[("pressed", COLOR_BUTTON_PRESSED), ("active", COLOR_BUTTON_ACTIVE)])

        style_1.configure("FetchButton", background=COLOR_LIGHT_BACKGROUND_1, borderwidth=0)

        style_1.configure("Time.TLabel", padding=5, background=COLOR_LIGHT_BACKGROUND_1, font=8)

        style_1.configure("Avatar.TLabel", background=COLOR_LIGHT_BACKGROUND_3)

        style_1.configure("Message.TLabel", background=COLOR_LIGHT_BACKGROUND_2)

        # changes color of button on cursor hover
        self["background"] = COLOR_PRIMARY

        self.title("Pomodoro Timer")
        self.columnconfigure(0, weight=1)   # take all the available space
        self.rowconfigure(1, weight=1)

        self.pomodoro = tk.StringVar(value=25)
        self.long_break = tk.StringVar(value=15)
        self.short_break = tk.StringVar(value=5)

        self.timer_order = ["Pomodoro", "Short Break", "Pomodoro", "Short Break", "Pomodoro", "Long Break"]
        # to update and move values at the end we use deque
        self.timer_schedule = deque(self.timer_order)

        container = ttk.Frame(self)
        container.grid()
        container.columnconfigure(0, weight=1)

        self.frames = dict()

        # frames for app

        # start frame
        Start_frame = Start(container, self, lambda: self.show_frame(Welcome), exit_function, background=COLOR_PRIMARY)  # welcome frame
        Start_frame.grid(row=0, column=0, sticky="NESW")  # takes up the entire space available

        # timer frame
        timer_frame = Timer(container, self, lambda: self.show_frame(Settings), lambda: self.show_frame(Chat), lambda: self.show_frame(Welcome),  background=COLOR_PRIMARY)  # timer frame
        timer_frame.grid(row=0, column=0, sticky="NESW")    # takes up the entire space available

        # settings frame
        Settings_frame = Settings(container, self, lambda: self.show_frame(Timer))  # settings frame
        Settings_frame.grid(row=0, column=0, sticky="NESW")  # takes up the entire space available

        # chat frame
        Chat_frame = Chat(container, lambda: self.show_frame(Welcome), background=COLOR_LIGHT_BACKGROUND_1)  # chatapp frame
        Chat_frame.grid(row=0, column=0, sticky="NESW")  # takes up the entire space available

        Welcome_frame = Welcome(container, self, lambda: self.show_frame(Timer), lambda: self.show_frame(Chat), lambda: self.show_frame(Maps), lambda: self.show_frame(MediaPlayer), lambda: self.show_frame(Start), background=COLOR_PRIMARY)  # welcome frame
        Welcome_frame.grid(row=0, column=0, sticky="NESW")  # takes up the entire space available

        Map_frame = Maps(container, self, lambda: self.show_frame(Welcome))  # Game intro frame
        Map_frame.grid(row=0, column=0, sticky="NESW")  # takes up the entire space available

        Media_player_frame = MediaPlayer(container, self, lambda: self.show_frame(Welcome), background=COLOR_PRIMARY)  # media player frame
        Media_player_frame.grid(row=0, column=0, sticky="NESW")  # takes up the entire space available

        self.frames[Start] = Start_frame
        self.frames[Welcome] = Welcome_frame
        self.frames[Timer] = timer_frame
        self.frames[Settings] = Settings_frame
        self.frames[Chat] = Chat_frame
        self.frames[Maps] = Map_frame
        # self.frames[Game] = Game_frame
        self.frames[MediaPlayer] = Media_player_frame

        self.show_frame(Start)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


app = PomodoroTimer()
app.geometry("1000x920")    # x
app.minsize(80, 900)
app.resizable(True, True)
app.mainloop()
