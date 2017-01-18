import csv
import math
import numpy as np


maxlines = 999999

################### Feature Extraction #########################################

def extract_features(input_filename, output_filename, num_rows=maxlines): #Num rows est
#le nombre max de lignes a traiter. Par defaut pas de limite

    ifile = open(input_filename, 'rb')
    reader = csv.reader(ifile)
    ofile = open(output_filename, 'w')

    # header = "Name"#, Faction"
    # for action in possible_actions:
    #     header += ", " + action
    #
    # ofile.write(header + "\n")

    rownum = 1

    head = reader.next()
    for row in reader:
        features = list()
        #Ici extraction et ecriture des features de chaque ligne
        if rownum <= num_rows: #Pour verifier sur quelques lignes au debut
            newrow = row[0].split(';')[0]
            #Extraction de features
            features.extend(frequence_actions(row))
            features.extend(faction(row))

            for feature in features:
                newrow +=  ", " + str(feature)
            ofile.write(newrow + "\n") #Inscription de la ligne sur le fichier
            rownum += 1

    ifile.close()
    ofile.close()
    return

############################################################

poss_act_0 = ["hotkey"+str(i)+"0" for i in range(10)]
poss_act_1 = ["hotkey"+str(i)+"1" for i in range(10)]
poss_act_2 = ["hotkey"+str(i)+"2" for i in range(10)]
possible_actions = ['s', 'sBase', 'sMineral'] + poss_act_0 + poss_act_1 + poss_act_2

def frequence_actions(row):
    """ Compute for each action its frequence """

    features = list()
    nb_actions = (len(row) - 1)/2
    for action in possible_actions:
        features.append(row.count(action)/float(nb_actions) if nb_actions > 0 else 0)
    return features

############################################################

def faction(row):
    """ Feature for the faction played. """

    faction = row[0].split(';')[1]
    if faction == "Protoss":
        features = [1,0,0]
    elif faction == "Zerg":
        features = [0,1,0]
    else:
        features = [0,0,1]
    return features
