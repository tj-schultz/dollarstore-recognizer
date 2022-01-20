"""
name: path.py -- dollarstore-recognizer
description: Path and point object definitions
authors: TJ Schultz, []
date: 1/14/22
"""

## point class
class Point():
    ## point coordinates
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

## path class
class Path():
    parsed_path = None

    def __init__(self, p=None):

        self.parsed_path = []
        if p is not None:
            self.stitch(p)


    def __len__(self):
        return len(self.parsed_path)

    def __str__(self):
        path_str = 'Path length: %s\tPath:\n' % len(self)
        for p in self.parsed_path:
            path_str += ('->(%s,%s)' % (p.x, p.y))
        return path_str

    def stitch(self, p):
        self.parsed_path.append(p)
