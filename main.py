from tkinter import *

from MenuFrame import MenuFrame
from ShowFrame import ShowFrame


class GestureDrawing:
    def __init__(self, root: Tk):
        self.root = root
        root.title("Gesture Drawing!")
        self.menuframe = MenuFrame(self)
        self.showframe = ShowFrame(self)

    def recieve_data(self, data):
        self.showframe.start(data)

    def start(self):
        self.menuframe.start()


if __name__ == '__main__':
    root = Tk()
    GestureDrawing(root).start()
    root.mainloop()
