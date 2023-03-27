#!/bin/python3

from color_grid import ColorGrid

class TrainGrid:
    def __init__(self, grid) -> None:
        self.grid = grid

    def train(self, trainfile):
        with open(trainfile, 'r') as f:
            line = f.readline()

            while line:
                line = f.readline()

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
    

