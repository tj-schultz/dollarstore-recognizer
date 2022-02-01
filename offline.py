"""
name: offline.py -- dollarstore-recognizer
description: alternative launch to perform a recognition loop
and log results offline
authors: TJ Schultz, Skylar McCain
date: 2/01/22
"""

from xml.dom.minidom import parse
import xml.dom.minidom as xmlmd
import csv
import os
import path as pth

## list of path types to read using filenames with '01-10' appended
xml_filetypes = ["arrow", "caret", "check", "circle", "delete_mark", "left_curly_brace",\
                 "left_sq_bracket", "pigtail", "question_mark", "rectangle",\
                 "right_curly_brace", "right_sq_bracket", "star", "triangle",\
                 "v", "x"]

## base dictionary of unprocessed input Path objects from xml
xml_base = {}

## reads a single xml file as a DOM element, records gesture and returns the path object
def readXMLpath(filepath):

    try:
        ## grab root of file
        tree = xmlmd.parse(filepath)
        element = tree.documentElement

        ## parse the point tags
        point_tags = element.getElementsByTagName("Point")

        ## formed path
        xml_path = pth.Path()

        ## get attributes and build path object
        for point in point_tags:
            x = point.getAttribute("X")
            y = point.getAttribute("Y")
            xml_path.stitch(pth.Point(x, y))

    except:
        print("Unable to read", filepath, "\n")

    return xml_path

if __name__ == "__main__":

    ## build xml_base
    for i in range(2, 12):                      ## for each user
        user_key = "s%s" % str(i).zfill(2)
        xml_base[user_key] = {}                 ## add user key-dict
        for prefix in xml_filetypes:            ## for each gesture
            xml_base[user_key][prefix] = {}     ## add prefix key-dict
            for num in range(1, 11):            ## for each sample xml
                file_key = str(num).zfill(2)

                ## read as DOM -- append to dictionary
                xml_base[user_key][prefix][file_key] = readXMLpath(\
                    os.path.join("xml", user_key, "medium", "%s%s.xml"\
                                 % (prefix, file_key))
                )

    for user in xml_base.keys():
        for gesture in xml_base[user]:
            for id in xml_base[user][gesture].keys():
                print(user, gesture, id, "length:", len(xml_base[user][gesture][id]))