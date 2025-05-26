from tkinter import *
from tkinter import ttk

from PIL import ImageTk

from modules.ImageExtensions import OptimizedImage
from modules.MenuFrame import SessionData
from modules.ShowFrame.ControlPanel import ControlPanel
from modules.ShowFrame.TimeLabel import TimeLabel
from Resources import Processed

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import GestureDrawing


class ShowFrame(ttk.Frame):
    def __init__(self, gd: 'GestureDrawing'):
        super().__init__(gd.root)

        self.gd = gd
        self._cur_image_i = 0  # you should not use this
        self.data = SessionData(Processed.TestImages, 0)
        self.cur_optimized_image = OptimizedImage(self.data.images[0])
        self.cur_image_size = (0, 0)

        self.init_widgets()
        self.img_label.bind("<Configure>", self.on_img_label_configured)

    @property
    def cur_image_i(self):
        return self._cur_image_i

    def init_widgets(self):
        self.configure(borderwidth=0)

        # initializing using Label instead of ttk.Label because it has highlight thickness setting, so we can remove
        # this pissing off invisible border on bottom and left
        img_label = Label(self, text='Loading image...', compound='none',
                          highlightthickness=0, borderwidth=0, relief=FLAT, padx=0, pady=0)
        time_label = TimeLabel(self)
        control_panel = ControlPanel(self)

        # packing in the window (frame)
        time_label.pack(expand=False, fill=X, side=TOP)
        control_panel.pack(expand=False, fill=X, side=BOTTOM)
        img_label.pack(expand=True, fill=BOTH, anchor=CENTER)

        # adding listeners
        time_label.on_time_expired.add_listener(self.next_image)
        control_panel.on_play_button_clicked.add_listener(time_label.switch_timer)
        control_panel.on_next_button_clicked.add_listener(self.next_image)
        control_panel.on_previous_button_clicked.add_listener(self.prev_image)

        # assigning as attributes
        self.img_label = img_label
        self.time_label = time_label
        self.control_panel = control_panel

    def start(self, data: SessionData):
        self.grid(row=0, column=0, sticky=NSEW)

        # setting the data
        self.data = data
        self.cur_optimized_image = OptimizedImage(self.data.images[self.cur_image_i])
        self.img_label.update()
        self.update_image()

        # starting the timer
        self.time_label.set_timer(self.data.interval)

    def update_image(self):
        # the label actually shrinks to "Loading image..." size when updated, so we have to
        width, height = self.img_label.winfo_width(), self.img_label.winfo_height()

        # showing the "Loading image..." thing
        self.img_label.configure(image='')
        self.img_label.image = None
        self.img_label.update()

        self.cur_optimized_image = OptimizedImage(self.data.images[self.cur_image_i])
        self.resize_current_image(width, height)

    def on_img_label_configured(self, event: Event):
        if event.width != self.cur_image_size[0] or event.height != self.cur_image_size[1]:
            self.resize_current_image(event.width, event.height)

    def resize_current_image(self, width, height):
        # +3 +3 to remove the space on sides and bottom (idk where that comes from)
        width += 3
        height += 3
        new_image = self.cur_optimized_image.resized((width, height))

        new_image_tk = ImageTk.PhotoImage(new_image)
        self.img_label.configure(image=new_image_tk)
        self.img_label.image = new_image_tk
        self.cur_image_size = new_image_tk.width(), new_image_tk.height()

    def set_image_i(self, i: int):
        self._cur_image_i = i % len(self.data.images)
        self.update_image()
        self.time_label.set_timer(self.data.interval)

    def next_image(self):
        self.set_image_i(self.cur_image_i + 1)

    def prev_image(self):
        self.set_image_i(self.cur_image_i - 1)


if __name__ == '__main__':
    from modules.GestureDrawing import GestureDrawing
    from modules.Constants import *

    root = Tk()
    gd = GestureDrawing(root)

    gd.on_data_received(SessionData(images=Processed.TestImages, interval=TEST_INTERVAL))
    root.mainloop()
