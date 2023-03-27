#!/bin/python3

import sys
from utils import coord2id
from color_grid import ColorGrid


class TrainGrid:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.num_cols = grid.num_cols
        self.data_rows = []
        self.trans = [None]*self.grid.num_elements

    def train(self, trainfile):
        with open(trainfile, 'r') as f:
            line = f.readline()

            while line:
                line = line.strip()

                coord, color = line.split()
                x, y = coord.split(":")
                i = coord2id(int(x), int(y), self.grid.num_cols)
                self.data_rows.append((i, color))

                line = f.readline()

    def calc_trans(self):
        for i in range(1, len(self.data_rows)):
            move_from = self.data_rows[i-1][0]
            move_to = self.data_rows[i][0]

            node = self.trans[move_from]
            if not node:
                node = {"O": 0, "L": 0, "U": 0, "R": 0, "D": 0}
                self.trans[move_from] = node

            key = None
            if move_to == move_from:
                key = 'O'  # the transition is to stop at the original location
            elif move_to == move_from-1:
                # left
                key = 'L'
            elif move_to == move_from + self.num_cols:
                # up
                key = 'U'
            elif move_to == move_from+1:
                # right
                key = 'R'
            elif move_to == move_from - self.num_cols:
                # down
                key = 'D'

            node[key] += 1

    def dump_trans(self):
        print("----- dump trans: -----")
        for i in range(0, len(self.trans)):
            t = self.trans[i]
            if t:
                print('%2d -> O:%2d, L:%2d, U:%2d, R:%2d, D:%2d' %
                      (i, t['O'], t['L'], t['U'], t['R'], t['D']))
            else:
                print('%2d -> ---' % i)

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
    traingrid.train(train_filename)
    traingrid.dump_train_data()
    traingrid.calc_trans()
    traingrid.dump_trans()
