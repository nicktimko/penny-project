#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''..
   penny_pca.py
.. moduleauthor:: Nick Timkovich <ntimkovich@u.northwestern.edu>

Does principal component analysis on the penny colors.  Ordinarly the 
principal components are some totally abstract thing, but because we're 
working with colors, the axes are also colors, easily(?) visualizable.
'''
from __future__ import division
import sys
import argparse

import numpy as np
import scipy.stats as sps
import scipy.optimize as spo
import matplotlib.pyplot as plt

import penny_reconstructor as penny_r
import pca
import skew

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Does principal component '
        'analysis on the penny colors')
    parser.add_argument('image', type=str, help='Image filename used to '
        'generate histograms (not actually read)')
    args = parser.parse_args(argv)

    histogram_file_in = args.image + '_hist.csv'
    colors = np.array(penny_r.get_colors(histogram_file_in, rounded=False))

    pcao = pca.PCA(colors, fraction=1)

    #import pdb;pdb.set_trace()
    #print p
    # principal component vectors = pcao.Vt
    # RGB triplets in principal components = pcao.pc()
    penny_pc = pcao.pc()

    title_format = ':^10s'
    stat_format = ':10.2f'
    stat_titles = 'min', 'q1', 'median', 'mean', 'q3', 'max'
    stat_funcs = min, lambda a: sps.scoreatpercentile(a, 25), np.median, np.mean, lambda a: sps.scoreatpercentile(a, 75), max
    assert len(stat_titles) == len(stat_funcs)
    print ' | '.join(['{' + title_format + '}'] * len(stat_titles)).format(*stat_titles)
    for pc_set in penny_pc.T:
        print ' | '.join(['{' + stat_format + '}'] * len(stat_funcs)).format(*[f(pc_set) for f in stat_funcs])


    # find image bounds to synthesize
    im_pc1_bounds = [min(penny_pc.T[0]), max(penny_pc.T[0])]
    im_pc1_range = im_pc1_bounds[1] - im_pc1_bounds[0]
    im_pc1_bounds[0] = im_pc1_bounds[0] - 0.25 * im_pc1_range
    im_pc1_bounds[1] = im_pc1_bounds[1] + 0.25 * im_pc1_range
    
    im_pc2_bounds = [min(penny_pc.T[1]), max(penny_pc.T[1])]
    im_pc2_range = im_pc2_bounds[1] - im_pc2_bounds[0]
    im_pc2_bounds[0] = im_pc2_bounds[0] - 0.25 * im_pc2_range
    im_pc2_bounds[1] = im_pc2_bounds[1] + 0.25 * im_pc2_range

    im_pc1_ax = np.arange(*[round(x) for x in im_pc1_bounds])
    im_pc2_ax = np.arange(*[round(x) for x in im_pc2_bounds])
    im_pc1_AX, im_pc2_AX = np.meshgrid(im_pc1_ax, im_pc2_ax)

    im = np.empty(im_pc1_AX.shape + (3,))
    for i, row in enumerate(im):
        for j, pxl in enumerate(row):
            im[i, j] = pcao.Vt[0] * im_pc1_ax[j] + pcao.Vt[1] * im_pc2_ax[i]
            im[i, j] = im[i, j] / 255

    fig, ax = plt.subplots()
    ax.plot(penny_pc.T[0], penny_pc.T[1], linestyle='none', marker='o', color='lime', markersize=10, alpha=0.5)
    ax.imshow(im, extent=[min(im_pc1_ax), max(im_pc1_ax), min(im_pc2_ax), max(im_pc2_ax)])
    ax.set_aspect('auto')
    ax.set_title('Penny Color Space')
    ax.set_xlabel('PC1 (1 unit = {} RGB units, of 255)'.format(', '.join('{:0.3f}'.format(v) for v in pcao.Vt[0])))
    ax.set_ylabel('PC2 (1 unit = {} RGB units, of 255)'.format(', '.join('{:0.3f}'.format(v) for v in pcao.Vt[1])))
    
    f2, ax2 = plt.subplots()
    pc1 = penny_pc.T[0]
    ax2.hist(pc1, bins=10, normed=True)
    norm_mean, norm_sd = sps.norm.fit(pc1)
    x = np.linspace(norm_mean - 4*norm_sd, norm_mean + 4*norm_sd, 100)
    y = sps.norm.pdf(x, norm_mean, norm_sd)
    ax2.autoscale(False, axis='x')
    ax2.plot(x, y, color='red', lw=5)
    ax2.set_title('Penny PC1 color distribution')
    ax2.set_xlabel('PC1')
    ax2.set_ylabel('Frequency')

    #print 'norm: ', sps.kstest(pc1, lambda x: sps.norm.cdf(x, *sps.norm.fit(pc1)))

    #spo.leastsq(lambda p, x: skew.skew(x, *p) - pc1, [0.5]*3, ())
    #print 'norm: ', sps.kstest(pc1, lambda x: sps.norm.cdf(x, *sps.norm.fit(pc1)))
    #print 'norm: ', sps.kstest(pc1, lambda x: sps.norm.cdf(x, *sps.norm.fit(pc1)))

    plt.show()

if __name__ == '__main__':
    sys.exit(main())
