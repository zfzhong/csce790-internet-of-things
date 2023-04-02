#!/bin/python3

# Empty color
EMPTY_COLOR = "*"

# Neighboring direction: Left, Up, Right, Down
DIRECTIONS = ['L', 'U', 'R', 'D']
COLORS = ['r', 'g', 'b', 'y']

OB2ID = {"r": 0, "g": 1, "b": 2, "y": 3}
NUM_COLS = 4


def ob2id(ob):
    return OB2ID[ob]


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
        return self.get_element(idx)

    def get_element(self, i):
        if i >= self.num_elements:
            raise Exception("element id %d out of bound" % i)

        return self.m[i]

    def add_element(self, val):
        self.m[self.num_elements] = val
        self.num_elements += 1

    def dump_matrix(self):
        for i in range(self.num_rows, 0, -1):
            idx = (i - 1) * self.num_cols
            row = self.m[idx:idx + self.num_cols]
            print(' '.join([str(e) for e in row]))

    def dump_elements(self):
        for i in range(0, self.num_elements):
            print("%2d: %s" % (i, self.m[i]))


class GridNode:

    def __init__(self, grid, id, color=EMPTY_COLOR):
        self.grid = grid
        self.id = id
        self.color = color
        self.num_neighbors = 0
        self.neighbors = {"L": None, "U": None, "R": None, "D": None}
        self.adjacent_colors = []

    def is_empty(self):
        return self.color == EMPTY_COLOR

    def set_neighbor(self, node, direction):
        self.neighbors[direction] = node
        if not node.is_empty():
            self.num_neighbors += 1
            if not node.color in self.adjacent_colors:
                self.adjacent_colors.append(node.color)

    def neighbor(self, direction):
        direction = direction.upper()
        if not direction in DIRECTIONS:
            raise Exception("direction % wrong" % direction)

        return self.neighbors[direction]

    def dump_neighbors(self):
        dl = []
        for direction in DIRECTIONS:
            nb = self.neighbor(direction)
            if nb:
                dl.append(str(nb))
            else:
                dl.append('---,---')

        print('%s: %s' % (self, ', '.join(dl)))

    def __str__(self) -> str:
        return "(%2d, %s)" % (self.id, self.color)

    def __expr__(self):
        return self.__str__()


class ColorGrid:

    def __init__(self):
        self.num_rows = 0
        self.num_cols = 0
        self.mat = None

    @property
    def num_elements(self):
        if not self.mat:
            return 0

        return self.mat.num_elements

    def get_node(self, i):
        if self.mat:
            return self.mat.get_element(i)

        return None

    def init_from_file(self, filename):
        with open(filename, 'r') as f:
            line = f.readline()

            # read size
            tokens = line.strip().split(',')
            self.num_rows = int(tokens[0].strip())
            self.num_cols = int(tokens[1].strip())
            self.mat = DataMatrix(self.num_rows, self.num_cols)

            line = f.readline()
            i = 0
            while line:
                line = line.strip()
                tokens = line.split()

                for e in tokens:
                    n = GridNode(self, i, e.strip())

                    # build left-right neighbors
                    if i % self.num_cols > 0:
                        lnode = self.mat.get_element(i - 1)
                        lnode.set_neighbor(n, 'R')
                        n.set_neighbor(lnode, 'L')

                    # build top-down neighbors
                    if i // self.num_cols > 0:
                        dnode = self.mat.get_element(i - self.num_cols)
                        dnode.set_neighbor(n, 'U')
                        n.set_neighbor(dnode, 'D')

                    self.mat.add_element(n)
                    i += 1

                line = f.readline()

    def dump_grid(self):
        print("\n------- dump grid: --------")
        self.mat.dump_matrix()

    def dump_elements(self):
        print("\n------- dump elements: --------")
        self.mat.dump_elements()

    def dump_neighbors(self):
        print("\n------ dump neighbors: -------")
        for i in range(0, self.mat.num_elements):
            node = self.mat.get_element(i)
            node.dump_neighbors()
