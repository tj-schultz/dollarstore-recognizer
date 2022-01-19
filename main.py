"""
name: main.py -- dollarstore-recognizer
description: An implementation of the 1$-recognizer in python with a canvas input
authors: TJ Schultz, []
date: 1/16/22
"""

import tkinter as tk
import canvas as cvs
import path as pth

VERSION = "0.1"

## main application class defined for tkinter
class MainApplication(tk.Frame):

    canvas = None
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        ## define canvas properties
        C_WIDTH = 300
        C_HEIGHT = 300
        canvas = cvs.Canvas(root, width=C_WIDTH, height=C_HEIGHT, bg="lightgrey",\
                            highlightthickness=5, highlightbackground="medium sea green")
        canvas.pack(side="top", fill="both", expand=False)
        canvas.bind("<Button-1>", canvas.pen)  # On Mouse left click
        canvas.bind("<Motion>", canvas.draw_polyline(canvas=canvas))
        canvas.bind("<ButtonRelease-1>", canvas.toggle_down())


if __name__ == "__main__":
    ## tkinter application root
    root = tk.Tk()

    ## define window properties
    root.title("dollarstore-recognizer v%s" % VERSION)
    root.minsize(300, 500)

    ## organize root geometry as window
    MainApplication(root).pack(side="top", fill="both", expand=True)

    ## run loop
    root.mainloop()