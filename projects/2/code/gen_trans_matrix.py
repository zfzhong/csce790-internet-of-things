#!/usr/bin/env python3

import sys
from utils import coord2id
from color_grid import ColorGrid, DIRECTIONS


class TrainGrid:

    def __init__(self, grid) -> None:
        self.grid = grid
        self.num_cols = grid.num_cols
        self.data_rows = []
        self.trans = [None] * self.grid.num_elements
        self.prob = [None] * self.grid.num_elements
        for i in range(0, len(self.trans)):
            self.trans[i] = {"O": 0, "L": 0, "U": 0, "R": 0, "D": 0}
            self.prob[i] = {"O": 0, "L": 0.25, "U": 0.25, "R": 0.25, "D": 0.25}

    def load(self, trainfile):
        with open(trainfile, 'r') as f:
            line = f.readline()

            while line:
                line = line.strip()

                coord, color = line.split()
                x, y = coord.split(":")
                i = coord2id(int(x), int(y), self.grid.num_cols)
                self.data_rows.append((i, color))

                line = f.readline()

    def calc_prob(self):
        for i in range(0, len(self.prob)):
            node = self.grid.get_node(i)
            if node.is_empty() or self.trans[i]['SUM'] <= 0:
                continue

            for d in DIRECTIONS:
                self.prob[i][d] = self.trans[i][d] / self.trans[i]['SUM']

        for i in range(0, len(self.prob)):
            node = self.grid.get_node(i)
            if node.is_empty():
                continue

            for d in DIRECTIONS:
                nb = node.neighbors[d]
                if nb and not nb.is_empty():
                    continue

                self.prob[i]['O'] += self.prob[i][d]
                self.prob[i][d] = 0

    def dump_prob(self, header=False):
        if header:
            print("----- dump probability -----")
        for i in range(0, len(self.prob)):
            node = self.grid.get_node(i)
            p = self.prob[i]

            print('%s -> O:%7.4f, L:%7.4f, U:%7.4f, R:%7.4f, D:%7.4f' %
                  (str(node), p['O'], p['L'], p['U'], p['R'], p['D']))

    def calc_trans(self):
        for i in range(1, len(self.data_rows)):
            move_from = self.data_rows[i - 1][0]
            move_to = self.data_rows[i][0]

            node = self.trans[move_from]
            key = None

            if move_to == move_from:
                key = 'O'  # the transition is to stop at the original location
            elif move_to == move_from - 1:
                # left
                key = 'L'
            elif move_to == move_from + self.num_cols:
                # up
                key = 'U'
            elif move_to == move_from + 1:
                # right
                key = 'R'
            elif move_to == move_from - self.num_cols:
                # down
                key = 'D'

            node[key] += 1

        # sum up all directions to get total
        for i in range(0, len(self.trans)):
            t = self.trans[i]
            total = t['O'] + t['L'] + t['U'] + t['R'] + t['D']
            t['SUM'] = total

        # Redistribute direction 'O' to other 'empty' directions, equally.
        for i in range(0, self.grid.num_elements):
            node = self.grid.get_node(i)
            if node.is_empty():
                continue

            for d in DIRECTIONS:
                nb = node.neighbors[d]
                if nb and not nb.is_empty():
                    continue

                tran = self.trans[i]
                tran[d] = tran['O'] / (len(DIRECTIONS) - node.num_neighbors)

    def dump_trans(self):
        print("----- dump trans: -----")
        total = 0
        for i in range(0, len(self.trans)):
            node = self.grid.get_node(i)
            t = self.trans[i]
            if t:
                print(
                    '%s -> O:%2d, L:%5.2f, U:%5.2f, R:%5.2f, D:%5.2f, total: %2d'
                    % (str(node), t['O'], t['L'], t['U'], t['R'], t['D'],
                       t['SUM']))
            else:
                print('%s -> ---' % str(node))

            total += t['SUM']
        print("Total: %d" % total)

    def dump_prob_full(self):
        format_str = "%7.4f"
        for i in range(0, self.grid.num_elements):
            node = self.grid.get_node(i)
            elems = []

            for j in range(0, self.grid.num_elements):
                if j == i:
                    elems.append(format_str % self.prob[i]['O'])
                    continue

                is_neighbor = False
                for d in DIRECTIONS:
                    nb = node.neighbors[d]
                    if nb and nb.id == j and not nb.is_empty():
                        elems.append(format_str % self.prob[i][d])
                        is_neighbor = True

                if not is_neighbor:
                    elems.append(format_str % 0)

            # i->N, probability 1.
            elems.append(format_str % 1)

            print(', '.join(elems))

        # N->i, probability 0.
        print(', '.join([format_str % 0] * (self.grid.num_elements + 1)))

    def dump_train_data(self):
        print("----- dump train data: ------")
        for e in self.data_rows:
            print(e)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], "<grid.dat> <train.dat>")
        sys.exit(1)

    grid_filename = sys.argv[1]
    train_filename = sys.argv[2]

    grid = ColorGrid()
    grid.init_from_file(grid_filename)

    traingrid = TrainGrid(grid)
    traingrid.load(train_filename)
    #traingrid.dump_train_data()
    traingrid.calc_trans()
    #traingrid.dump_trans()

    traingrid.calc_prob()
    #traingrid.dump_prob()
    traingrid.dump_prob_full()
