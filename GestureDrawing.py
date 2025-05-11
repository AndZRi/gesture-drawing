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
        self.menuframe = MenuFrame(self)
        self.showframe = ShowFrame(self)
        root.grid_propagate(False)

    def on_data_received(self, data):
        self.showframe.start(data)

    def start(self):
        self.menuframe.start()


if __name__ == '__main__':
    root = Tk()
    GestureDrawing(root).start()
    root.mainloop()
