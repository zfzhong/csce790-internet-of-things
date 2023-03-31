#!/bin/python3

from gen_matrix import states2key, id2coord


NUM_STATES = 16


class VertibiAlgorithm:
    def __init__(self, tm, em, seq):
        self.tm = tm
        self.em = em
        self.seq = seq
        self.delta = [[1]*NUM_STATES] 
        self.prevs = []
        self.trace = []


    def dump_delta(self):
        for i in range(0, len(self.delta)):
            s  = ','.join(['%.6f' % x for x in self.delta[i]])
            print(s)

    def dump_prevs(self):
        for i in range(0, len(self.prevs)):
            print(self.prevs[i])

    def dump_trace(self):
        for i in range(0, len(self.trace)):
            id = self.trace[i]
            x,y = id2coord(id)
            print ("%s:%s %s" % (x, y, seq[i]))


    def get_em_prob(self, i, ob):
        return self.em[i][ob]

    def get_tx_prob(self, id1, id2):
        key = states2key(id1, id2)
        if key in self.tm[id1]:
            return self.tm[id1][key]

        return 0

    def predict(self):
        seq = self.seq
        for i in range(1, len(seq)):
            ob = seq[i-1]
            
            d = []
            ids = []
            for id2 in range(0, NUM_STATES):
                m = 0
                tid = 0
                for id1 in range(0, NUM_STATES):
                    em_prob = self.get_em_prob(id1, ob)
                    tx_prob = self.get_tx_prob(id1, id2)
                    val = self.delta[i-1][id1]*em_prob*tx_prob

                    if val > m:
                        m = val
                        tid = id1
                
                ids.append(tid)
                d.append(m*100)

            self.prevs.append(ids)
            self.delta.append(d)
        
        ob = seq[-1]
        m = 0
        tid = 0
        for id in range(0, NUM_STATES):
            em_prob = self.get_em_prob(id, ob)
            val = self.delta[-1][id]*em_prob
            if val > m:
                m = val
                tid = id
        
        # backtrace
        self.trace = [tid]
        for i in range(0, len(self.prevs)):
            j = len(self.prevs) - i - 1
            self.trace.append(self.prevs[j][tid])
            tid = self.prevs[j][tid]
        
        self.trace.reverse()



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

def load_matrix(filename):
    m = []
    for i in range(0, NUM_STATES):
        m.append({})

    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            tokens = line.split(',')

            i = int(tokens[0].strip())

            for j in range(1,len(tokens)):
                tks = tokens[j].split(':')
                key = tks[0].strip()
                val = float(tks[1].strip())
                m[i][key] = float(val)

            line = f.readline()
    
    return m

def dump_matrix(m):
    for i in range(0, len(m)):
        print(i, m[i])


import sys
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage:", sys.argv[0], "<tm_file> <em_file> <observation_file>")
        sys.exit(1)

    tm_file = sys.argv[1]
    em_file = sys.argv[2]
    obs_file = sys.argv[3]

    tm = load_matrix(tm_file)
    #dump_matrix(tm) 

    em = load_matrix(em_file)
    #dump_matrix(em)

    seq = load_observation_sequence(obs_file)
    #print(len(seq))
    #print(seq)

    va = VertibiAlgorithm(tm, em, seq)
    va.predict()
    va.dump_trace()
    #va.dump_delta()
    #va.dump_prevs()

