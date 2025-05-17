import tkinter
from tkinter import *
from tkinter import ttk

from PIL import ImageTk

from modules.ImageExtensions import OptimizedImage
from modules.MenuFrame import SessionData
from Resources import Processed

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import GestureDrawing


class ShowFrame(ttk.Frame):
    def __init__(self, gd: 'GestureDrawing'):
        super().__init__(gd.root)

        self.gd = gd
        self.cur_image_i = 0
        self.data = SessionData(Processed.TestImages, 0)
        self.cur_optimized_image = OptimizedImage(self.data.images[0])
        self.cur_image_size = (0, 0)

        self.time_left = 0
        self.time_label_text = StringVar()

        self.init_widgets()
        self.bind("<Configure>", self.on_configured)

    def init_widgets(self):
        self.configure(borderwidth=0)

        # initializing using Label instead of ttk.Label because it has highlight thickness setting, so we can remove
        # this pissing of invisible border on bottom and left
        img_label = Label(self, text='Loading image...', compound='none',
                          highlightthickness=0, borderwidth=0, relief=FLAT, padx=0, pady=0)
        time_label = Label(self, textvariable=self.time_label_text, font=('consolas', 20), highlightthickness=0)

        # packing in the window (frame)
        time_label.pack(expand=False, fill=X, side=TOP)
        img_label.pack(expand=True, fill=BOTH, anchor=CENTER)

        # assigning as attributes
        self.img_label = img_label
        self.time_label = time_label

    def start(self, data: SessionData):
        self.grid(row=0, column=0, sticky=NSEW)

        # setting the data
        self.data = data
        self.cur_optimized_image = OptimizedImage(self.data.images[self.cur_image_i])
        self.img_label.update()
        self.change_image()

        # starting the timer
        self.time_left = data.interval
        self.update_time_label()
        self.time_label.after(1000, self.timer_tick)

    def change_image(self):
        # the label actually shrinks to "Loading image..." size when updated, so we have to
        width, height = self.img_label.winfo_width(), self.img_label.winfo_height()

        # showing the "Loading image..." thing
        self.img_label.configure(image='')
        self.img_label.image = None
        self.img_label.update()

        self.cur_optimized_image = OptimizedImage(self.data.images[self.cur_image_i])
        self.resize_current_image(width, height)
        # self.resize_current_image(self.winfo_width(), self.winfo_height() - self.time_label.winfo_height())

    def on_configured(self, event: tkinter.Event):
        if event.width != self.cur_image_size[0] or event.height != self.cur_image_size[1]:
            # self.resize_current_image(event.width, event.height - self.time_label.winfo_height())
            self.img_label.update_idletasks()
            self.resize_current_image(self.img_label.winfo_width(), self.img_label.winfo_height())

    def resize_current_image(self, width, height):
        # +3 +3 to remove the space on sides and bottom (idk where that comes from)
        width += 3
        height += 3
        new_image = self.cur_optimized_image.resized((width, height))

        new_image_tk = ImageTk.PhotoImage(new_image)
        self.img_label.configure(image=new_image_tk)
        self.img_label.image = new_image_tk
        self.cur_image_size = new_image_tk.width(), new_image_tk.height()

    def timer_tick(self):
        self.time_left -= 1
        self.update_time_label()

        if self.time_left == 0:
            self.on_time_expired()
            self.time_left = self.data.interval
            self.update_time_label()

        # so it recursively does the counting
        self.time_label.after(1000, self.timer_tick)

    def on_time_expired(self):
        self.cur_image_i += 1
        if self.cur_image_i >= len(self.data.images):
            self.cur_image_i = 0

        self.change_image()

    def update_time_label(self):
        mins = self.time_left // 60
        secs = self.time_left - mins * 60
        self.time_label_text.set(f"{mins:02d}:{secs:02d}")
        self.time_label.update()


if __name__ == '__main__':
    from modules.GestureDrawing import GestureDrawing
    from modules.GlobalConstants import *


    root = Tk()
    gd = GestureDrawing(root)

    gd.on_data_received(SessionData(images=Processed.TestImages, interval=TEST_INTERVAL))
    root.mainloop()
