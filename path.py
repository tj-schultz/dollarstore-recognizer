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
    parsed_path = [256]
    head = None

    def __init__(self, p):
        head = p
        self.parsed_path[-1] = p

    def append(self, p):
        self.parsed_path[-1] = p