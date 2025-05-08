from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
from os import listdir
from dataclasses import dataclass
# from collections import namedtuple

# from main import GestureDrawing


# SessionData = namedtuple("SessionData", ['images', 'interval'])
@dataclass
class SessionData:
    images: list[Image.Image]
    interval: int = 0


class MenuFrame(ttk.Frame):
    def __init__(self, gd, padding='12 12 12 12'):
        super().__init__(gd.root, padding=padding)

        self.gd = gd
        self.source_dir = StringVar()
        self.mins = IntVar()
        self.secs = IntVar()

        self.init_widgets()

    def init_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid(column=0, row=0, sticky=NSEW)

        folder_frame = ttk.Frame(self, padding='12 12 12 12')
        folder_frame.grid(column=1, row=1, sticky=NSEW)
        folder_button = ttk.Button(folder_frame, text="Pick folder", command=self.pick_folder)
        folder_button.grid(column=1, row=1, sticky=EW)
        folder_frame.grid_columnconfigure(2, weight=1)
        folder_entry = ttk.Entry(folder_frame, textvariable=self.source_dir)
        folder_entry.grid(column=2, row=1, sticky=EW)

        time_frame = ttk.Frame(self, padding='12 12 12 12')
        time_frame.grid(column=1, row=2, sticky=NSEW)

        time_label = ttk.Label(time_frame, text="Time: ", font=20)
        time_label.grid(column=1, row=1, sticky=NSEW)
        time_frame.grid_columnconfigure(1, weight=1)
        time_frame.grid_rowconfigure(1, weight=1)

        minutes_entry = ttk.Entry(time_frame, textvariable=self.mins, width=10)
        minutes_entry.grid(column=2, row=1)
        ttk.Label(time_frame, text='m   ', font=20).grid(column=3, row=1, sticky=W)

        secs_entry = ttk.Entry(time_frame, textvariable=self.secs, width=10)
        secs_entry.grid(column=4, row=1)
        ttk.Label(time_frame, text='s', font=20).grid(column=5, row=1, sticky=W)

        start_button = ttk.Button(self, text="Start", command=self.finish)
        start_button.grid(column=1, row=3, sticky=NSEW)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def pick_folder(self):
        self.source_dir.set(filedialog.askdirectory())

    def start(self):
        # self.pack(expand=True, fill=BOTH)
        self.grid(row=0, column=0, sticky=NSEW)

    def finish(self):
        src_dir = self.source_dir.get()
        interval = self.mins.get() * 60 + self.secs.get()

        # get images from the directory to a list
        images = []
        success, failure = 0, 0
        for filename in listdir(src_dir):
            try:
                images.append(Image.open(src_dir + '/' + filename))
                success += 1

            except UnidentifiedImageError as ex:
                print(ex)
                failure += 1

            except NotADirectoryError as ex:
                print(ex)
                return
        print(f"loaded {success}/{failure + success} images")


        self.grid_forget()

        self.gd.receive_data(SessionData(images=images, interval=interval))
