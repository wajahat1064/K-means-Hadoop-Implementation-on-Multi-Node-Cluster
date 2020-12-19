#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Wajahat Waheed, David Olson, and Bruno Hnatusko III 
#Author: Bruno Hnatusko III
#A simple mapper that takes in and prints pairs of numbers for K-means.
import sys
for line in sys.stdin:
    line = line.strip()
    coords = line.split(',')
    print('%s\t%s'%(coords[0],coords[1]))