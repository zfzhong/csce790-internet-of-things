#!/bin/python3 

NUM_STATES = 16
COLORS = ['r', 'g', 'b', 'y']
GRID = [None, "r", "g", None, "g", None, "b", "r", "y", "g", "r", "y", "b", "y", None, "b"]
DIRECTIONS = [(0,0), (0,1), (0, -1), (1,0), (-1,0)]

def get_transition_frequency(trans):
    """
    Get the number of occurance for each state that is an origin of a transition.
    For example, given "4->8: 6" and "4->4: 11", we will have "4:17", which means
    that there are 17 state transitions originating from state 4.
    """
    freq = [0]*NUM_STATES

    for key in trans:
        id1,id2 = key2states(key)
        if id1 >= 0:
            freq[id1] += trans[key]

    return freq

def gen_transition_matrix(trans):
    """
    Generate the state transition matrix, which is encoded as an array of directionaries.
    """
    tm = []
    for i in range(0,NUM_STATES):
        tm.append({})

    for key in trans:
        id1,id2 = key2states(key)
        
        tm[id1][key] = trans[key]

    return tm

def get_prob_transition_matrix(id1, id2, tm):
    """
    get the probability of transition from state 'id1' to state 'id2'.
    """
    key = states2key(id1, id2)
    if key in tm[id1]:
        return tm[id1][key]

    return 0

def get_states_frequency(stats):
    """
    Get the number of occurane for each state.
    """
    freq = [0]*NUM_STATES
    for key in stats:
        x,y = get_coord(key)
        id = coord2id(x,y)

        for k in stats[key]:
            freq[id] += stats[key][k]
            
    return freq

def gen_emission_matrix(stats):
    """
    Generate the emission matrix, which is encoded as an array of dictionary.
    """

    # initialization based on the grid map given
    em = []
    for i in range(0, NUM_STATES):
        em.append({})

    # get occurance of each state from train data
    freq = get_states_frequency(stats)

    for key in stats:
        x,y = get_coord(key)
        i = coord2id(x, y)
        for color in stats[key]:
            em[i][color] = stats[key][color] / freq[i]

    for i in range(0, NUM_STATES):
        if not em[i].keys() and GRID[i]:
            actual_color = GRID[i]
            em[i][actual_color] = 1

    return em

def get_prob_emission_matrix(i, color, em):
    """
    get the probability of emitting 'color' at state 'i'.
    """
    if color in em[i]:
        return em[i][color]

    return 0
    

def get_coord(s):
    """
    Convert a string to coordinate.
    For example, '3:2' will be converted to (3, 2).
    """
    tokens = s.split(":")
    x = int(tokens[0])
    y = int(tokens[1])
    return x, y
    
def coord2id(x, y):
    """"
    Convert a coordinate to id.
    For example: coordiate (3,2) will be convereted to 9.
    """
    return (x-1) * 4 + (y-1)

def id2coord(idx):
    """
    Convert an id to coordiate.
    For example, id 9 will be converted to (3,2).
    """
    x = (idx // 4) + 1
    y = (id % 4) + 1

def gen_transition_key(state1, state2):
    """
    Generate transition key based on two state strings.
    For example, state1="1:2", state="1:3" should generate key "1->2".
    """
    x1,y1 = get_coord(state1)
    x2,y2 = get_coord(state2)
    
    id1 = coord2id(x1,y1)
    id2 = coord2id(x2,y2)

    return states2key(id1, id2)

def states2key(id1, id2):
    """
    Generate state transition based given two state ids.
    """
    return "%d->%d" % (id1, id2)

def key2states(key):
    """
    Generate state ids based on the transition key.
    For example, key "1->2" should be decoded as "1, 2".
    """
    states = key.split('->')
    id1 = int(states[0])
    id2 = int(states[1])

    return id1,id2

def get_transition_stats(filename):
    """
    Get transition statistics from the input file (train.dat)
    """
    transition = {}
    with open(filename, 'r') as f:
        line = f.readline()
        
        if not line:
            return transition

        line = line.strip()
        tokens = line.split()
        prev_state = tokens[0]

        line = f.readline()

        while line:
            line = line.strip()
            tokens = line.split()

            curr_state = tokens[0]

            trans_key = gen_transition_key(prev_state, curr_state)
            if not trans_key in transition:
                transition[trans_key] = 1
            else:
                transition[trans_key] += 1

            line = f.readline()
            prev_state = curr_state

    return transition

def get_emission_stats(filename):
    """
    Get emission statistics from the input file (train.dat).
    """
    emission = {}

    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            tokens = line.split()

            key = tokens[0]
            color = tokens[1]
            
            if not key in emission:
                emission[key] = {color: 1}
            else:
                if color not in emission[key]:
                    emission[key][color] = 1
                else:
                    emission[key][color] += 1


            line = f.readline()

    return emission


import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], "<filename>")
        sys.exit(1)

    filename = sys.argv[1]
    emission = get_emission_stats(filename)
    freq = get_states_frequency(emission)
    print(freq)

    total = 0
    for key in emission:
        x,y = get_coord(key)
        id = coord2id(x, y)
        print(key, freq[id], emission[key])
        for k in emission[key]:
            total += emission[key][k]

    print("total:", total)

    em = gen_emission_matrix(emission)
    for i in range(0,len(em)):
        print(i, em[i])

    print("--- transitions: ---")
    trans = get_transition_stats(filename)
    i = 0
    for key in trans:
        print(i, ":", key, trans[key]) 
        i += 1   

    fr = get_transition_frequency(trans)
    print(fr)
    print("+++ trans matrix: ----")
    tm = gen_transition_matrix(trans)
    for i in range(0, len(tm)):
        print(i, ":", fr[i], tm[i])

    