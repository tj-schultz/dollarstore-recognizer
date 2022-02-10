"""
name: offline.py -- dollarstore-recognizer
description: alternative launch to perform a recognition loop
and log results offline
authors: TJ Schultz, Skylar McCain
date: 2/01/22
"""

from curses import keyname
from xml.dom.minidom import parse
import xml.dom.minidom as xmlmd
import csv
import os
import path as pth
import recognizer as rec
import dollar
import random
import pandas as pd

## list of path types to read using filenames with '01-10' appended
xml_filetypes = ["arrow", "caret", "check", "circle", "delete_mark", "left_curly_brace",\
                 "left_sq_bracket", "pigtail", "question_mark", "rectangle",\
                 "right_curly_brace", "right_sq_bracket", "star", "triangle",\
                 "v", "x"]

## base dictionary of unprocessed input Path objects from xml
xml_base = {}



## reads a single xml file as a DOM element, records gesture and returns the path object
def read_XML_path(filepath):

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
            x = int(point.getAttribute("X"))
            y = int(point.getAttribute("Y"))
            xml_path.stitch(pth.Point(x, y))

    except:
        print("Unable to read", filepath, "\n")

    return xml_path

def random100_test(R):
    # dictionary to represent columns in output cvs file - converted to dataframe at end
    output = {
        'User' : [],
        'GestureType' : [],
        'RandomIteration' : [],
        'NumberOfTraningExamples(E)': [],
        'TotalSizeOfTrainingSet' : [],
        'TrainingSetContents' : [],
        'Canidate' : [],
        'RecoResultGesture' : [],
        'Correct/Incorrect' : [],
        'RecoResultScore' : [],
        'RecoResultBestMatch' : [],
        'RecoResultN-BestList' : []
    }
    # dictionary to store random list of templates each repetion of random100, size = 16 * e
    templates = {}
    # to store one randomly selected canidate for each gesture, size = 16
    canidates = {}
    for user in R.preprocessed:
        for e in range(1,9):
            for i in range(1,100):
                for gesture in R.preprocessed[user]:
                    canidates[gesture] = {}
                    for temp in random.sample(R.preprocessed[user][gesture].keys(), e + 1):
                        id = "_".join([gesture,temp])
                        templates[id] = R.preprocessed[user][gesture][temp]
                    canidates[gesture][id] = templates.pop(id)
                for gesture in canidates.keys():
                    for canidate in canidates[gesture]:

                        #call recognizer on canidate with list of randomly generated templates from above
                        n_best = R.recognize(canidates[gesture][canidate],templates)
                    
                        #write row elements to output dictionary
                        output['User'].append(user)
                        output['GestureType'].append(gesture)
                        output['RandomIteration'].append(i)
                        output['NumberOfTraningExamples(E)'].append(e)
                        output['TotalSizeOfTrainingSet'].append(e*16)
                        output['TrainingSetContents'].append(list(templates.keys()))
                        output['Canidate'].append(canidate)

                        #gets string of result gesture type
                        reco_gesture = n_best[0][0].rsplit('_',1)[0]
                        output['RecoResultGesture'].append(reco_gesture)
                        output['Correct/Incorrect'].append('correct' if reco_gesture == gesture else 'incorrect')
                        output['RecoResultScore'].append(n_best[0][1])
                        output['RecoResultBestMatch'].append(n_best[0][0])
                        output['RecoResultN-BestList'].append(n_best)
                        #if correct
                            #score++
                        #write score/100 to output-doc at user, gesture, level e
                        
                templates.clear()
                canidates.clear()
    output_df = pd.DataFrame(output)
    output_df.to_csv('random100_test_output.csv')
   


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
                xml_base[user_key][prefix][file_key] = read_XML_path(\
                    os.path.join("xml", user_key, "slow", "%s%s.xml"\
                                 % (prefix, file_key))
                )


    ## instantiate the recognizer and preprocess the template dictionary recursively
    R = rec.Recognizer(xml_base)
    random100_test(R)

    ## debug -- vectors should be of length 2 * 64 = 128
    # for user in R.preprocessed:
    #     for gesture in R.preprocessed[user]:
    #         for id in R.preprocessed[user][gesture].keys():
    #             print(user, gesture, id, "length:", len(xml_base[user][gesture][id]))
    #             #R.recognize(R.preprocessed[user][gesture][id], R.preprocessed[user][gesture], preprocess=False)