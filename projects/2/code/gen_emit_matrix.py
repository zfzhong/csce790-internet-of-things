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

        self.emit_adjacent = [None] * self.grid.num_elements
        self.stats_adjacent = {"self": 0, "near": 0, "away": 0}

        for i in range(0, self.grid.num_elements):
            self.emit[i] = {"r": 0, "g": 0, "b": 0, "y": 0}
            self.prob[i] = {"r": 0, "g": 0, "b": 0, "y": 0}
            self.emit_adjacent[i] = {"near": 0, "away": 0, "self": 0}

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

    def calc_emit_prob(self):
        total = self.stats_adjacent['self'] + \
            self.stats_adjacent['near'] + self.stats_adjacent['away']
        for i in range(0, self.grid.num_elements):
            node = self.grid.get_node(i)
            if node.is_empty():
                continue

            for c in COLORS:
                if c == node.color:
                    self.prob[i][c] = self.stats_adjacent['self'] / total
                elif c in node.adjacent_colors:
                    self.prob[i][c] = self.stats_adjacent['near'] / \
                        (total*len(node.adjacent_colors))
                elif len(node.adjacent_colors) + 1 < len(COLORS):
                    self.prob[i][c] = self.stats_adjacent['away'] / \
                        (total * (len(COLORS) - 1 - len(node.adjacent_colors)))

    def dump_emit_prob(self, header=False):
        if header:
            print("----- dump emit probability: -----")

        format_str = "%7.4f"
        for i in range(0, len(self.prob)):
            node = self.grid.get_node(i)
            t = self.prob[i]
            elems = []

            for color in COLORS:
                elems.append(format_str % t[color])

            print(', '.join(elems))
        print(', '.join([format_str % 0] * len(COLORS)))

    def get_emit_stats(self):
        for i in range(0, len(self.data_rows)):
            row = self.data_rows[i]
            n, color = row
            self.emit[n][color] += 1

        for i in range(0, len(self.emit)):
            node = self.grid.get_node(i)
            total = 0
            for c in COLORS:
                total += self.emit[i][c]
                if c == node.color:
                    self.emit_adjacent[i]['self'] = self.emit[i][c]
                elif c in node.adjacent_colors:
                    self.emit_adjacent[i]["near"] += self.emit[i][c]
                else:
                    self.emit_adjacent[i]["away"] += self.emit[i][c]

            self.stats_adjacent['self'] += self.emit_adjacent[i]['self']
            self.stats_adjacent['near'] += self.emit_adjacent[i]['near']
            self.stats_adjacent['away'] += self.emit_adjacent[i]['away']

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

    def dump_emit_adjacency(self, header=False):
        if header:
            print("----- dump emit adjacency: -----")

        for i in range(0, len(self.emit_adjacent)):
            node = self.grid.get_node(i)
            t = self.emit_adjacent[i]
            print('%s -> self: %2d, near:%2d, away:%2d, total:%2d' %
                  (str(node), t['self'], t['near'], t['away'],
                   t['self'] + t['near'] + t['away']))

        print("total -> self:%d, near: %d, away: %d" %
              (self.stats_adjacent['self'], self.stats_adjacent['near'],
               self.stats_adjacent['away']))

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
    #traingrid.dump_emit_stats(True)
    #traingrid.dump_emit_adjacency(True)

    traingrid.calc_emit_prob()
    traingrid.dump_emit_prob(False)
