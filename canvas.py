"""
name: canvas.py -- dollarstore-recognizer
description: Canvas tkinter definitions
authors: TJ Schultz, []
date: 1/14/22
"""

import tkinter as tk
import path as pth

## canvas class
class Canvas(tk.Frame):
    down = False
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

    def get_pointer_pos(self, event):
        print(event.x, event.y)
        return (event.x, event.y)

    ## toggle boolean state for recording pen values, controlled in main
    def toggle_down(self):
        self.down = not self.down

    ## pen method to draw path
    def pen(self, event):
        self.toggle_down()
        start_x = event.x
        start_y = event.y
        path = pth.Path(pth.Point(start_x, start_y))
        while (self.down):
            
            path.append(pth.Point())
            print(path)


