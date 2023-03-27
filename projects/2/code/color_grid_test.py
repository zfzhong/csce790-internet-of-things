#!/bin/python3

from color_grid import ColorGrid
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ", sys.argv[0], "<filename>")
        sys.exit(1)

    filename = sys.argv[1]

    cg = ColorGrid()
    cg.init_from_file(filename)

    cg.dump_grid()
    cg.dump_elements()
    cg.dump_neighbors()


