from tkinter import *
from utils.Event import Event as uEvent

class TimeLabel(Label):
    def __init__(self, master):
        super().__init__(master)
        self.configure(font=('consolas', 20), highlightthickness=0)

        self.text = StringVar()
        self.time_left = 0
        self.paused = False

        self.__cur_after_id = None  # used for self.after_cancel()
        self.on_time_expired = uEvent()

        self.configure(textvariable=self.text)

    def set_timer(self, time: int):
        self.time_left = time
        self.after(1000, self.timer_tick)
        self.update_text()

    def switch_timer(self):
        self.paused = not self.paused
        if not self.paused:
            self.set_timer(self.time_left)

    def timer_tick(self):
        if not self.paused:
            self.time_left -= 1
            self.after(1000, self.timer_tick)

        self.update_text()

        if self.time_left == 0:
            self.on_time_expired()

    def update_text(self):
        mins = self.time_left // 60
        secs = self.time_left - mins * 60
        self.text.set(f"{mins:02d}:{secs:02d}")
        self.update()

    def after(self, ms, func=...):
        if self.__cur_after_id is not None:
            self.after_cancel(self.__cur_after_id)
        self.__cur_after_id = super().after(ms, func)
