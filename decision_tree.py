import csv
import math
import numpy as np
from sklearn import tree
#from template_feature_extraction import *

################### Creating and training a decision tree model #############################

def train_tree(features, classes):

    # Learning
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(features, classes)
    return clf
