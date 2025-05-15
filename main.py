from tkinter import *
from modules.GestureDrawing import GestureDrawing


if __name__ == '__main__':
    root = Tk()
    GestureDrawing(root).start()
    root.mainloop()
