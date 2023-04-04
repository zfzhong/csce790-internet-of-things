#!/usr/bin/env python3
#
# Zifei (David) Zhong
# zhongz@email.sc.edu
# University of South Carolina
# March 31, 2023
#
# Code to test implementation of the Viterbi Algorithm.
#

from color_grid import NUM_COLS
from hmm_viterbi import ViterbiAlgorithm


def load_matrix(filename):
    """
    This function is used to load both transition matrix and emission matrix. Notice that
    the matrices should have all numbers separated by ',' in each row.

    For emission matrix (em), the observation sysmbols should also be numbered 1 to N.

    For example, in an application we have 4 observed colors: 'r', 'g', 'b', and 'y', we
    then can have a mapping dictionary: {'r':0, 'g':1, 'b':2, 'y':3}, whih maps an observed
    symbol to the state number '0'~'3'. 
    """
    m = []
    with open(filename, 'r') as f:
        line = f.readline()

        while line:
            line = line.strip()
            tokens = line.split(',')

            row = [float(e.strip()) for e in tokens]
            m.append(row)

            line = f.readline()

    return m


def dump_matrix(m, format_str="%7.4f"):
    for i in range(0, len(m)):
        row = m[i]
        s = ', '.join([format_str % e for e in row])
        print(s)


def load_observation_sequence(filename):
    seq = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            tokens = line.split()
            seq.append(tokens[-1].strip())

            line = f.readline()

    return seq


def dump_trace(trace, seq):
    for i in range(0, len(trace)):
        #print(trace[i])
        x, y = id2coord(trace[i], NUM_COLS)
        print("%d:%d %s" % (x, y, seq[i]))


def load_init_prob_file(filename):
    probs = None
    with open(filename, 'r') as f:
        line = f.readline().strip()
        tokens = line.split(',')
        probs = [float(e) for e in tokens]

    return probs


import sys
from utils import id2coord

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print(
            "Usage:", sys.argv[0],
            "<num_states> <init_file> <tm_file> <em_file> <observation_file>")
        sys.exit(1)

    num_states = int(sys.argv[1])
    init_file = sys.argv[2]
    tm_file = sys.argv[3]
    em_file = sys.argv[4]
    obs_file = sys.argv[5]

    init_prob = load_init_prob_file(init_file)

    tm = load_matrix(tm_file)
    # dump_matrix(tm)

    em = load_matrix(em_file)
    # dump_matrix(em)

    seq = load_observation_sequence(obs_file)
    # print(len(seq))
    # print(seq)

    va = ViterbiAlgorithm(num_states, init_prob, tm, em, seq)
    va.predict()
    #va.dump_delta()
    #va.dump_prevs()

    trace = va.backtrace(len(seq) - 1)
    dump_trace(trace, seq)