import tkinter
from tkinter import *
from tkinter import ttk

from MenuFrame import MenuFrame


class GestureDrawing:
    def __init__(self, root: Tk):
        self.root = root
        root.title = "Gesture Drawing!"
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self.menuframe = MenuFrame(self)
        self.menuframe.start()

    def recieve_data(self, data):
        print(data)

    def slideshow_init(self):
        slideframe = ttk.Frame(root, padding='12 12 12 12')
        self.slideframe = slideframe
        slideframe.pack(expand=True, fill=tkinter.BOTH)
        slideframe.grid_columnconfigure(1, weight=1)
        slideframe.grid_rowconfigure(1, weight=0)
        slideframe.grid_rowconfigure(2, weight=0)
        slideframe.grid_rowconfigure(3, weight=1)
        slideframe.grid(column=0, row=0, sticky=NSEW)

        ####


root = Tk()
GestureDrawing(root)
root.mainloop()
