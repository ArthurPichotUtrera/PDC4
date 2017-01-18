import csv
import math
import numpy as np
from decision_tree import train_tree
from decision_tree import train_rforest
from decision_tree import train_svm, train_logistic
from template_feature_extraction import extract_features
from random import randint

maxlines = 999999

####################### Getting the features ###################################

def get_features(features_filename, lines_train=range(maxlines)):
    # Lit les features d'un fichier csv avec un header coherent.
    # Separe les features des lignes de training et les features des lignes de validation.
    # Si on veut les features de tout le fichier, ne pas specifier lines_train.

    # Get features from csv at lines specified into numpy ndarrays. Csv must have a coherent header.
    ifile = open(features_filename, 'rb')
    reader = csv.reader(ifile)

    header = next(reader)

    features_train = np.ndarray((0,len(header)-1)) # -1 parce que le nom n'est pas une feature.
    features_validate = np.ndarray((0,len(header)-1))
    classes_train = np.ndarray((0,1))
    classes_validate = np.ndarray((0,1))

    for row in reader:
        if reader.line_num in lines_train:
            classes_train = np.append(classes_train, [[row.pop(0)]], axis=0)
            row_float = []
            for col in row:
                row_float += [float(col)]
            features_train = np.append(features_train,[row_float], axis=0)
        else:
            classes_validate = np.append(classes_validate, [[row.pop(0)]], axis=0)
            row_float = []
            for col in row:
                row_float += [float(col)]
            features_validate = np.append(features_validate, [row_float], axis=0)

    ifile.close()
    print "Extracted features from " + features_filename
    return features_train, features_validate, classes_train, classes_validate

############################# Getting features from testing data ######################
def get_features_test(features_filename):
    features, useless_validation, classes, useless_validate_classes = get_features(features_filename)
    # On utilise la fonction precedente avec toutes les lignes dans le "train". les
    # classes ne nous interessent pas car elles sont anonymes.
    return features, classes


####################### Validating #############################################

def validate(model, features, classes):
    predictions = model.predict(features)
    print "Prediction des classes"
    accuracy = 0
    num_features = features.shape[0]
    print "Taille de validation: "
    print num_features
    print "Comparaison des classes"
    for i in range(num_features):
        if predictions[i] == classes[i]:
            accuracy += 1./num_features
    print "Precision: " + str(accuracy)
    return accuracy

####################### Training and Validating ################################

def train_validate(features_filename, lines_train=range(maxlines)):
    features_train, features_validate, classes_train,  classes_validate = get_features(features_filename, lines_train)
    #model = train_tree(features_train, classes_train)
    model = train_rforest(features_train, classes_train, 200)
    #model = train_svm(features_train, classes_train)
    #model = train_logistic(features_train, classes_train)

    if lines_train == range(4200): # Si on entraine sur toutes les lignes
        print "Pas de validation, la mesure de la precision se fait sur le training dataset"
        accuracy = validate(model, features_train, classes_train)
    else:
        print "Mesure de la precision sur le validation dataset"
        accuracy = validate(model, features_validate, np.ravel(classes_validate))

    return model, accuracy

########################### Predicting ########################################

def predict(model, testing_features_filename, output_filename):
    features, classes = get_features_test(testing_features_filename)
    predictions = model.predict(features)

    ofile = open(output_filename, 'r+')
    ofile.write("row ID,battleneturl\n")

    for i in range(features.shape[0]):
        ofile.write(classes[i,0] + "," + predictions[i] + "\n")

    ofile.close()
    print "Prediction done and written in " + output_filename
    return

####################### What we actually do ####################################

#extract_features("first_100_train.csv", "features_first100_train.csv")
#extract_features("first_100_test.csv", "features_first100_test.csv")

#extract_features("train.csv", "features_train.csv")
#extract_features("test.csv", "features_test.csv")

# Selection de 300 lignes environs pour la validation
lines_train = range(4200)
#for i in range(350):
#    lines_train.pop(randint(0,len(lines_train)-1))

model, accuracy = train_validate("features_train.csv", lines_train)
predict(model, "features_test.csv", "res.csv")

################################################################################
