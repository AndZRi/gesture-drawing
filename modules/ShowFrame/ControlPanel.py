from tkinter import ttk
from tkinter import *

from PIL import ImageTk
from Resources import Processed
from utils.Event import Event as uEvent

class ControlPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.paused = False

        self.on_previous_button_clicked = uEvent()
        self.on_play_button_clicked = uEvent()
        self.on_next_button_clicked = uEvent()

        self.on_play_button_clicked.add_listener(self.switch_pause)

        self.init_widgets()

    def init_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_propagate(True)

        # adjust the size of buttons with the icons size (i was lazy)
        pause_img = ImageTk.PhotoImage(Processed.PauseIcon)
        play_button = ttk.Button(self, image=pause_img, command=self.on_play_button_clicked)
        play_button.image = pause_img

        prev_img = ImageTk.PhotoImage(Processed.PreviousIcon)
        previous_button = ttk.Button(self, image=prev_img, command=self.on_previous_button_clicked)
        previous_button.image = prev_img

        next_img = ImageTk.PhotoImage(Processed.NextIcon)
        next_button = ttk.Button(self, image=next_img, command=self.on_next_button_clicked)
        next_button.image = next_img

        previous_button.grid(column=0, row=0, sticky=E)
        play_button.grid(column=1, row=0)
        next_button.grid(column=2, row=0, sticky=W)

        self.play_button = play_button

    def switch_pause(self):
        self.paused = not self.paused

        if self.paused:
            play_img = ImageTk.PhotoImage(Processed.PlayIcon)
            self.play_button.configure(image=play_img)
            self.play_button.image = play_img
        else:
            pause_img = ImageTk.PhotoImage(Processed.PauseIcon)
            self.play_button.configure(image=pause_img)
            self.play_button.image = pause_img
