import random
from tkinter import *
from tkinter import ttk, filedialog, messagebox

from PIL import Image, UnidentifiedImageError

import os
from os import listdir
from dataclasses import dataclass

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import GestureDrawing


@dataclass
class SessionData:
    images: list[Image.Image]
    interval: int = 0


def get_images_from_dir(src_dir: str) -> list[Image.Image]:
    images = []
    success, failure = 0, 0

    if not os.path.isdir(src_dir):
        return []
    for filename in listdir(src_dir):
        try:
            images.append(Image.open(src_dir + '/' + filename))
            success += 1

        except UnidentifiedImageError as ex:
            print(ex)
            failure += 1

    print(f"loaded {success}/{failure + success} files")

    return images


class MenuFrame(ttk.Frame):
    def __init__(self, gd: 'GestureDrawing', padding='12 12 12 12'):
        super().__init__(gd.root, padding=padding)

        self.gd = gd
        self.source_dir = StringVar()
        self.mins = IntVar()
        self.secs = IntVar()

        self.do_shuffle = True  # remember to make a checkbox for this

        self.init_widgets()

    def init_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid(column=0, row=0, sticky=NSEW)

        # folder frame
        folder_frame = ttk.Frame(self, padding='12 12 12 12')
        folder_frame.grid(column=1, row=1, sticky=NSEW)
        folder_frame.grid_columnconfigure(2, weight=1)

        folder_button   = ttk.Button(folder_frame, text="Pick folder", command=self.pick_folder)
        folder_entry    = ttk.Entry(folder_frame, textvariable=self.source_dir)

        folder_button.  grid(column=1, row=1, sticky=EW)
        folder_entry.   grid(column=2, row=1, sticky=EW)

        # time picking frame
        time_frame = ttk.Frame(self, padding='12 12 12 12')
        time_frame.grid(column=1, row=2, sticky=NSEW)
        time_frame.grid_columnconfigure(1, weight=1)
        time_frame.grid_rowconfigure(1, weight=1)

        time_label      = ttk.Label(time_frame, text="Time:", font=('Consolas', 18))
        minutes_entry   = ttk.Entry(time_frame, textvariable=self.mins, width=5, font=('Arial', 15))
        secs_entry      = ttk.Entry(time_frame, textvariable=self.secs, width=5, font=('Arial', 15))
        ttk.Label(time_frame, text='m  ', font=('Consolas', 18), padding='4 4 4 4').grid(column=3, row=1, sticky=W)
        ttk.Label(time_frame, text='s', font=('Consolas', 18), padding='4 4 4 4').grid(column=5, row=1, sticky=W)

        time_label.     grid(column=1, row=1, sticky=NSEW)
        minutes_entry.  grid(column=2, row=1)
        secs_entry.     grid(column=4, row=1)

        # start button
        start_button = ttk.Button(self, text="Start", command=self.finish)
        start_button.grid(column=1, row=3, sticky=NSEW)


        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def pick_folder(self):
        self.source_dir.set(filedialog.askdirectory())

    def start(self):
        self.grid(row=0, column=0, sticky=NSEW)

    def finish(self):
        src_dir = self.source_dir.get()
        interval = self.mins.get() * 60 + self.secs.get()

        if src_dir == 'PASHALKO':
            from Resources import Processed
            images = Processed.TestImages
        else:
            images = get_images_from_dir(src_dir)

        if not images:
            messagebox.showwarning("Error", "Please, select an existing and not empty directory.")
            return

        if self.do_shuffle:
            random.shuffle(images)

        self.grid_forget()

        self.gd.on_data_received(SessionData(images=images, interval=interval))
