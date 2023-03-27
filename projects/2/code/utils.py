#!/bin/python3

def id2coord(i, num_cols):
    y = i // num_cols + 1
    x = i % num_cols + 1
    return x,y

