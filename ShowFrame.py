from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, UnidentifiedImageError


class ShowFrame(ttk.Frame):
    def __init__(self, gd, padding='12 12 12 12'):
        super().__init__(gd.root, padding=padding)

        self.init_widgets()

    def init_widgets(self):
        img_label = ttk.Label(self)
