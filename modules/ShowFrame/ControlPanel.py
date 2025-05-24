from tkinter import ttk
from tkinter import *
from collections.abc import Callable

from PIL import ImageTk
from Resources import Processed

class ControlPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.paused = False
        self.previous_button_listeners: list[Callable] = []
        self.play_button_listeners: list[Callable] = [self.switch_pause]
        self.next_button_listeners: list[Callable] = []

        self.init_widgets()

    def init_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_propagate(True)

        play_img = ImageTk.PhotoImage(Processed.PlayIcon)
        play_button = ttk.Button(self, image=play_img, command=self.on_play_button_clicked)
        play_button.image = play_img

        prev_img = ImageTk.PhotoImage(Processed.PreviousIcon)
        previous_button = ttk.Button(self, image=prev_img, command=self.on_previous_button_clicked)
        previous_button.image = prev_img

        next_img = ImageTk.PhotoImage(Processed.NextIcon)
        next_button = ttk.Button(self, image=next_img, command=self.on_next_button_clicked)
        next_button.image = next_img

        previous_button.grid(column=0, row=0, sticky=E)
        play_button.grid(column=1, row=0)
        next_button.grid(column=2, row=0, sticky=W)

    def switch_pause(self):
        self.paused = not self.paused

    def on_play_button_clicked(self):
        for i in self.play_button_listeners:
            i()

    def on_previous_button_clicked(self):
        for i in self.previous_button_listeners:
            i()

    def on_next_button_clicked(self):
        for i in self.next_button_listeners:
            i()
