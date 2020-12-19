#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Wajahat Waheed, David Olson, and Bruno Hnatusko III 
#Author: Bruno Hnatusko III
#Creates a graph from a specified file created by the reducer_for_graphing program.

#You may need to put this in the terminal: python -m pip install matplotlib
import matplotlib.pyplot as plt
import math as math

#Data
centroids = []  
clusters = [] 
currentCluster = -1 #Used for assigning points to clusters.
#Colors used for graphing.
clusterColors = []
centroidColors = []

#Get centroids and clusters
import sys
for line in sys.stdin:
    line = line.strip()   
    #If the line is the delimiter, move on to the first or next cluster.
    if line == '<Cluster Follows>': 
        currentCluster = currentCluster + 1
        clusters.append([])
    else:
         (x,y) = line.split('\t')
         point = ((float(x),float(y)))
         if currentCluster == -1: #We are not yet at a cluser. This is a centroid.
             centroids.append(point)
         else: #We are at a cluster. This is a point.
             clusters[currentCluster].append(point)

clustCount = len(clusters)
        
#Create a color i/nth of the way through the color spectrum.
#A very mathematical approach because I challenge myself to find one.
#Examples: 
#0: red 
#1/6: yellow 
#1/3: green 
#1/2: cyan 
#2/3: blue
#5/6: magenta 
def makeColor(i,n):
    c = 3*float(i)/n
    #Array locations 
    prim = int(c) #Primary color coordinate: round c down.
    sec = (prim+1)%3 #Secondary color coordinate: next after prim
    #Hue determination
    u = math.floor(c/0.5)
    v = c - (0.5 * u) #How far into the current sixth of the spectrum the color is.   
    primV = 1 #Primary color value
    secV = 2*v #Secondary color value
    if (c % 1 >= 0.5): #If c is in the 2nd, 4th, or last 6th of the spectrum
        primV = 1-secV
        secV = 1
    #Color formation
    color = [0,0,0]
    color[prim] = primV
    color[sec] = secV
    return color

#Create a color partway between white and the given color.
#Examples: (1,0,0),1 -> (1,.5,.5); (1,.5,.25),.5 -> (1,.625,.3175)
def getLighterColor(color,factor):
    newColor = list(color)
    for i in range(3):
        newColor[i] += factor * float(1-newColor[i])/2
    return newColor

#Create a color partially as bright as the given color.
#Examples: (1,0,0),1 -> (.5,0,0); (1,.5,.25),.5-> (.75,.375,.1875)
def getDarkerColor(color,factor):
    newColor = list(color)
    for i in range(3):
        newColor[i] -= factor * float(newColor[i])/2
    return newColor

#Create a color for each cluster and centroid. First color is always pure red.
for i in range(clustCount):
    currentColor = makeColor(i,clustCount)
    clusterColors.append(getLighterColor(currentColor,0.5))
    centroidColors.append(getDarkerColor(currentColor,1))

#Plot each iteration-th point in each cluster. 
#Plotting may take a very long time, so it is advised not to plot all points.
increment = 100
for i in range(clustCount):
    pointCount = len(clusters[i])
    currentPoint = 0
    for point in clusters[i][0::increment]:
        (pointX,pointY) = point
        plt.scatter(pointX,pointY,color=clusterColors[i])
        currentPoint = currentPoint + increment
        #print('Point %s/%s has been plotted.'%(currentPoint,pointCount))
        #Uncomment the above line if you want the program to show you progress.
        
#Plot centroids; they must be put last so they are not overwritten.
for i in range(clustCount):
    (centX,centY) = centroids[i]
    plt.scatter(centX,centY,color=centroidColors[i])

plt.show() #Show the plot. We are done. Woohoo!



