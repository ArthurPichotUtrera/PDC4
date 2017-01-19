import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, linear_model as lm
from sklearn.feature_selection import RFE, RFECV

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

def train_rforest_rfe(features, classes, num_estimators):
    print 'Training random forest with ' + str(num_estimators) + ' estimators, and RFE'
    estimator = RandomForestClassifier(n_estimators = num_estimators)
    #selector = RFE(estimator, 5, step=1, n_jobs=-1)
    selector = RFECV(estimator, n_jobs=-1)
    print "Evaluation de l'importance des features"
    selector = selector.fit(features, classes)
    print("Optimal number of features: %d" % selector.n_features_)
    print "Selected features:"
    print selector.support_
    print "Ranking:"
    print selector.ranking_

    plt.figure()
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(selector.grid_scores_) + 1), selector.grid_scores_)
    plt.show()

    estimator = estimator.fit(features, np.ravel(classes)) # ravel pour convertir 1d array jsais pas quoi
    return estimator

def train_svm(features, classes):
    print 'Training svm'
    clf = svm.SVC() #Ou NuSVC, ou LinearSVC
    clf = clf.fit(features, np.ravel(classes)) # ravel pour convertir 1d array jsais pas quoi
    return clf

def train_logistic(features, classes):
    print 'Training logistic regression'
    clf = lm.LogisticRegression()
    return clf.fit(features, np.ravel(classes))
