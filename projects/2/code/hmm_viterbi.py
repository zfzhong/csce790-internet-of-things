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
# 1) The transition matrix (tm) always has an ending state N, while all other states
#    are numbered from 0 to (N-1).
# 2) The transition probability from state i (0 <= i <= N-1) to state N is 1. The
#    transition probability from state N to state N is 0.
# 3) The emission probabiliy for state N is always 0, which means the ending state
#    never emits anything.

import sys
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

    def __init__(self, n, init_probs, tm, em, seq):
        self.num_states = n
        self.tm = tm
        self.em = em
        self.seq = seq
        self.delta = [init_probs]
        self.prevs = None

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
            print("%s:%s" % (id, seq[i]))

    def get_em_prob(self, i, ob):
        j = ob2id(ob)
        return self.em[i][j]

    def get_tx_prob(self, i, j):
        return self.tm[i][j]

    def predict(self):
        self.prevs = []
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
        trace = []

        prev_state = self.prevs[k][-1]
        trace.append(prev_state)

        for i in range(k - 1, -1, -1):
            prev_state = self.prevs[i][prev_state]
            trace.append(prev_state)

        trace.reverse()
        return trace
