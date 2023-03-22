#!/bin/python3

import sys
NUM_STATES = 16
COLORS = ['r', 'g', 'b', 'y']
GRID = [None, "r", "g", None, "g", None, "b",
        "r", "y", "g", "r", "y", "b", "y", None, "b"]
DIRECTIONS = [(0,0), (0, 1), (0, -1), (1, 0), (-1, 0)]


def get_transition_frequency(trans):
    """
    Get the number of occurance for each state that is an origin of a transition.
    For example, given "4->8: 6" and "4->4: 11", we will have "4:17", which means
    that there are 17 state transitions originating from state 4.
    """
    freq = [0]*NUM_STATES

    for key in trans:
        id1, id2 = key2states(key)
        if id1 >= 0:
            freq[id1] += trans[key]

    return freq

def get_transition_freedom(grid):
    """
    Get the degree of freedom for each square in the grid.
    """
    freedom = [0] * NUM_STATES
    
    for i in range(0, NUM_STATES):
        x,y = id2coord(i)

        for d in DIRECTIONS:
            x0,y0 = d

            x1 = x+x0
            y1 = y+y0

            if grid[i] and x1 >= 1 and x1 <= 4 and y1 >= 1 and y1 <= 4:
                id = coord2id(x1,y1)
                if grid[id]:
                    freedom[i] += 1

    return freedom

def gen_transition_matrix(trans, factor=0.5):
    """
    Generate the state transition matrix, which is encoded as an array of directionaries.
    """
    tm = []
    for i in range(0, NUM_STATES):
        tm.append({})

    freq = get_transition_frequency(trans)

    for key in trans:
        id1, id2 = key2states(key)
        tm[id1][key] = trans[key] / freq[id1]

    freedom = get_transition_freedom(GRID)

    for i in range(0, NUM_STATES):
        if len(tm[i].keys()) < freedom[i]:
            x,y = id2coord(i)
            
            # It's getting tricky here:
            # We assume all other possibilities sumed up together should be equal to
            # a factor of the minimum probability of exisiting choices.

            # 1) find the minimum
            m1 = 1
            for k in tm[i]:
                if tm[i][k] < m1:
                    m1 = tm[i][k]

            # 2) normalize all probabilities
            tp = (m1 *  factor)

            for k in tm[i]:
                tm[i][k] = tm[i][k] / (1+tp)
            
            if len(tm[i].keys()) == 0:
                tp = m1
            else:
                tp = tp / (1+tp)
            
            # 3) split the probability across all possible but no-exisiting choices
            p =  tp / (freedom[i] - len(tm[i].keys()))

            # 4) assign probability  to all possible but non-exisiting choices
            for d in DIRECTIONS:
                x0,y0 = d
                x1 = x + x0
                y1 = y + y0

                if GRID[i] and x1 >= 1 and x1 <= 4 and y1 >= 0 and y1 <= 4:
                    id2 = coord2id(x1,y1)
                    key = states2key(i, id2)
                    if GRID[id2] and not key in tm[i]:
                        tm[i][key] = p
                
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
        x, y = get_coord(key)
        id = coord2id(x, y)

        for k in stats[key]:
            freq[id] += stats[key][k]

    return freq


def gen_emission_matrix(stats, factor=0.5):
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
        x, y = get_coord(key)
        i = coord2id(x, y)
        for color in stats[key]:
            em[i][color] = stats[key][color] / freq[i]

    for i in range(0, NUM_STATES):
        if not em[i].keys() and GRID[i]:
            actual_color = GRID[i]
            em[i][actual_color] = 1

    for i in range(0, NUM_STATES):
        if len(em[i].keys()) < 4 and GRID[i]:
            m1 = 1
            for k in em[i]:
                if em[i][k] < m1:
                    m1 = em[i][k]
            
            tp = m1 * factor
            for k in em[i]:
                em[i][k] = em[i][k] / (1+tp)
            
            tp = tp/(1+tp)
            p = tp / (4-len(em[i].keys()))
            for colors in COLORS:
                if not colors in em[i]:
                    em[i][colors] = p

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
    y = (idx % 4) + 1

    return x,y

def gen_transition_key(state1, state2):
    """
    Generate transition key based on two state strings.
    For example, state1="1:2", state="1:3" should generate key "1->2".
    """
    x1, y1 = get_coord(state1)
    x2, y2 = get_coord(state2)

    id1 = coord2id(x1, y1)
    id2 = coord2id(x2, y2)

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

    return id1, id2


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


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], "<filename> <E/T> <factor=0.5>")
        sys.exit(1)

    filename = sys.argv[1]
    action = sys.argv[2]

    factor = 0.5 # default 
    
    if len(sys.argv) >= 4:
        factor = float(sys.argv[3])


    if action.upper() == 'E':
        # generate emission matrix
        emission = get_emission_stats(filename)
        #freq = get_states_frequency(emission)    
        #print(freq)

        em = gen_emission_matrix(emission, factor=factor)
        for i in range(0, NUM_STATES):
            items = []
            for color in COLORS:
                items.append("%s:%s" % (color, get_prob_emission_matrix(i, color, em)))
            s = ','.join(items)
            print('%d, %s' % (i, s))

    if action.upper() == 'T':
        trans = get_transition_stats(filename)
        tm = gen_transition_matrix(trans, factor=factor)
        for i in range(0, NUM_STATES):
            items = []
            for d in DIRECTIONS:
                x,y = id2coord(i)
                x0,y0 = d

                x1 = x+x0
                y1 = y + y0
                
                if x1 >= 1 and x1 <= 4 and y1 >= 1 and y1 <= 4:
                    id2 = coord2id(x1,y1)
                    key = states2key(i, id2)

                    items.append("%s:%s" % (key, get_prob_transition_matrix(i, id2, tm)))

            s = ','.join(items)
            print('%d, %s' % (i, s))
    
