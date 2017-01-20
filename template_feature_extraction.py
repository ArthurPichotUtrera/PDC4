import csv
import math
import numpy as np
import string
from wagnerfischerpp import *

maxlines = 999999

################### Feature Extraction #########################################

def extract_features(input_filename, lines_train, players_per_faction, nb_rows, num_rows=maxlines): #Num rows est
#le nombre max de lignes a traiter. Par defaut pas de limite

    ifile = open(input_filename, 'rb')
    reader = csv.reader(ifile)
    # reader.next()
    ofile_protoss = open("features_protoss.csv", 'w')
    ofile_terran = open("features_terran.csv", 'w')
    ofile_zerg = open("features_zerg.csv", 'w')

    for num_row, row in enumerate(reader):
        features = list()
        #Ici extraction et ecriture des features de chaque ligne
        if num_row <= num_rows: #Pour verifier sur quelques lignes au debut
            newrow = row[0].split(';')[0]
            faction = row[0].split(';')[1]
            # row = get_x_first_frames(row, 2000) # TODO: A tester

            #Extraction de features
            features.extend(frequence_actions(row))
            features.extend(get_mean_frequency(row))
            features.extend(get_frequency_histogram(row))

            # TODO: lines_train attention
            # features.extend(get_sequence_dissimilarity(row, players_per_faction, lines_train, 20))

            features.extend(get_row_position(num_row, nb_rows)) # TODO moins bien pour zerg ???

            #Add features in new row, then write in file
            for feature in features:
                newrow +=  ", " + str(feature)
            # Write features in the right file
            if faction == "Protoss":
                ofile_protoss.write(newrow + "\n")
            elif faction == "Terran":
                ofile_terran.write(newrow + "\n")
            else:
                ofile_zerg.write(newrow + "\n")

    ifile.close()
    ofile_protoss.close()
    ofile_terran.close()
    ofile_zerg.close()

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

# TODO: Faire 3 modeles
def faction(row):
    """ Feature for the faction played. """

    faction = row[0].split(';')[1]
    if faction == "Protoss":
        features = [1,0,0]
    elif faction == "Terran":
        features = [0,1,0]
    else:
        features = [0,0,1]
    return features

############################################################

def get_x_first_frames(row, x):

    i = 1
    res = [row[0]]

    while i+1 < len(row) and int(row[i+1]) <= x:
        res.append(row[i])
        res.append(row[i+1])
        i += 2
    return res

############################################################

# TODO: Distinguer les actions avec le clavier et les actions avec la sourie ??
def get_mean_frequency(row, before_frame_x = float('inf')):
    """ Frequence moyenne entre deux actions """
    # TODO: before frame x
    frames = row[len(row)-1]
    nb_actions = (len(row)-1)/2

    try:
        return [nb_actions/float(frames)]
    except ValueError:
        return [0]

############################################################

# TODO: Distinguer les actions avec le clavier et les actions avec la sourie
def get_frequency_histogram(row, before_frame_x = float('inf')):
    """ Retourne un histogramme contenant le pourcentage d'actions realisees de 0, 1, 2, ... x frames de l action precedente.  """

    nb_actions = (len(row)-1)/2
    i = 1
    frame_previous_action = 0
    x = 6
    histogram = [0]*x
    while i+1 < len(row) and int(row[i+1]) <= before_frame_x:
        delta = int(row[i+1]) - frame_previous_action
        if delta < x:
            histogram[delta] += 1
        frame_previous_action = int(row[i+1])
        i += 2
    for i in range(x):
        histogram[i] /= float(nb_actions)
    return histogram

############################################################

actions_sequence = poss_act_0 + poss_act_1 + poss_act_2 #['s', 'sBase', 'sMineral'] + poss_act_0 + poss_act_1 + poss_act_2

letters = list(string.ascii_letters)

def action_to_letter(action):
    if action in actions_sequence:
        return letters[actions_sequence.index(action)]
    return ""

def get_sequence_dissimilarity(row, players_per_faction, lines_train, nb_actions_max = float('inf')):
    """ Similarite max pour chacun des players. """

    faction = row[0].split(';')[1]
    # Noms des joueurs possibles
    if faction == "Protoss":
        f = 0
    elif faction == "Terran":
        f = 1
    else:
        f = 2
    names = players_per_faction[f]
    mins = [1]*len(names)
    ifile = open("sequence_keys.csv", 'r')
    reader = csv.reader(ifile)
    # reader.next()
    row_seq = ""
    a = 1
    while a*2-1 < len(row) and len(row_seq) < nb_actions_max:
        row_seq += action_to_letter(row[a*2-1])
        a += 1

    i = 0 # On utilise a_row si la ligne fait partie du training
    for a_row in reader:
        # Get player name
        a_name = a_row[0].split(';')[0]
        a_faction = a_row[0].split(';')[1]
        if a_faction == faction : # Si
            if i in lines_train[f]:
                n = names.index(a_name)
                # Get firsts actions
                a_row_seq = a_row[1][:nb_actions_max]
                # Get distance
                if len(a_row_seq) != len(row_seq[:len(a_row_seq)]): print a_row_seq + "    " + row_seq
                distance = WagnerFischer(a_row_seq, row_seq[:len(a_row_seq)]).cost
                # update
                if mins[n] > distance/float(len(a_row_seq)):
                    mins[n] = distance/float(len(a_row_seq))
            i += 1
    return mins


############################################################

def create_sequence_file(filename = "train_clean.csv"):
    ifile = open(filename, 'r') # TODO: filename in parameter
    reader = csv.reader(ifile)
    # reader.next()
    ofile = open("sequence_"+filename, 'w')
    # ofile.write("player;faction,sequence\n")

    for row in reader:
        new_row = row[0] + ","
        a = 1
        while a*2 - 1 < len(row): #and a <= nb_actions_max
            new_row += action_to_letter(row[a*2 - 1])
            a += 1
        ofile.write(new_row + "\n")

    ifile.close()
    ofile.close()

#create_sequence_file()

############################################################

def get_row_position(num_row, nb_rows):
    return [num_row/float(nb_rows)]
