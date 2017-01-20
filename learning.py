import csv
import math
import numpy as np
from decision_tree import train_tree
from decision_tree import train_rforest
from decision_tree import train_svm, train_logistic
from template_feature_extraction import extract_features
from random import randint

# maxlines = 9999

####################### Getting the features ###################################

def get_features(features_filename, lines_train=[-1]):
    # Lit les features d'un fichier csv avec un header coherent.
    # Separe les features des lignes de training et les features des lignes de validation.
    # Si on veut les features de tout le fichier, ne pas specifier lines_train.

    # Get features from csv at lines specified into numpy ndarrays. Csv must have a coherent header.
    ifile = open(features_filename, 'r')
    reader = csv.reader(ifile)

    nb_features = len(next(reader))
    ifile.seek(0)

    features_train = np.ndarray((0,nb_features-1))
    features_validate = np.ndarray((0,nb_features-1))
    classes_train = np.ndarray((0,1))
    classes_validate = np.ndarray((0,1))

    all_lines = lines_train == [-1]

    for row in reader:
        if all_lines or reader.line_num in lines_train:
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

def train_validate(file_features, lines_train=[-1]):
    #features_train, features_validate, classes_train, classes_validate = get_features(features_filename, lines_train)
    # model = train_tree(features_train, classes_train)
    # model = train_rforest(features_train, classes_train, 200)
    # model = train_svm(features_train, classes_train)
    # model = train_logistic(features_train, classes_train)

    features_train, features_validate, classes_train, classes_validate = get_features(file_features, lines_train)

    model = train_rforest(features_train, classes_train, 200)

    if lines_train == [-1]: # Si on entraine sur toutes les lignes
        print "Pas de validation, la mesure de la precision se fait sur le training dataset"
        accuracy = validate(model, features_train, classes_train)
    else:
        print "Mesure de la precision sur le validation dataset"
        accuracy = validate(model, features_validate, np.ravel(classes_validate))

    return model, accuracy

########################### Predicting ########################################

def predict(model_protoss, model_terran, model_zerg, output_filename):

    # TODO: 3 modeles
    features_test_protoss, classes_test_protoss = get_features_test("features_protoss.csv")
    features_test_terran, classes_test_terran = get_features_test("features_terran.csv")
    features_test_zerg, classes_test_zerg = get_features_test("features_zerg.csv")
    predictions_protoss = model_protoss.predict(features_test_protoss)
    predictions_terran = model_terran.predict(features_test_terran)
    predictions_zerg = model_zerg.predict(features_test_zerg)

    ofile = open(output_filename, "w")
    ofile.write("row ID,battleneturl\n")

    for i in range(features_test_protoss.shape[0]):
        ofile.write(classes_test_protoss[i,0] + "," + predictions_protoss[i] + "\n")
    for i in range(features_test_terran.shape[0]):
        ofile.write(classes_test_terran[i,0] + "," + predictions_terran[i] + "\n")
    for i in range(features_test_zerg.shape[0]):
        ofile.write(classes_test_zerg[i,0] + "," + predictions_zerg[i] + "\n")

    ofile.close()
    print "Prediction done and written in " + output_filename
    return

####################### What we actually do ####################################

# TODO: Ecrire 10 lines_train dans un fichier et tester dessus
#       pour comparer avec exactement les memes ensembles pour l entrainement et le test



training_data = "train_clean.csv"

# TODO: faire des subsets de player en fonction de la faction
# TODO: get nb de rows pour feature position
players_per_faction = [[],[],[]] # Protoss, Terran, , Zerg
nb_rows_per_faction = [0,0,0]
ifile = open(training_data, 'r')
reader = csv.reader(ifile)

for row in reader:
    player = row[0].split(";")[0]
    faction = row[0].split(";")[1]
    if faction == "Protoss":
        nb_rows_per_faction[0] += 1
        if player not in players_per_faction[0]:
            players_per_faction[0].append(player)
    elif faction == "Terran":
        nb_rows_per_faction[1] += 1
        if player not in players_per_faction[1]:
            players_per_faction[1].append(player)
    else:
        nb_rows_per_faction[2] += 1
        if player not in players_per_faction[2]:
            players_per_faction[2].append(player)
nb_rows = nb_rows_per_faction[0] + nb_rows_per_faction[1] + nb_rows_per_faction[2]

accuracies_protoss = 0
accuracies_terran = 0
accuracies_zerg = 0
nb_tests = 1
for i in range(nb_tests):

    #### CROSS VALIDATION
    # Selection de 300 lignes environs pour la validation
    # lines_train = [range(nb_rows_per_faction[0]),range(nb_rows_per_faction[1]),range(nb_rows_per_faction[2])]
    # for i in range(nb_rows_per_faction[0]/10):
    #     lines_train[0].pop(randint(0,len(lines_train[0])-1))
    # for i in range(nb_rows_per_faction[1]/10):
    #     lines_train[1].pop(randint(0,len(lines_train[1])-1))
    # for i in range(nb_rows_per_faction[2]/10):
    #     lines_train[2].pop(randint(0,len(lines_train[2])-1))
    #
    # extract_features(training_data, lines_train, players_per_faction, nb_rows)
    #
    # model_protoss, accuracy_protoss = train_validate("features_protoss.csv", lines_train[0])
    # model_terran, accuracy_terran = train_validate("features_terran.csv", lines_train[1])
    # model_zerg, accuracy_zerg = train_validate("features_zerg.csv", lines_train[2])
    #
    # accuracies_protoss += accuracy_protoss
    # accuracies_terran += accuracy_terran
    # accuracies_zerg += accuracy_zerg

    ##### TEST
    extract_features(training_data, [[-1],[-1],[-1]], players_per_faction, nb_rows)

    model_protoss, accuracy_protoss = train_validate("features_protoss.csv")
    model_terran, accuracy_terran = train_validate("features_terran.csv")
    model_zerg, accuracy_zerg = train_validate("features_zerg.csv")

    # TODO refaire line train nb_rows pour similarite
    tfile = open("test.csv", 'r')
    reader = csv.reader(tfile)
    nb_rows = 0
    for row in reader:
        nb_rows += 1
    tfile.close()
    extract_features("test.csv", [[-1],[-1],[-1]], players_per_faction, nb_rows)
    predict(model_protoss, model_terran, model_zerg, "res.csv")

accuracies_protoss /= nb_tests
accuracies_terran /= nb_tests
accuracies_zerg /= nb_tests
print "Accuracy protoss : " + str(accuracies_protoss)
print "Accuracy terran : " + str(accuracies_terran)
print "Accuracy zerg : " + str(accuracies_zerg)

mean_accuracy = accuracies_protoss*nb_rows_per_faction[0]
mean_accuracy += accuracies_terran*nb_rows_per_faction[1]
mean_accuracy += accuracies_zerg*nb_rows_per_faction[2]
mean_accuracy /= (nb_rows_per_faction[0]+nb_rows_per_faction[1]+nb_rows_per_faction[2])
print "Mean accuracy : " + str(mean_accuracy)

################################################################################
