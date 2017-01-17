import csv
import numpy as np
from sklearn import tree

################### Feature Extraction Template #############################

poss_act_0 = ["hotkey"+str(i)+"0" for i in range(10)]
poss_act_1 = ["hotkey"+str(i)+"1" for i in range(10)]
poss_act_2 = ["hotkey"+str(i)+"2" for i in range(10)]
possible_actions = ['s', 'sBase', 'sMineral'] + poss_act_0 + poss_act_1 + poss_act_2

training_file = "../train.csv"
testing_file = "../test.csv"

# Get training data
features = np.ndarray((0,33))
classes = np.ndarray((0,1))
ifile = open(training_file, 'rb')
reader = csv.reader(ifile)
next(reader) # Skip header

for row in reader:
    classes = np.append(classes, [[row[0].split(";")[0]]], axis=0)

    tmp = list()
    nb_of_actions = len(row) - 1
    for action in possible_actions:
        count = row.count(action)
        if nb_of_actions > 0 :
            tmp.append(row.count(action)) #/float(nb_of_actions)
        else:
            tmp.append(0)
    features = np.append(features, [tmp], axis=0)

ifile.close()

# Learning
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, classes)

# Get testing data
ifile = open(testing_file, 'rb')
reader = csv.reader(ifile)
next(reader) # Skip header

test_features = np.ndarray((0,33))
row_names = []
for row in reader:
    row_names.append(row[0].split(";")[0])
    tmp = list()
    for action in possible_actions:
        tmp.append(row.count(action))
    test_features = np.append(test_features, [tmp], axis=0)
ifile.close()

# Make predictions
res = clf.predict(test_features)

# Print the number of correct predictions if we use same file for training and testing
if training_file == testing_file:
    ok = 0
    for i in range(len(res)):
        if classes[i,0] == res[i]: ok += 1
    print(str(ok) + "/" + str(len(res)))

# Write predictions
ofile = open("../res.csv", 'w')
ofile.write("row ID,battleneturl\n")
for i, name in enumerate(row_names):
    ofile.write(name + "," + res[i] + "\n")

ofile.close()
