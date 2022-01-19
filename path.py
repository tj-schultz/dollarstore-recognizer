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
    parsed_path = []

    def __init__(self, p):
        head = p
        self.parsed_path.append(p)

    def stitch(self, p):
        self.parsed_path.append(p)

    def get_length(self):
        return len(self.parsed_path)

    def display(self):
        print('Length:%s\tPath:\n' % len(self.parsed_path))
        for i in range(len(self.parsed_path)):
            print('%s, %s\n' % (self.parsed_path[i].x, self.parsed_path[i].y))
