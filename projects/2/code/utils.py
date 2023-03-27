#!/bin/python3

def id2coord(i, num_cols):
    y = i // num_cols + 1
    x = i % num_cols + 1
    return x,y

def coord2id(x, y, num_cols):
    return (y-1) * num_cols + (x-1)
    