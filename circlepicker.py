#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''..
   circlepicker.py
.. moduleauthor:: Nick Timkovich <ntimkovich@u.northwestern.edu>

Generates circular masks from an image by having the user click three points 
on the edge.  Saves the circle center and radius in a file for later use.
'''
import sys
import os
import csv
import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def perp(v):
    # adapted from http://stackoverflow.com/a/3252222/194586
    p = np.empty_like(v)
    p[0] = -v[1]
    p[1] = v[0]
    return p

# def seg_intersect(a1,a2, b1,b2):
#     # adapted from http://stackoverflow.com/a/3252222/194586
#     da = a2 - a1
#     db = b2 - b1
#     dp = a1 - b1
#     dap = perp(da)
#     denom = np.dot(dap, db)
#     num = np.dot(dap, dp)
#     if denom == 0:
#         raise ValueError('lines are parallel.')
#     return (num / denom) * db + b1

def circle_3pt(a, b, c):
    '''
    1. Make some arbitrary vectors along the perpendicular bisectors between 
        two pairs of points.
    2. Find where they intersect (the center).
    3. Find the distance between center and any one of the points (the 
        radius).
    '''
    a = np.array(a) 
    b = np.array(b)
    c = np.array(c)

    # find perpendicular bisectors
    ab = b - a
    c_ab = (a + b) / 2
    pb_ab = perp(ab)
    bc = c - b
    c_bc = (b + c) / 2
    pb_bc = perp(bc)

    ab2 = c_ab + pb_ab
    bc2 = c_bc + pb_bc

    # find where some example vectors intersect
    #center = seg_intersect(c_ab, c_ab + pb_ab, c_bc, c_bc + pb_bc)

    A1 = ab2[1] - c_ab[1]
    B1 = c_ab[0] - ab2[0]
    C1 = A1 * c_ab[0] + B1 * c_ab[1]
    A2 = bc2[1] - c_bc[1]
    B2 = c_bc[0] - bc2[0]
    C2 = A2 * c_bc[0] + B2 * c_bc[1]
    center = np.linalg.inv(np.matrix([[A1, B1],[A2, B2]])) * np.matrix([[C1], [C2]])
    center = np.array(center).flatten()

    radius = np.linalg.norm(a - center)

    return center, radius

class Masker(object):
    def __init__(self, outfile, axes):
        self.mask_number = 1
        self.edges = []
        self.outfile = outfile
        self.axes = axes

    def onclick(self, event):
        if event.button != 2:
            # only accept middle mouse click
            return
        if not (event.xdata or event.ydata):
            # ignore clicking outside graph
            return
        self.edges.append((event.xdata, event.ydata))
        if len(self.edges) == 3:
            # maths
            center, radius = circle_3pt(*self.edges)
            row = [self.mask_number] + list(center) + [radius]
            print row

            # dump
            with open(self.outfile, 'ab') as f:
                fcsv = csv.writer(f)
                fcsv.writerow(row)

            # draw the thing
            self.axes.add_patch(patches.Circle(center, radius, alpha=0.3))
            self.axes.text(center[0], center[1], str(self.mask_number), 
                    horizontalalignment='center',
                    verticalalignment='center')
            event.canvas.draw()

            # reinitialize
            self.edges = []
            self.mask_number += 1

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Show an image and capture '
        'clicks specifying circular regions (3-point method)')
    parser.add_argument('image', type=str, help='Input image')

    args = parser.parse_args(argv)

    img = mpimg.imread(args.image)

    fig, ax = plt.subplots()
    ax.imshow(img)

    # a = (173, 169)
    # b = (83, 340)
    # c = (260, 350)
    # center, radius = circle_3pt(a, b, c)
    # ax.add_patch(patches.Circle(center, radius, alpha=0.3))

    masker = Masker(args.image + '.csv', ax)
    cid = fig.canvas.mpl_connect('button_press_event', masker.onclick)

    plt.show()

if __name__ == '__main__':
    sys.exit(main())