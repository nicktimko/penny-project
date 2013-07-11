#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''..
   pennyreconstructor.py
.. moduleauthor:: Nick Timkovich <ntimkovich@u.northwestern.edu>

Uses the histogram data to make penny-colored-pixels.
'''
from __future__ import division
import sys
import argparse
import csv
import itertools

import numpy as np
import matplotlib.pyplot as plt

# from http://docs.python.org/2/library/itertools.html#recipes
def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

# from http://stackoverflow.com/a/312464/194586
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Show an image and capture '
        'clicks specifying circular regions (3-point method)')
    parser.add_argument('image', type=str, help='Input image')

    args = parser.parse_args(argv)

    histogram_file_in = args.image + '_hist.csv'

    colors = []
    with open(histogram_file_in, 'rb') as fi:
        histcsv = csv.reader(fi)
        for hists in grouper(3, histcsv, None):
            assert hists[0][0] == hists[1][0] == hists[2][0]
            penny_num = hists[0][0]
            rgb = [0, 0, 0]
            for i, hist in enumerate(hists):
                hist = np.array(hist[2:], np.float)
                rgb[i] = int(round(sum(hist * np.arange(256))/sum(hist)))
            print penny_num, rgb
            colors.append(rgb)

    pixels = np.array([row + [[0] * 3] * (10 - len(row)) for row in chunks(colors, 10)])
    plt.imshow(pixels / 255, interpolation='nearest')
    plt.title('Anti-CSI zoom-enhancing')

    plt.show()

if __name__ == '__main__':
    sys.exit(main())