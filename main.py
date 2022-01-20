"""
name: main.py -- dollarstore-recognizer
description: An implementation of the $-recognizer in python with a Canvas input
authors: TJ Schultz, []
date: 1/20/22
"""
import os.path
import tkinter as tk
import canvas as cvs
import sys

## main application class defined for tkinter
class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        ## variable to show points when drawing
        self.show_points = tk.BooleanVar()

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
        self.canvas.bind("<ButtonRelease-1>", self.update_path)

        ## pack canvas
        self.canvas.grid(padx=100)
        self.canvas.pack(side="top", fill="both", expand=False)

        ## GUI -- Path length display
        self.length_frame = tk.Frame(root)
        self.length_label = tk.Label(self.length_frame, text="Path Length:")
        self.length_entry = tk.Entry(self.length_frame, width=8)
        self.length_frame.pack(side="top")
        self.length_label.pack(side="left")
        self.length_entry.pack(side="left")

        ## GUI -- Path length -- Path Points display
        self.points_check = tk.Checkbutton(self.length_frame, text="Show points",\
                                           variable=self.show_points,\
                                           onvalue=True, offvalue=False)
        self.points_check.pack(side="left")

        ## GUI -- App info
        self.info_frame = tk.Frame(root)
        self.info_button = tk.Button(self.info_frame, text="?", command=self.info_window, font="d",\
                                     bg="medium sea green")
        self.info_button.pack(side="right")
        self.info_frame.pack(side="bottom")

    ## prompts new info window for app
    def info_window(self):
        window = tk.Toplevel()
        window.title("Info")

        ## open icon
        window.iconbitmap(os.path.join('resources', 'icon.ico'))

        info_text = "This is a tkinter application\n running on python %s and developed for open use by\n"\
        "TJ Schultz. 2022\n" \
        "\n\nDrag the mouse pointer to plot a single stroke path. Clicking again begins a new path.\n" \
        "Click the checkbox to plot the path points." % (sys.version)

        github_image = tk.PhotoImage(file=os.path.join('resources', 'qr.png'))

        info_label = tk.Label(window, text=info_text, justify="left")
        github_label = tk.Label(window, image=github_image)
        info_label.pack(side="top", fill="both", expand=False)
        github_label.pack(side="top", fill="both", expand=False)

    ## returns pointer position
    def get_pointer_pos(self, event):
        print(event.x, event.y)
        return (event.x, event.y)

    ## calls pen to end drawing and updates the path length entry
    def update_path(self, event):

        ## stops pen
        self.pathcanvas.pen(event)

        ## draws points if show_points
        self.pathcanvas.draw_points(self.show_points.get())

        ## updates previous path length display
        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, len(self.pathcanvas.path))
        self.length_entry.update()

if __name__ == "__main__":
    ## tkinter application root
    root = tk.Tk()

    ## open icon
    root.iconbitmap(os.path.join('resources', 'icon.ico'))

    ## define window properties
    root.title("dollarstore-recognizer")
    root.minsize(300, 500)
    root.maxsize(300, 500)

    ## organize root geometry as window
    MainApplication(root).pack(side="top", fill="both", expand=True)

    ## run loop
    root.mainloop()