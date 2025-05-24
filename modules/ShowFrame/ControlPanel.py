from tkinter import ttk
from tkinter import *
from collections.abc import Callable

from Resources import Processed

class ControlPanel(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.paused = False
        self.configure(background='black', height=50)
        self.previous_button_listeners: list[Callable] = []
        self.play_button_listeners: list[Callable] = [self.switch_pause]
        self.next_button_listeners: list[Callable] = []

    def init_widgets(self):
        play_button = Button(self, image=Processed.PlayIcon, command=self.on_play_button_clicked)
        previous_button = Button(self, image=Processed.PreviousIcon, command=self.on_previous_button_clicked)
        next_button = Button(self, image=Processed.NextIcon, command=self.on_next_button_clicked)

        # previous_button.grid(column=0, row=0)
        # play_button.grid(column=1, row=0)
        # next_button.grid(column=2, row=0)

        previous_button.pack(side=LEFT)
        play_button.pack(side=BOTTOM)
        next_button.pack(side=RIGHT)


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
