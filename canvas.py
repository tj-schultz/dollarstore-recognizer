"""
name: canvas.py -- dollarstore-recognizer
description: Canvas tkinter definitions
authors: TJ Schultz, []
date: 1/20/22
"""

import tkinter as tk
import path as pth
import time

## line attributes
line_pref = {
    "width": 5,
    "fill": "black",
    "ssteps": 5
}

## PathCanvas class
class PathCanvas():

    ## time constant to wait before parsing a new x, y value from mouse motion
    PATH_PARSE_CONST = 0.01

    ## class members
    down = False
    path = pth.Path()

    C_WIDTH = 0
    C_HEIGHT = 0

    def __init__(self, parent, incanvas, WIDTH, HEIGHT):

        self.parent = parent

        ## create native tkinter canvas object inside PathCanvas
        self.canvas = incanvas
        self.canvas.pack(side="top", fill="none", expand=False)

        self.C_WIDTH = WIDTH
        self.C_HEIGHT = HEIGHT

    ## returns pointer position
    def get_pointer_pos(self, event):
        print(event.x, event.y)
        return (event.x, event.y)

    ## toggle boolean state for recording pen values
    def toggle_down(self):
        self.down = not self.down

    ## pen tool method to draw path
    def pen(self, event):
        if not self.down:
            print("Pen")
            self.clear()
            self.toggle_down()
            start_x = event.x
            start_y = event.y
            self.path = pth.Path(pth.Point(start_x, start_y))
        else:
            self.toggle_down()

    ## log motion to the path structure using stitch
    def log_motion(self, x, y):
        time.sleep(self.PATH_PARSE_CONST)
        if self.down:
            self.path.stitch(pth.Point(x, y))
            print(str(self.path))

    ## draws polyline on canvas for last two points
    def draw_polyline(self, event):
        ## prevents drawing beyond border
        if event.x <= self.C_WIDTH and event.y <= self.C_HEIGHT:

            ## log motion
            self.log_motion(event.x, event.y)

            ## if 2 or more points in path, draw a line with the last two points
            if len(self.path) > 1 and self.down:
                self.canvas.create_line(self.path.parsed_path[-2].x, self.path.parsed_path[-2].y, \
                                        self.path.parsed_path[-1].x, self.path.parsed_path[-1].y,\
                                        width=line_pref["width"], fill=line_pref["fill"],\
                                        splinesteps=line_pref["ssteps"], capstyle="round")
            ## update the Canvas object
            self.canvas.update()

    ## clears the canvas
    def clear(self):
        del self.path.parsed_path
        self.path = pth.Path()
        self.canvas.delete("all")