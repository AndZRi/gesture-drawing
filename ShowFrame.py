import tkinter
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image
from math import floor

from MenuFrame import SessionData


def resize_rationed(image: Image.Image, width, height):
    ratio = image.width / image.height
    nw1 = floor(height * ratio)
    nh1 = floor(nw1 / ratio)

    nh2 = floor(width / ratio)
    nw2 = floor(nh2 * ratio)

    if nw1 <= nw2:
        return image.resize((nw1, nh1), resample=Image.Resampling.BOX)
    return image.resize((nw2, nh2), resample=Image.Resampling.BOX)


class ShowFrame(ttk.Frame):
    def __init__(self, gd):
        super().__init__(gd.root)

        self.gd = gd
        self.cur_image_i = 0
        self.cur_image_size = (0, 0)
        # self.widgetName = ""

        self.init_widgets()

        self.bind("<Configure>", self.on_configured)

    def init_widgets(self):
        img_label = ttk.Label(self)
        time_label = ttk.Label(self)

        time_label.pack(expand=False, side=TOP)
        img_label.pack(expand=True, anchor=CENTER)

        self.img_label = img_label
        self.time_label = time_label

    def start(self, data: SessionData):
        self.grid(row=0, column=0, sticky=NSEW)

        self.data = data
        self.img_label.configure(image=ImageTk.PhotoImage(data.images[0]), text='gde image muzhiki')
        self.img_label.image = ImageTk.PhotoImage(data.images[0])

        self.resize_current_image(200, 200)

    def on_configured(self, event: tkinter.Event):
        if event.width != self.cur_image_size[0] or event.height != self.cur_image_size[1]:
            self.resize_current_image(event.width, event.height - self.time_label.winfo_height())

    def resize_current_image(self, width, height):
        new_image = resize_rationed(self.data.images[self.cur_image_i], width, height)
        new_image_tk = ImageTk.PhotoImage(new_image)
        self.img_label.configure(image=new_image_tk)
        self.img_label.image = new_image_tk
        self.cur_image_size = new_image_tk.width(), new_image_tk.height()


if __name__ == '__main__':
    from main import GestureDrawing

    root = Tk()
    gd = GestureDrawing(root)

    test_images = [Image.open("test_image.jpg")]
    gd.receive_data(SessionData(images=test_images, interval=-1))
    root.mainloop()
