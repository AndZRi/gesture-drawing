import tkinter
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

from ImageExtensions import OptimizedImage
from MenuFrame import SessionData


class ShowFrame(ttk.Frame):
    def __init__(self, gd):
        super().__init__(gd.root)

        self.gd = gd
        self.cur_image_i = 0
        self.cur_optimized_image = OptimizedImage(Image.open("../test_images/test_image.jpg"))
        self.cur_image_size = (0, 0)
        self.data = SessionData([Image.open("../test_images/test_image.jpg")], 0)

        self.time_left = 0
        self.time_label_text = StringVar()

        self.init_widgets()
        self.bind("<Configure>", self.on_configured)

    def init_widgets(self):
        img_label = ttk.Label(self, text='Loading image...')
        time_label = ttk.Label(self, textvariable=self.time_label_text, font=('consolas', 20))

        time_label.pack(expand=False, side=TOP)
        img_label.pack(expand=True, anchor=CENTER)

        self.img_label = img_label
        self.time_label = time_label

    def start(self, data: SessionData):
        self.grid(row=0, column=0, sticky=NSEW)

        self.data = data
        self.cur_optimized_image = OptimizedImage(self.data.images[self.cur_image_i])
        self.after(50, self.change_image)

        self.time_left = data.interval
        self.refresh_time_label()
        self.time_label.after(1000, self.on_timer_tick)

    def change_image(self):
        self.img_label.configure(image=None)
        self.img_label.image = None
        self.img_label.update()
        self.cur_optimized_image = OptimizedImage(self.data.images[self.cur_image_i])
        self.resize_current_image(self.winfo_width(), self.winfo_height() - self.time_label.winfo_height())

    def on_configured(self, event: tkinter.Event):
        if event.width != self.cur_image_size[0] or event.height != self.cur_image_size[1]:
            self.resize_current_image(event.width, event.height - self.time_label.winfo_height())

    def resize_current_image(self, width, height):
        new_image = self.cur_optimized_image.resized((width, height))

        new_image_tk = ImageTk.PhotoImage(new_image)
        self.img_label.configure(image=new_image_tk)
        self.img_label.image = new_image_tk
        self.cur_image_size = new_image_tk.width(), new_image_tk.height()

    def on_timer_tick(self):
        self.time_left -= 1

        if self.time_left == 0:
            self.on_time_expired()

        self.refresh_time_label()
        self.time_label.after(1000, self.on_timer_tick)

    def on_time_expired(self):
        self.cur_image_i += 1
        if self.cur_image_i >= len(self.data.images):
            self.cur_image_i = 0

        self.change_image()
        self.time_left = self.data.interval

    def refresh_time_label(self):
        mins = self.time_left // 60
        secs = self.time_left - mins * 60
        self.time_label_text.set(f"{mins:02d}:{secs:02d}")


if __name__ == '__main__':
    from GestureDrawing import GestureDrawing
    from MenuFrame import get_images_from_dir
    from GlobalConstants import *


    root = Tk()
    gd = GestureDrawing(root)

    gd.on_data_received(SessionData(images=get_images_from_dir(TEST_IMAGES_DIR), interval=TEST_INTERVAL))
    root.mainloop()
