train = open("test.csv", 'r')
first_100 = open("first_100_test.csv", 'w')

print train.readline()

for i in range(100):
    first_100.write(train.readline())
