#!/bin/python3
#
# Zifei (David) Zhong
# zhongz@email.sc.edu
# University of South Carolina
# March 31, 2023
#
# Implementation of the Viterbi Algorithm to infer the hidden states given a sequence
# of observations, assuming that the transition matrix (tm) and emission matrix (em)
# are provided.
#
# In the implementation, we require the following:
# 1) The transition matrix (tm) always has a state "0", from which all other states
#    originate. Or put it differently, the "starting state" is always state "0".
# 2) The tansition matrix (tm) always has a state "N+1", which is the ending state.
# 3) All other states are numbered from 1 to N.
# 4) The transition probability from state i (1 <= i <= N) to state N+1 is 1.
# 5) The emission probabiliy for state "N+1" is always 0, which means the state
#    "N+1" doesn't emit anything.

import sys
from gen_matrix import states2key, id2coord
from color_grid import ob2id


class ViterbiAlgorithm:
    """
    The ViterbiAlgorithm takes in 4 arguments, and identfies/infers a squence of hidden
    states given a sequence of observations.

    * args:
      n: number of states
     tm: transition matrix
     em: emission matrix
    seq: sequence of observations
    """

    def __init__(self, n, tm, em, seq):
        self.num_states = n
        self.tm = tm
        self.em = em
        self.seq = seq
        self.delta = []
        self.prevs = []
        self.trace = []

        self.init_delta()

    def init_delta(self):
        """
        delta(0,:) is the first row of the transition matrix.
        """
        self.delta.append(self.tm[0])

    def dump_delta(self):
        for i in range(0, len(self.delta)):
            s = ','.join(['%.6f' % x for x in self.delta[i]])
            print(s)

    def dump_prevs(self):
        for i in range(0, len(self.prevs)):
            print(self.prevs[i])

    def dump_trace(self):
        for i in range(0, len(self.trace)):
            id = self.trace[i]
            x, y = id2coord(id)
            print("%s:%s %s" % (x, y, seq[i]))

    def get_em_prob(self, i, ob):
        j = ob2id(ob)
        return self.em[i][j]

    def get_tx_prob(self, i, j):
        return self.tm[i][j]

    def predict(self):
        seq = self.seq
        for k in range(0, len(seq)):
            ob = seq[k]

            ds, ps = [], []
            for id2 in range(0, self.num_states):
                m, prev = 0, 0
                for id1 in range(0, self.num_states):
                    em_prob = self.get_em_prob(id1, ob)
                    tx_prob = self.get_tx_prob(id1, id2)
                    val = self.delta[k][id1] * em_prob * tx_prob

                    if val > m:
                        m, prev = val, id1

                ps.append(prev)
                ds.append(m)

            # prevs[k]
            self.prevs.append(ps)

            # delta[k+1]
            self.delta.append(ds)

    def backtrace(self, k):
        """
        The backtracing starts from delta(k, N+1), where 0 <= k < len(seq), and state "N+1"
        is the ending state.
        """
        prev_state = self.prevs[k][-1]
        self.trace.append(prev_state)

        for i in range(k-1, -1, -1):
            prev_state = self.prevs[i][prev_state]
            self.trace.append(prev_state)

        self.trace.reverse()


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

            row = [int(e.strip()) for e in tokens]
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


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage:", sys.argv[0], "<tm_file> <em_file> <observation_file>")
        sys.exit(1)

    tm_file = sys.argv[1]
    em_file = sys.argv[2]
    obs_file = sys.argv[3]

    tm = load_matrix(tm_file)
    # dump_matrix(tm)

    em = load_matrix(em_file)
    # dump_matrix(em)

    seq = load_observation_sequence(obs_file)
    # print(len(seq))
    # print(seq)

    va = ViterbiAlgorithm(tm, em, seq)
    va.predict()
    va.dump_trace()
    # va.dump_delta()
    # va.dump_prevs()
