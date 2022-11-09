import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import pygame
import tkintermapview


def start_welcome_sound():
    pygame.mixer.music.load("./frames/PS5 Intro Theme 2.mp3")
    pygame.mixer.music.play()


class Maps(ttk.Frame):  # we are calling super class to make self into the frame
    def __init__(self, parent, controller, show_welcome):
        super().__init__(parent)

        self["style"] = "Background.TFrame"  # assigning Background style

        COLOR_PRIMARY = "#2e3f4f"
        COLOR_LIGHT_BACKGROUND = "#fff"
        COLOR_DARK_TEXT = "#8095a8"
        COLOR_LIGHT_TEXT = "#eee"
        labelframe = LabelFrame(self, background=COLOR_PRIMARY, borderwidth=10)
        labelframe.pack(fill="both", expand=True, pady=(20, 0), padx=5)

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TimerText.TLabel",
                        background=COLOR_LIGHT_BACKGROUND,
                        foreground=COLOR_DARK_TEXT,
                        font="Courier 30")

        # welcome label
        welcome_description = ttk.Label(labelframe,
                                        text="   Welcome to Navigator - The Map App",
                                        style="TimerText.TLabel")
        welcome_description.pack(pady=(2, 20), expand=False, fill="both")

        self.markers_list = []

        # To search specific location
        def locate():
            global marker
            marker = map_widget.set_address(search_box.get(), marker=True)
            self.markers_list.append(marker)
            locations.config(text=f"Location: {search_box.get().upper()}", foreground="white")

        # To delete a marker
        def delete_locate_marker():
            map_widget.delete(marker)
            locations.config(text="Location Details", foreground="white")

        # To delete All markers
        def delete_all_located_markers():
            for markers in self.markers_list:
                map_widget.delete(markers)
            locations.config(text="Location Details", foreground="white")
            clear_marker_list()

        # To get address via coordinates
        def address():
            coord = map_widget.get_position()
            adr = tkintermapview.convert_coordinates_to_address(coord[0], coord[1])
            print(adr.city, adr.state, adr.country, adr.latlng)
            locations.config(text=f"City: {adr.city}   State: {adr.state}   Country: {adr.country}   Coordinates: {adr.latlng}", foreground="white")

        self.marker_list = []

        # To Add Markers
        def add_marker_event(coords):
            print("Add marker:", coords)
            new_marker = map_widget.set_marker(coords[0], coords[1], address())
            self.marker_list.append(new_marker)

        # To Delete Markers
        def clear_marker_list():
            for markers in self.marker_list:
                map_widget.delete(markers)
                locations.config(text="Location Details", foreground="white")

        # Map Label Frame
        map_label = LabelFrame(labelframe)
        map_label.pack(expand=True, pady=20)

        # Map widget
        map_widget = tkintermapview.TkinterMapView(map_label, width=800, height=600, corner_radius=0)

        # Map Server (Google)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Satellite Mode Function
        def normal_mode():
            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Satellite Mode Function
        def satellite_mode():
            map_widget.set_tile_server("https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", max_zoom=22)

        # Set Coordinates
        map_widget.set_position(23.2599, 77.4126)

        # Set A Zoom Level
        map_widget.set_zoom(10)  # The higher the value, more the zoom

        # Set Address
        map_widget.set_address("", marker=True)

        # To add markers at the current location
        map_widget.add_right_click_menu_command(label="Add Marker",
                                                command=add_marker_event,
                                                pass_coords=True)

        # To delete markers at the current location
        map_widget.add_right_click_menu_command(label="delete Marker",
                                                command=clear_marker_list,
                                                pass_coords=False)

        # set a position marker
        # marker_2 = map_widget.set_marker(52.516268, 13.377695, text="Brandenburger Tor")
        # marker_3 = map_widget.set_marker(52.55, 13.4, text="52.55, 13.4")
        # # marker_3.set_position(...)
        # # marker_3.set_text(...)
        # # marker_3.delete()
        #
        # # set a path
        # path_1 = map_widget.set_path([marker_2.position, marker_3.position, (52.57, 13.4), (52.55, 13.35)])
        # # path_1.add_position(...)
        # # path_1.remove_position(...)
        # # path_1.delete()

        map_widget.pack()

        # Control_1 Frame
        control_frame_1 = LabelFrame(labelframe, background=COLOR_PRIMARY, border=False)
        control_frame_1.pack()

        # Locations Detail Label
        locations = Label(control_frame_1, background=COLOR_PRIMARY, text="Location Details", foreground="white")
        locations.grid(row=0, column=0, padx=(60, 540))

        # back button
        back_button = ttk.Button(control_frame_1,
                                 text="Back",
                                 command=lambda: [show_welcome(), start_welcome_sound()],
                                 style="PomodoroButton.TButton",
                                 cursor="hand2")
        back_button.grid(row=0, column=1, padx=(0, 60))

        # Control Frame
        control_frame = LabelFrame(labelframe, background=COLOR_PRIMARY)
        control_frame.pack(pady=20)

        # Search Box
        search_box = Entry(control_frame, font=28)
        search_box.grid(row=0, column=0, pady=20, padx=10)

        # Search Button
        search_button = ttk.Button(control_frame, text="Locate", style="PomodoroButton.TButton", command=locate)
        search_button.grid(row=0, column=1, padx=10)

        # Remove Marker Button
        remove_marker_button = ttk.Button(control_frame, text="Clear Marker", style="PomodoroButton.TButton", command=delete_locate_marker)
        remove_marker_button.grid(row=0, column=2, padx=10)

        # Remove All Markers Button
        remove_all_markers_button = ttk.Button(control_frame, text="Clear All", style="PomodoroButton.TButton", command=delete_all_located_markers)
        remove_all_markers_button.grid(row=0, column=3, padx=10)

        # normal mode button
        normal_mode_button = ttk.Button(control_frame,
                                        text="Normal",
                                        command=normal_mode,
                                        style="PomodoroButton.TButton",
                                        cursor="hand2")
        normal_mode_button.grid(row=0, column=4, padx=10)

        # satellite mode button
        satellite_mode_button = ttk.Button(control_frame,
                                           text="Satellite",
                                           command=satellite_mode,
                                           style="PomodoroButton.TButton",
                                           cursor="hand2")
        satellite_mode_button.grid(row=0, column=5, padx=10)

