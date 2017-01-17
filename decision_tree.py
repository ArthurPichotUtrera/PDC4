import csv
import math
import numpy as np
from sklearn import tree
from template_feature_extraction import *

################### Feature Extraction Template #############################

poss_act_0 = ["hotkey"+str(i)+"0" for i in range(10)]
poss_act_1 = ["hotkey"+str(i)+"1" for i in range(10)]
poss_act_2 = ["hotkey"+str(i)+"2" for i in range(10)]
possible_actions = ['s', 'sBase', 'sMineral'] + poss_act_0 + poss_act_1 + poss_act_2

training_file = "../train.csv"
testing_file = "../test.csv"
#testing_file = "../train.csv"

# Get training data
features, classes = get_features(training_file)

# Learning
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, classes)

# Get testing data
test_features, row_names = get_features(testing_file)

# Make predictions
res = clf.predict(test_features)

# Print the number of correct predictions if we use same file for training and testing
if training_file == testing_file:
    ok = 0
    for i in range(row_names.shape[0]):
        if classes[i,0] == res[i]: ok += 1
    print(str(ok) + "/" + str(len(res)))

# Write predictions
ofile = open("../res.csv", 'w')
ofile.write("row ID,battleneturl\n")
for i in range(row_names.shape[0]):
    ofile.write(row_names[i,0] + "," + res[i] + "\n")

ofile.close()
