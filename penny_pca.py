#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''..
   penny_pca.py
.. moduleauthor:: Nick Timkovich <ntimkovich@u.northwestern.edu>

Does principal component analysis on the penny colors.  Ordinarly the 
principal components are some totally abstract thing, but because we're 
working with colors, the axes are also colors, easily(?) visualizable.
'''

import sys
import argparse

import numpy as np
import matplotlib.pyplot as plt

import penny_reconstructor as penny_r
import pca

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Does principal component '
        'analysis on the penny colors')
    parser.add_argument('image', type=str, help='Image filename used to '
        'generate histograms (not actually read)')
    args = parser.parse_args(argv)

    histogram_file_in = args.image + '_hist.csv'
    colors = np.array(penny_r.get_colors(histogram_file_in))

    p = pca.PCA(colors, fraction=1)

    import pdb;pdb.set_trace()
    #print p
    fig, ax = plt.subplots()
    pc = p.pc()
    ax.plot(pc.T[0], pc.T[1], 'o')
    plt.show()

if __name__ == '__main__':
    sys.exit(main())
