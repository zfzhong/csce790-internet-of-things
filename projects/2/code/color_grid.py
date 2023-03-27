#!/bin/python3

# Empty color
EMPTY_COLOR = "*"

# Neighboring direction: Left, Up, Right, Down
DIRECTIONS = ['L', 'U', 'R', 'D']

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
        for i in range(self.num_rows,0,-1):
            idx = (i-1) * self.num_cols
            row = self.m[idx:idx+self.num_cols]
            print(' '.join([str(e) for e in row]))

    def dump_elements(self):
        for i in range(0, self.num_elements):
            print("%2d: %s" % (i, self.m[i]))


class GridNode:
    def __init__(self, grid, id, color=EMPTY_COLOR):
        self.grid = grid
        self.id = id
        self.color = color

        self.left_node = None
        self.up_node = None
        self.right_node = None
        self.down_node = None

    def is_empty(self):
        return self.color == EMPTY_COLOR

    def neighbor(self, direction):
        direction = direction.upper()
        if not direction in DIRECTIONS:
            raise Exception("direction % wrong" % direction)

        if direction == 'L':
            return self.left_node
        if direction == 'U':
            return self.up_node
        if direction == 'R':
            return self.right_node
        if direction == 'D':
            return self.down_node    
    
    def dump_neighbors(self):
        dl = []
        for direction in DIRECTIONS:
            nb = self.neighbor(direction)
            if nb:
                dl.append(str(nb))
            else:
                dl.append('(--,--)')
        
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

    def init_from_file(self, filename):
        with open (filename, 'r') as f:
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
                        lnode = self.mat.get_element(i-1)
                        lnode.right_node = n
                        n.left_node = lnode
                    
                    # build top-down neighbors
                    if i // self.num_cols > 0:
                        dnode = self.mat.get_element(i-self.num_cols)
                        dnode.up_node = n
                        n.down_node = dnode                    

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

        

