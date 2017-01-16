import csv

################### Feature Extraction Template #############################

poss_act_1 = ["hotkey"+str(i)+"1" for i in range(10)]
poss_act_2 = ["hotkey"+str(i)+"2" for i in range(10)]
possible_actions = ['s', 'sBase', 'sMineral'] + poss_act_1 + poss_act_2


ifile = open("first_100_train.csv", 'rb')
reader=csv.reader(ifile)
ofile = open("features_first100_train.csv", 'r+')
#writer = csv.writer(ofile, delimiter=';')

rownum = 1
newrow = ''

for row in reader:
    if rownum <= 1000:
        colnum = 0
        newrow= row[0] + ", " + row[1]
        for action in possible_actions:
            newrow += ", " + str(row.count(action))

        #for col in row:
        #    if colnum == 0:
        #        newrow = col
        #    if colnum != 0 and not col.isdigit():
        #        newrow += col + ", "
        #    colnum += 1
        ofile.write(newrow + "\n")
        newrow=''
        rownum += 1

ifile.close()
ofile.close()

#Format de sortie: Nom, Faction, s, sBase, sMineral, hotkey01, ..., hotkey 91,
# hohtkey02, ..., hotkey 92
