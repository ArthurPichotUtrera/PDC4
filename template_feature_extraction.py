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
    # Get data from csv into numpy ndarrays
    features = np.ndarray((0,len(possible_actions)))
    classes = np.ndarray((0,1))
    ifile = open(features_filename, 'rb')
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

########################### Predicting #################################

def predict(features_filename, testing_filename, output_filename):
    lines_train = range(len(features_filename)) #pu un truc dans le genre
    lines_validate = []
    model, accuracy = train_validate(features_filename, lines_train, lines_validate)
    #Todo: ouvrir le fichier testing en read, output en write
    #Todo: utiliser le modele sur chaque ligne et ecrire le resultat dans l'output.
    return

####################### Training and Validating #############################

def train_validate(features_filename, lines_train, lines_validate):
    features, classes = get_features(features_filename)
    model = [] #train_decision_tree(features_filename, lines_train)
    accuracy = validate(model, features_filename, lines_validate)

    return model, accuracy

####################### What we actually do ####################################



input_filename = "first_100_train.csv"
output_filename = "features_first100_train.csv"

extract_features("first_100_train.csv", "features_first100_train.csv")


################################################################################
