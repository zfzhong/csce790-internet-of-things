#!/bin/python3

from utils import coord2id
from color_grid import ColorGrid

class TrainGrid:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.data_rows = []

    def train(self, trainfile):
        with open(trainfile, 'r') as f:
            line = f.readline()

            while line:
                line = line.strip()
                
                coord, color = line.split()
                x,y = coord.split(":")
                i = coord2id(int(x), int(y), self.grid.num_cols)
                self.data_rows.append((i,color))

                line = f.readline()

    def dump_train_data(self):
        print("----- dump train data: ------")
        for e in self.data_rows:
            print(e)

import sys
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
    

