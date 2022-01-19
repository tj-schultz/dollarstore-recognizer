"""
name: canvas.py -- dollarstore-recognizer
description: Canvas tkinter definitions
authors: TJ Schultz, []
date: 1/14/22
"""

import tkinter as tk
import path as pth
import time

## canvas class
class Canvas(tk.Frame):
    down = True
    path = pth.Path(pth.Point(0, 0))
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

    ## returns pointer position
    def get_pointer_pos(self, event):
        print(event.x, event.y)
        return (event.x, event.y)

    ## toggle boolean state for recording pen values, controlled in main
    def toggle_down(self):
        self.down = not self.down

    ## pen tool method to draw path
    def pen(self, event):
        self.toggle_down()
        start_x = event.x
        start_y = event.y
        self.path = pth.Path(pth.Point(start_x, start_y))

    ## log motion using stitch
    def log_motion(self, x, y):
        time.sleep(0.1)
        if self.down:
            self.path.stitch(pth.Point(x, y))

    def draw_polyline(self, event):
        canvas.log_motion(event.x, event.y)
        if len(canvas.path.parsed_path > 2):
            canvas.create_line(canvas.path.parsed_path[-2].x, canvas.path.parsed_path[-2].y, \
                               canvas.path.parsed_path[-1].x, canvas.path.parsed_path[-1].y)