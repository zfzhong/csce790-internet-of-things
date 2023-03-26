#!/bin/python3

class DataMatrix:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_elements = 0
        self.m = [None] * (num_rows * num_cols)

    def check_bounds(self, i, description="index"):
        if i < 0 or i > self.num_rows:
            raise Exception("%s %d is out of bound" % (description, i))
        
    def get(self, i, j):
        self.check_bounds(i, "row number")
        self.check_bounds(j, "column number")
                
        idx = i * self.num_cols + j
        return self.m[idx]

    def add_element(self, val):
        self.m[self.num_elements] = val
        self.num_elements += 1

    
class ColorGrid:
    def __init__(self):
        self.num_rows = 0
        self.num_cols = 0
        self.dmat = None

    def init_from_file(self, filename):
        with open (filename, 'r') as f:
            line = f.readline()

            # read size
            tokens = line.strip().split(',')
            self.num_rows = int(tokens[0].strip())
            self.num_cols = int(tokens[1].strip())

            line = f.readline()
            while line:
                line = line.strip()
                tokens = line.split(',')

                for e in tokens:
                    self.add_element(e.strip())

                line = f.readline()

