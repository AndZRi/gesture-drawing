from tkinter import *

from collections.abc import Callable

class TimeLabel(Label):
    def __init__(self, master):
        super().__init__(master)
        self.configure(font=('consolas', 20), highlightthickness=0)

        self.text = StringVar()
        self.time_left = 0
        self.paused = False
        self.time_expired_listeners: list[Callable] = []

        self.cur_after_id = None  # used for self.after_cancel()

        self.configure(textvariable=self.text)

    def set_timer(self, time: int):
        self.time_left = time
        if self.cur_after_id is not None:
            self.after_cancel(self.cur_after_id)
        self.cur_after_id = self.after(1000, self.timer_tick)
        self.update_text()

    def switch_timer(self, paused):
        self.paused = paused
        if not paused:
            self.set_timer(self.time_left)

    def timer_tick(self):
        if not self.paused:
            self.time_left -= 1
            self.cur_after_id = self.after(1000, self.timer_tick)

        self.update_text()

        if self.time_left == 0:
            self.on_time_expired()

    def update_text(self):
        mins = self.time_left // 60
        secs = self.time_left - mins * 60
        self.text.set(f"{mins:02d}:{secs:02d}")
        self.update()

    def on_time_expired(self):
        for i in self.time_expired_listeners:
            i()
