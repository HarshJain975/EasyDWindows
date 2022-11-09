from tkinter import ttk
from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3


def start_welcome_sound():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("./frames/PS5 Intro Theme 2.mp3")
    pygame.mixer.music.play()


class MediaPlayer(ttk.Frame):
    def __init__(self, parent, controller, show_welcome, background):
        super().__init__(parent)

        self["style"] = "Background.TFrame"  # assigning Background style

        labelframe = LabelFrame(self, background=background, borderwidth=10)
        labelframe.pack(fill="both", expand=True, pady=(20, 0), padx=5)

        # initialize Pygame Mixer
        pygame.mixer.init()

        # Add Song Function
        # def add_song(self):
        #     song = filedialog.askopenfilename(initialdir='Music/', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"), ))
        #     # strip out the directory info and .mp3 extension from song name
        #     song = song.replace("C:/Users/harsh/Downloads/Timer_File/Music/", "")
        #     song = song.replace(".mp3", "")
        #     # Add song to listbox
        #     song_box.insert(END, song)

        # Grab Song Length Time Info
        def play_time():
            # Check for double timing
            if stopped:
                return
            # Grab current song elapsed time
            current_time = pygame.mixer.music.get_pos() / 1000

            # throw up temporary label to get data
            # slider_label.config(text=f"Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}")

            # Convert to time format
            converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

            # Get the currently playing song
            #current_song = song_box.curselection()
            # Grab song title from playlist
            song = song_box.get(ACTIVE)
            # Add directory structure and mp3 to song title
            song = f"{song}.mp3"
            # Get song length with mutagen
            song_mut = MP3(song)
            # Get song length
            global song_length
            song_length = song_mut.info.length
            # Convert to Time Format
            converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

            current_time += 1

            if int(my_slider.get()) == int(song_length):
                # Output time to status bar till the end (entire length)
                status_bar.config(text=f"Time Elapsed: {converted_song_length}  ")
            elif paused:
                pass
            elif int(my_slider.get()) == int(current_time):
                # slider hasn't been moved
                # Update Slider to Position
                slider_position = int(song_length)

                my_slider.config(to=slider_position, value=int(current_time))

            else:
                # slider has been moved!
                # Update Slider to Position
                slider_position = int(song_length)
                my_slider.config(to=slider_position, value=int(my_slider.get()))

                # Convert to time format
                converted_current_time = time.strftime('%H:%M:%S', time.gmtime(int(my_slider.get())))

                # Output time to status bar
                status_bar.config(text=f"Time Elapsed: {converted_current_time}  of  {converted_song_length}  ")

                # Move this thing along by one second
                next_time = int(my_slider.get()) + 1
                my_slider.config(value=next_time)

            # # Output time to status bar
            # status_bar.config(text=f"Time Elapsed: {converted_current_time}  of  {converted_song_length}  ")
            # Update Slider Position Value to Current Song Position
            # my_slider.config(value=int(current_time))

            # update time
            status_bar.after(1000, play_time)

        # Add many songs
        def add_many_songs():
            songs = filedialog.askopenfilenames(initialdir='Music/', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))

            # Loop through song list and replace the directory info and .mp3 extension from song name
            for song in songs:
                song = song.replace("", "")
                song = song.replace(".mp3", "")
                # Insert into playlist
                song_box.insert(END, song)

        # Play selected song
        def play():
            # Set Stopped Variable to False so Song can Play
            global stopped
            stopped = False
            song = song_box.get(ACTIVE)
            song = f"{song}.mp3"

            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)

            # Call play_time function to get song length

            play_time()

            # # Update Slider to Position
            slider_position = int(song_length)
            my_slider.config(to=slider_position, value=0)

            # Get Current Volume
            # current_volume = pygame.mixer.music.get_volume()
            # slider_label.config(text=current_volume * 100)

        # Stop playing current song
        global stopped
        stopped = False

        def stop():
            # Reset Slider and Status Bar
            status_bar.config(text='')
            my_slider.config(value=0)
            # Stop Song from Playing
            pygame.mixer.music.stop()
            # unselects the current song from the listbox
            song_box.selection_clear(ACTIVE)

            # Clear The Status Bar
            status_bar.config(text='')

            # Set Stop Variable to True
            global stopped
            stopped = True

        # Play the next song in playlist
        def next_song():
            # Reset Slider and Status Bar
            status_bar.config(text='')
            my_slider.config(value=0)

            # Get the current song tuple number
            next_one = song_box.curselection()
            # Add one to the current song number
            next_one = next_one[0] + 1
            # Grab song title from playlist
            song = song_box.get(next_one)
            # Add directory structure and mp3 to song title
            song = f"{song}.mp3"

            # Load and play song
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)

            # Clear active bar in listbox
            song_box.selection_clear(0, END)

            # Activate new song bar
            song_box.activate(next_one)

            # Set Active bar to Next Song
            song_box.selection_set(next_one, last=None)

        # Play previous song in playlist
        def previous_song():
            # Reset Slider and Status Bar
            status_bar.config(text='')
            my_slider.config(value=0)

            # Get the current song tuple number
            next_one = song_box.curselection()
            # Add one to the current song number
            next_one = next_one[0] - 1
            # Grab song title from playlist
            song = song_box.get(next_one)
            # Add directory structure and mp3 to song title
            song = f"{song}.mp3"

            # Load and play song
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)

            # Clear active bar in listbox
            song_box.selection_clear(0, END)

            # Activate new song bar
            song_box.activate(next_one)

            # Set Active bar to Next Song
            song_box.selection_set(next_one, last=None)

        # Delete a Song
        def delete_song():
            stop()
            song_box.delete(ANCHOR)
            pygame.mixer.music.stop()

        # Delete All Songs from playlist
        def delete_all_songs():
            stop()
            # Delete All Songs
            song_box.delete(0, END)
            # Stop Music if it's playing
            pygame.mixer.music.stop()

        # Create Global Pause Variable
        global paused
        paused = False

        # Pause and Unpause the current song
        def pause(is_paused):
            global paused
            paused = is_paused

            if paused:
                # Unpause
                pygame.mixer.music.unpause()  # If paused we want to unpause
                paused = False
            else:
                # Pause
                pygame.mixer.music.pause()  # if unpaused we want to pause
                paused = True

        # Create Slider Function
        def slide(x):
            # slider_label.config(text=f"{int(my_slider.get())} of {int(song_length)}")
            song = song_box.get(ACTIVE)
            song = f"{song}.mp3"

            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

        options_frame = ttk.Frame(labelframe, style="Background.TFrame")
        options_frame.grid()

        # Create Volume Function
        def volume(x):
            pygame.mixer.music.set_volume(volume_slider.get())
            # Get Current Volume
            current_volume = pygame.mixer.music.get_volume()
            # slider_label.config(text=current_volume * 100)

            # Output time to status bar
            volume_status_bar.config(text=f"Volume: {int(current_volume * 100)}  ")

        # App MP3 Player Display
        app_description = ttk.Label(options_frame,
                                    text="MP3 Player",
                                    style="LightText.TLabel",
                                    font="Courier 34")

        app_description.grid(row=0, column=0, padx=(0, 60), pady=(20, 0))

        # Back Button
        back_button = ttk.Button(options_frame,
                                 text="<-",
                                 command=lambda: [show_welcome(), stop(), stop(), start_welcome_sound()],
                                 style="PomodoroButton.TButton",
                                 cursor="hand2")
        back_button.grid(row=0, column=1, padx=(0, 10), pady=(20, 0))

        # Add Songs Button
        add_song_button = ttk.Button(options_frame, text="Add Songs", style="PomodoroButton.TButton", command=add_many_songs)
        add_song_button.grid(row=0, column=2, padx=(10, 10), pady=(20, 0))

        # Delete Song Button
        delete_song_button = ttk.Button(options_frame, text="Delete Song", style="PomodoroButton.TButton", command=delete_song)
        delete_song_button.grid(row=0, column=3, padx=(10, 10), pady=(20, 0))

        # Delete Songs Button
        delete_all_songs_button = ttk.Button(options_frame, text="Delete All Songs", style="PomodoroButton.TButton", command=delete_all_songs)
        delete_all_songs_button.grid(row=0, column=4, padx=(10, 10), pady=(20, 0))

        # Create Master Frame
        master_frame = ttk.Frame(labelframe, style="Background.TFrame")
        master_frame.grid(pady=20)

        # Create Playlist Box
        song_box = Listbox(master_frame, bg="black", fg="green", width=80, height=20, selectbackground="white", selectforeground="black", selectborderwidth=1)    # bg = background color, fg = text color
        song_box.grid(row=0, column=0, padx=20)

        # Create Status Bar
        status_bar = Label(master_frame, text="", relief=GROOVE)
        status_bar.grid(row=1, column=0, ipady=1, pady=(30, 1), sticky="EW", columnspan=2)

        # Create Volume Status Bar
        volume_status_bar = Label(master_frame, text="Volume: 100 ", relief=GROOVE)
        volume_status_bar.grid(row=1, column=0, ipady=1, pady=(30, 1), sticky="E", columnspan=1)

        # Create Volume Label Frame
        volume_frame = ttk.LabelFrame(master_frame, text="Volume")
        volume_frame.grid(row=0, column=1, padx=(10, 10))

        # Create music position slider
        my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=968)
        my_slider.grid(row=2, column=0, pady=(0, 20), columnspan=2)

        # Create volume slider
        volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
        volume_slider.pack()

        # # Create Volume Value Label Frame
        # volume_value_frame = ttk.LabelFrame(master_frame)
        # volume_value_frame.grid(row=0, column=1, padx=(0, 60), pady=(220, 0))
        #
        # # Create Temporary Slider Label
        # slider_label = ttk.Label(volume_value_frame, text=f"volume: {0}", style="LightText.TLabel")
        # slider_label.pack()

        # Create Player Control Frame
        controls_frame = ttk.Frame(master_frame, style="Background.TFrame")
        controls_frame.grid(row=3, column=0, pady=20, columnspan=2)

        # Create Player Control Buttons
        back_button = ttk.Button(controls_frame, text="<<<", style="PomodoroButton.TButton", command=previous_song)
        forward_button = ttk.Button(controls_frame, text=">>>", style="PomodoroButton.TButton", command=next_song)
        play_button = ttk.Button(controls_frame, text="|>", style="PomodoroButton.TButton", command=play)
        pause_button = ttk.Button(controls_frame, text="||", style="PomodoroButton.TButton", command=lambda: pause(paused))
        stop_button = ttk.Button(controls_frame, text="|Stop|", style="PomodoroButton.TButton", command=stop)

        back_button.grid(row=0, column=0, padx=10)
        forward_button.grid(row=0, column=1, padx=10)
        play_button.grid(row=0, column=2, padx=10)
        pause_button.grid(row=0, column=3, padx=10)
        stop_button.grid(row=0, column=4, padx=10)
