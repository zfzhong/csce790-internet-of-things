#!/usr/bin/env python3

import sys
from utils import coord2id
from color_grid import ColorGrid, COLORS


class TrainEmitGrid:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.num_cols = grid.num_cols
        self.data_rows = []
        self.emit = [None] * self.grid.num_elements
        self.prob = [None] * self.grid.num_elements
        for i in range(0, self.grid.num_elements):
            self.emit[i] = {"r": 0, "g": 0, "b": 0, "y": 0}
            self.prob[i] = {"r": 0, "g": 0, "b": 0, "y": 0}

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

    def get_emit_stats(self):
        for i in range(0, len(self.data_rows)):
            row = self.data_rows[i]
            n, color = row
            self.emit[n][color] += 1

        for i in range(0, len(self.emit)):
            total = 0
            for c in COLORS:
                total += self.emit[i][c]

            self.emit[i]["total"] = total

    def dump_emit_stats(self, header=False):
        if header:
            print("----- dump emit stats: -----")

        s = 0
        for i in range(0, len(self.emit)):
            node = self.grid.get_node(i)
            t = self.emit[i]
            print('%s -> r:%2d, g:%2d, b:%2d, y:%2d, total: %2d' %
                  (str(node), t['r'], t['g'], t['b'], t['y'], t['total']))
            s += t['total']
        print("total: %d" % s)

    def dump_train_data(self, header=False):
        if header:
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

    traingrid = TrainEmitGrid(grid)
    traingrid.load(train_filename)
    # traingrid.dump_train_data()

    traingrid.get_emit_stats()
    traingrid.dump_emit_stats(True)
    
