from tkinter import *

from MenuFrame import MenuFrame
from ShowFrame import ShowFrame


class GestureDrawing:
    def __init__(self, root: Tk):
        self.root = root
        root.title("Gesture Drawing!")
        root.rowconfigure(index=0, weight=1)
        root.columnconfigure(index=0, weight=1)
        root.geometry("300x200")
        root.minsize(50, 50)
        root.grid_propagate(False)

        self.menuframe = MenuFrame(self)
        self.showframe = ShowFrame(self)

        self.always_on_top = True

    def on_data_received(self, data):
        self.showframe.start(data)

    def start(self):
        self.menuframe.start()

    @property
    def always_on_top(self) -> bool:
        return self._always_on_top

    @always_on_top.setter
    def always_on_top(self, value: bool):
        self._always_on_top = value
        self.root.wm_attributes("-topmost", self._always_on_top)


if __name__ == '__main__':
    root = Tk()
    GestureDrawing(root).start()
    root.mainloop()
