import csv
import math
import numpy as np
#from decision_tree import *


poss_act_0 = ["hotkey"+str(i)+"0" for i in range(10)]
poss_act_1 = ["hotkey"+str(i)+"1" for i in range(10)]
poss_act_2 = ["hotkey"+str(i)+"2" for i in range(10)]
possible_actions = ['s', 'sBase', 'sMineral'] + poss_act_1 + poss_act_2

################### Feature Extraction #############################

def extract_features(input_filename, output_filename, num_rows=9999999999): #Num rows est
#le nombre max de lignes a traiter. Par defaut pas de limite

    ifile = open(input_filename, 'rb')
    reader=csv.reader(ifile)
    ofile = open(output_filename, 'r+')

    header = "Name, Faction"
    for action in possible_actions:
        header += ", " + action

    ofile.write(header + "\n")

    rownum = 1
    newrow = ''
    for row in reader:
        #Ici extraction et ecriture des features de chaque ligne
        if rownum <= num_rows: #Pour verifier sur quelques lignes au debut
            colnum = 0
            newrow = row[0] + ", " + row[1] #Le nom du joueur puis la faction
            for action in possible_actions:
                newrow += ", "  + str(row.count(action))
            ofile.write(newrow + "\n") #Inscription de la ligne sur le fichier
            newrow = ''
            rownum += 1

    ifile.close()
    ofile.close()
    return

####################### Training ###########################

def get_features(features_filename):
    # Get features from csv into numpy ndarrays
    ifile = open(features_filename, 'rb')
    reader = csv.reader(ifile)

    header = next(reader)

    features = np.ndarray((0,len(header)-1)) # -1 parce que le nom n'est pas une feature.
    classes = np.ndarray((0,1))


    for row in reader:
        classes = np.append(classes, [[row.pop(0)]], axis=0)
        features = np.append(features,[row], axis=0)

    print features
    ifile.close()
    return(features, classes)

########################### Predicting #################################

def predict(features_filename, testing_filename, output_filename):
    lines_train = range(len(features_filename)) #pu un truc dans le genre
    lines_validate = []
    model, accuracy = train_validate(features_filename, lines_train, lines_validate)
    #Todo: ouvrir le fichier testing en read, output en write
    #Todo: utiliser le modele sur chaque ligne et ecrire le resultat dans l'output.
    return

####################### Training and Validating #############################

def train_validate(features_filename, lines_train, lines_validate=[]):
    features, classes = get_features(features_filename)
    model = [] #train_decision_tree(features_filename, lines_train)
    accuracy = validate(model, features_filename, lines_validate)

    return model, accuracy

####################### What we actually do ####################################


#extract_features("first_100_train.csv", "features_first100_train.csv")
#train_validate("features_first100_train.csv", range(100))

features, classes = get_features('features_first100_train.csv')

################################################################################
