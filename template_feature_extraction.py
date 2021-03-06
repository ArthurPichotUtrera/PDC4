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

    rownum = 1

    head = reader.next()
    for row in reader:
        features = list()
        #Ici extraction et ecriture des features de chaque ligne
        if rownum <= num_rows: #Pour verifier sur quelques lignes au debut
            newrow = row[0].split(';')[0]
            #Extraction de features
            features.extend(get_first_action_frames(row))
            features.extend(faction(row))

            row = get_x_first_frames(row, 2000)

            features.extend(frequence_actions(row))
            features.extend(get_mean_frequency(row))
            features.extend(get_frequency_histogram(row))

            #Add features in new row, then write in file
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

# TODO: Faire 3 modeles
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

##################################################################

def get_first_action_frames(row):
    """ Compute the frame of the first s, sBase, sMineral. """
    features = []
    for action in ['s', 'sBase', 'sMineral']:
        i=1
        first_frame = 10000
        while i < len(row):
            if row[i] == action:
                first_frame = row[i+1]
                break
            i += 2
        features.append(first_frame)
    return features
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
