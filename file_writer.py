train = open("train.csv", 'r')
first_100 = open("first_100_train.csv", 'w')

print train.readline()

for i in range(100):
    first_100.write(train.readline())
