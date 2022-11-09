import tkinter as tk
from tkinter import ttk


class Settings(ttk.Frame):
    def __init__(self, parent, controller, show_timer):
        super().__init__(parent)

        self["style"] = "Background.TFrame"  # setting the style property for frame

        # spacing and alignment
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        settings_container = ttk.Frame(self,
                                       padding="30 15 30 15",
                                       style="Background.TFrame"
                                       )

        settings_container.grid(row=0, column=0, sticky="EW", padx=10, pady=(80, 40))

        settings_container.columnconfigure(0, weight=1)
        settings_container.rowconfigure(1, weight=1)

        pomodoro_label = ttk.Label(settings_container,
                                   text="Pomodoro: ",
                                   style="LightText.TLabel",
                                   font="Courier 20")
        pomodoro_label.grid(column=0, row=0, sticky="W")

        pomodoro_input = tk.Spinbox(settings_container,
                                    from_=0,
                                    to=120,
                                    increment=1,
                                    justify="center",
                                    textvariable=controller.pomodoro,
                                    width=10,
                                    font="Courier 20")
        pomodoro_input.grid(column=1, row=0, sticky="EW")
        pomodoro_input.focus()

        long_break_label = ttk.Label(settings_container,
                                     text="Long break time: ",
                                     style="LightText.TLabel",
                                     font="Courier 20")
        long_break_label.grid(column=0, row=1, sticky="W")

        long_break_input = tk.Spinbox(settings_container,
                                      from_=0,
                                      to=60,
                                      increment=1,
                                      justify="center",
                                      textvariable=controller.long_break,
                                      width=10,
                                      font="Courier 20")
        long_break_input.grid(column=1, row=1, sticky="EW")

        short_break_label = ttk.Label(settings_container,
                                      text="Short break time: ",
                                      style="LightText.TLabel",
                                      font="Courier 20")
        short_break_label.grid(column=0, row=2, sticky="W")

        short_break_input = tk.Spinbox(settings_container,
                                       from_=0,
                                       to=60,
                                       increment=1,
                                       justify="center",
                                       textvariable=controller.short_break,
                                       width=10,
                                       font="Courier 20")
        short_break_input.grid(column=1, row=2, sticky="EW")

        for child in settings_container.winfo_children():
            # to add padding in all of the labels and spinboxes in settings container
            child.grid_configure(padx=5, pady=5)    # adds padding 5 pixels in Left-Right and Top-Bottom

        # button container
        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(sticky="EW", padx=10)
        button_container.columnconfigure(0, weight=1)

        # timer button
        timer_button = ttk.Button(button_container,
                                  text="Back",
                                  command=show_timer,
                                  style="PomodoroButton_1.TButton",
                                  cursor="hand2")
        timer_button.grid(column=0, row=0, sticky="EW", padx=2)
