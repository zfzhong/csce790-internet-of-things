#! /bin/python3

import sys

def load_file(filename):
    data = []

    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            tokens = line.split()
            data.append((tokens[0].strip(), tokens[1].strip()))

            line = f.readline()

    return data

def compare_result(d1, d2):
    if len(d1) != len(d2):
        print("data size different, abort")
        return

    correct = 0
    total = len(d1)
    for i in range(0, total):
        if d1[i][0] == d2[i][0] and d1[i][1] == d2[i][1]:
            correct += 1

    print("correct predict: %d" % correct)
    print("correct percentage: %.2f%%" % (correct *100 / total) )
        


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "<test_file> <predict_file>")
        sys.exit(1)

    test_file = sys.argv[1]
    predict_file = sys.argv[2]

    tdata = load_file(test_file)
    pdata = load_file(predict_file)

    compare_result(tdata, pdata)


