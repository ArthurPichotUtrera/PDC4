import csv
import math
import numpy as np

################### Feature Extraction Template #############################

poss_act_0 = ["hotkey"+str(i)+"0" for i in range(10)]
poss_act_1 = ["hotkey"+str(i)+"1" for i in range(10)]
poss_act_2 = ["hotkey"+str(i)+"2" for i in range(10)]
possible_actions = ['s', 'sBase', 'sMineral'] + poss_act_0 + poss_act_1 + poss_act_2

filename = "../train.csv"

def get_features(filename):
    # Get data
    features = np.ndarray((0,len(possible_actions)))
    classes = np.ndarray((0,1))
    ifile = open(filename, 'rb')
    reader = csv.reader(ifile)
    next(reader) # Skip header

    for row in reader:
        classes = np.append(classes, [[row[0].split(";")[0]]], axis=0)
        tmp = list()
        nb_of_actions = (len(row) - 1)/2
        for action in possible_actions:
            count = row.count(action)
            if nb_of_actions > 0 :
                #print(row.count(action))
                #print("   "+str(1000*row.count(action)/float(nb_of_actions)))
                tmp.append(1000*row.count(action)/float(nb_of_actions)) # /float(nb_of_actions)
            else:
                tmp.append(0)
        features = np.append(features, [tmp], axis=0)

    ifile.close()

    return(features, classes)
