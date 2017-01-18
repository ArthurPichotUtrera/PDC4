import csv
import math
import numpy as np


maxlines = 999999
poss_act_0 = ["hotkey"+str(i)+"0" for i in range(10)]
poss_act_1 = ["hotkey"+str(i)+"1" for i in range(10)]
poss_act_2 = ["hotkey"+str(i)+"2" for i in range(10)]
possible_actions = ['s', 'sBase', 'sMineral'] + poss_act_0 + poss_act_1 + poss_act_2

################### Feature Extraction #########################################

def extract_features(input_filename, output_filename, num_rows=maxlines): #Num rows est
#le nombre max de lignes a traiter. Par defaut pas de limite

    ifile = open(input_filename, 'rb')
    reader=csv.reader(ifile)
    ofile = open(output_filename, 'r+')

    header = "Name"#, Faction"
    for action in possible_actions:
        header += ", " + action

    ofile.write(header + "\n")

    rownum = 1
    newrow = ''

    head = reader.next()
    for row in reader:
        #Ici extraction et ecriture des features de chaque ligne
        if rownum <= num_rows: #Pour verifier sur quelques lignes au debut
            colnum = 0
            newrow = row[0].split(';')[0]# + ", " + row[1] #Le nom du joueur# puis la faction
            for action in possible_actions:
                newrow += ", "  + str(row.count(action))
            ofile.write(newrow + "\n") #Inscription de la ligne sur le fichier
            newrow = ''
            rownum += 1

    ifile.close()
    ofile.close()
    return
