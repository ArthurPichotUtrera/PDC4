import csv
import math
import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
#from template_feature_extraction import *

################### Creating and training a decision tree model #############################

def train_tree(features, classes):
    print 'Training decision tree'
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(features, classes)
    return clf

def train_rforest(features, classes, num_estimators):
    print 'Training random forest with ' + str(num_estimators) + ' estimators.'
    clf = RandomForestClassifier(n_estimators = num_estimators)
    clf = clf.fit(features, np.ravel(classes)) # ravel pour convertir 1d array jsais pas quoi
    return clf
