#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''..
   circle_histogram.py
.. moduleauthor:: Nick Timkovich <ntimkovich@u.northwestern.edu>

Uses defined circular regions to make masks then histograms the pixels.  
Writes three rows (red, green blue) for each region.
'''
import sys
import argparse
import csv

import Image
import ImageDraw

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Uses defined circular '
        'regions to make masks then histograms the pixels.  Writes three '
        'rows (red, green blue) for each region.')
    parser.add_argument('image', type=str, help='Input image.  Region data '
        'file is assumed to have the same name with a bonus "_hist.csv" '
        'extension')

    args = parser.parse_args(argv)

    region_file_in = args.image + '.csv'
    histogram_file_out = args.image + '_hist.csv'
    
    im = Image.open(args.image)
    
    with open(region_file_in, 'rb') as fi:
        regioncsv = csv.reader(fi)
        with open(histogram_file_out, 'wb') as fo:
            histcsv = csv.writer(fo)
            for row in regioncsv:
                print row
                num, x, y, r = row
                num = int(num)
                x = float(x)
                y = float(y)
                r = float(r)

                # adapted from http://stackoverflow.com/a/4380602/194586
                # make an empty image
                mask=Image.new('L', im.size, color=0)
                # "initalize a draw object" (dunno quite what that means)
                draw=ImageDraw.Draw(mask)
                draw.ellipse((x - r, y - r, x + r, y + r), fill=255)

                # get the histogram in the masked region
                hist_all = im.histogram(mask)
                hist_rgb = [hist_all[256*n:256*(n+1)] for n in xrange(3)]
                for hist, color in zip(hist_rgb, 'RGB'):
                    histcsv.writerow([num, color] + hist)

if __name__ == '__main__':
    sys.exit(main())