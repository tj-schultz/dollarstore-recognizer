"""
name: main.py -- dollarstore-recognizer
description: An implementation of the $-recognizer in python with a Canvas input
authors: TJ Schultz, []
date: 1/20/22
"""

import tkinter as tk
import canvas as cvs
import path as pth

VERSION = "0.1"

## main application class defined for tkinter
class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        ## GUI -- Canvas

        ## define Canvas properties
        C_WIDTH = 300
        C_HEIGHT = 300

        self.canvas = tk.Canvas(root, width=C_WIDTH, height=C_HEIGHT, bg="lightgrey", \
                                         highlightthickness=5, highlightbackground="medium sea green")

        ## create PathCanvas container object for Canvas
        self.pathcanvas = cvs.PathCanvas(root, self.canvas, C_WIDTH, C_HEIGHT)

        ## binding mouse events to Canvas object in tk frame, and tying them to functions in PathCanvas object
        self.canvas.bind("<Button-1>", self.pathcanvas.pen)
        self.canvas.bind("<Motion>", self.pathcanvas.draw_polyline)
        self.canvas.bind("<ButtonRelease-1>", self.pathcanvas.pen)

        ## pack canvas
        self.canvas.pack(side="top", fill="both", expand=False)

        ## GUI -- Path length display
        length_frame = tk.Frame(root)
        length_label = tk.Label(length_frame, text="Path Length:")
        length_entry = tk.Entry(length_frame, width=8, state="disabled")
        length_frame.pack(side="top")
        length_label.pack(side="left")
        length_entry.pack(side="left")

    ## returns pointer position
    def get_pointer_pos(self, event):
        print(event.x, event.y)
        return (event.x, event.y)

if __name__ == "__main__":
    ## tkinter application root
    root = tk.Tk()

    ## define window properties
    root.title("dollarstore-recognizer v%s" % VERSION)
    root.minsize(300, 500)
    root.maxsize(300, 500)

    ## organize root geometry as window
    MainApplication(root).pack(side="top", fill="both", expand=True)

    ## run loop
    root.mainloop()