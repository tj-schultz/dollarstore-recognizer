"""
name: recognizer.py -- dollarstore-recognizer
description: Recognizer class with member functions to resample, rotate, scale/translate paths and
run calculations to determine the score for a particular recognizer
authors: TJ Schultz, []
date: 1/26/22
"""
import math
import path as pth
import dollar

## recognizer class containing canvas display methods for
class Recognizer():

    ##
    class RotationSet():

        ## for this particular project, the rotations are through 90, 180, and 270
        rotations = [90, 180, 270]

        def __init(self, templates):


        def rotate_path(self, path):
            for
    def __init__(self):


    ## returns distance between points in non-pixel units
    def distance(self, p1, p2):
        return math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))

    ## gets the path length as a sum of distances
    def path_length(self, path):
        d = 0

        ## add distances
        for i in range(len(path) - 1):
            d = d + self.distance(path.parsed_path[i], path.parsed_path[i + 1])

        return d

    ## resamples a path into n evenly spaced points
    def resample(self, path, n):
        if n <= 0:
            return []

        interval = self.path_length(path) / (n - 1)
        dist = 0

        ## create a copy path
        copy = path

        ## create return path
        new_path = pth.Path(path.parsed_path[0])

        i = 1
        while i < len(copy) - 1:

            ## get points
            p1 = path.parsed_path[i]
            p2 = path.parsed_path[i + 1]

            ## calc distance
            d = self.distance(p1, p2)
            if dist + d > interval:

                ## interpolate new values
                qx = p1.x + (((interval - dist) / d) * (p2.x - p1.x))
                qy = p1.y + (((interval - dist) / d) * (p2.y - p1.y))
                q = pth.Point(qx, qy)

                ## stitch point to new path and copy point to copy path
                new_path.stitch(q)
                copy.insert(i + 1, q)

                ## reset dist
                dist = 0
            else:
                ## add distance
                dist = dist + d
            i = i + 1

        return new_path

    ## returns tuple of point coordinate mins and max
    def bbox(self, path):
        x_min, x_max, y_min, y_max = (0, 0, 0, 0)

        for p in path.parsed_path:
            if p.x <= x_min:
                x_min = p.x
            elif p.x >= x_max:
                x_max = p.x
            if p.y <= y_min:
                y_min = p.y
            elif p.y >= y_max:
                y_max = p.y
        return (x_min, x_max, y_min, y_max)

    def centroid(self, path):
        (x_min, x_max, y_min, y_max) = self.bbox(path)
        x = x_min + ((x_max - x_min) / 2.0)
        y = y_min + ((y_max - y_min) / 2.0)
        return pth.Point(x, y)

    ## rotates path by theta
    def rotate_by(self, path, theta):

        rotated = pth.Path()

        ## calc centroid
        cent = self.centroid(path)

        ## perform rotation for each point
        for p in path.parsed_path:
            qx = ((p.x - cent.x) * math.cos(theta)) - \
                 ((p.y - cent.y) * math.sin(theta)) + cent.x
            qy = ((p.x - cent.x) * math.sin(theta)) + \
                 ((p.y - cent.y) * math.cos(theta)) + cent.y
            rotated.stitch(pth.Point(qx, qy))

        return rotated

    ## rotates the points so their indicative angle is 0 degrees
    def rotate_to_zero(self, path):
        cent = self.centroid(path)
        theta = math.atan((cent.y - path.parsed_path[0].y) / (cent.x - path.parsed_path[0].x))
        new_path = self.rotate_by(path, (theta * -1.0))
        return new_path

    ## scales points to square aspect ratio
    def scale_to_square(self, path, size):

        ## get bbox info
        bbox = self.bbox(path)
        b_width = bbox[1] - bbox[0]
        b_height = bbox[3] - bbox[2]

        new_path = pth.Path()

        for p in path.parsed_path:
            qx = p.x * (size / b_width)
            qy = p.y * (size / b_width)
            new_path.stitch(pth.Point(qx, qy))

        return new_path

    ## translates points around the origin
    def translate_to_origin(self, path):
        cent = self.centroid(path)

        new_path = pth.Path()

        for p in path.parsed_path:
            qx = p.x - cent.x
            qy = p.y - cent.y
            new_path.stitch(pth.Point(qx, qy))

        return new_path

    ## preprocess path to compare
    def preprocess(self, path):
        ## resample the points
        new_path = self.resample(path, dollar.Dollar.prefs["n_points"])

        ## rotate to indicative angle
        new_path = self.rotate_to_zero(new_path)

        ## scale to size box
        new_path = self.scale_to_square(new_path, dollar.Dollar.prefs["square_size"])

    ## recognizer method -- combines steps in performing scoring
    def recognize(self, path):

        ## preprocess the candidate path
        candidate = self.preprocess(path)