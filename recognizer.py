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

    preprocessed = {}

    ## preprocess the template set on init
    def __init__(self, template_dict):

        ## copy template dictionary
        self.preprocessed = template_dict

        for t_key in template_dict.keys():
            ## create a Path object
            new_path = pth.Path(template_dict[t_key])

            ## preprocess and replace the point list with the Path object
            new_path = self.preprocess(new_path)
            self.preprocessed[t_key] = new_path
            #print(t_key, len(self.preprocessed[t_key]))


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
        if n <= 1:
            return path

        interval = self.path_length(path) / (n - 1)
        print("interval ", interval)
        dist = 0

        ## create a copy path
        copy = path

        ## create return path
        new_path = pth.Path(path.parsed_path[0])

        i = 1
        while i < len(copy) - 1 and len(new_path) < n:
            print(i, len(copy), len(new_path))

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
            elif p.x > x_max:
                x_max = p.x
            if p.y <= y_min:
                y_min = p.y
            elif p.y > y_max:
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

        print(b_width, b_height)

        new_path = pth.Path()

        for p in path.parsed_path:
            qx = p.x * (size / b_width)
            qy = p.y * (size / b_height)
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

    ## sum and average distance between two point paths
    def path_distance(self, A, B):
        d = 0
        for i in range(min(len(A), len(B))):
            d = d + self.distance(A.parsed_path[i], B.parsed_path[i])
        return d / min(len(A), len(B))

    ## distance at angle
    def distance_at_angle(self, path, template, theta):
        new_path = self.rotate_by(path, theta)
        d = self.path_distance(new_path, template)
        return d


    ## distance at best angle with default parameters for theta a, b and delta
    def distance_best_angle(self, path, template, atheta=-45, btheta=45, delta=2):

        ## calculate golden const
        PHI = round(0.5 * (-1.0 + math.sqrt(5)), 5)

        ## calculated variables
        x1 = (PHI * atheta) + ((1.0 - PHI) * btheta)
        f1 = self.distance_at_angle(path, template, x1)

        x2 = ((1.0 - PHI) * atheta) + (PHI * btheta)
        f2 = self.distance_at_angle(path, template, x2)

        ## find the optimum angle using delta
        while btheta - atheta > delta:
            if f1 < f2:
                btheta = x2
                x2 = x1
                f2 = f1
                x1 = (PHI * atheta) + ((1.0 - PHI) * btheta)
                f1 = self.distance_at_angle(path, template, x1)
            else:
                atheta = x1
                x1 = x2
                f1 = f2
                x2 = ((1.0 - PHI) * atheta) + (PHI * btheta)
                f2 = self.distance_at_angle(path, template, x2)

        ## return the minimum distance from f1, f2
        return min(f1, f2)


    ## preprocess path to compare
    def preprocess(self, path):
        ## resample the points
        new_path = self.resample(path, dollar.Dollar.prefs["n_points"])

        ## rotate to indicative angle
        new_path = self.rotate_to_zero(new_path)

        ## scale to size box
        new_path = self.scale_to_square(new_path, dollar.Dollar.prefs["square_size"])

        ## translate to origin
        new_path = self.translate_to_origin(new_path)

        return new_path

    ## recognizer method -- combines steps in performing scoring
    def recognize(self, path):

        if len(path) < 1:
            return

        ## preprocess the candidate path into a Path object
        candidate = self.preprocess(path)

        ## for each preprocessed template, compare the path and calculate the max score
        b = dollar.Dollar.prefs["square_size"]
        tprime = ""
        hd = (0.5 * math.sqrt(2.0 * math.pow(dollar.Dollar.prefs["square_size"], 2)))
        for t_key in self.preprocessed.keys():

            d = self.distance_best_angle(candidate, self.preprocessed[t_key])
            print(t_key, (1.0 - (d / hd)))
            ## if a new best match is found
            if d < b:
                b = d
                tprime = t_key  ## set t_key for output

        ## calculate final score
        score = 1.0 - (b / hd)
        return (tprime, score)