import csv
import math
import numpy as np

ofile = open("train_clean.csv", 'w')

with open("train.csv") as f:
   for line in f:
       if len(line.split(",")) > 20:
           ofile.write(line)

ofile.close()
