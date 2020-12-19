#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Wajahat Waheed, David Olson, and Bruno Hnatusko III 
#Author: Bruno Hnatusko III
#A k-means reducer program ALTERNATE VERSION
#Takes data-points and pre-determined centroids, then updates centroids
#To reflect averages of points that are grouped into clusters based on closest centroids.
#This version also creates folders listing centroids and clusters 
#during the start and each iteration of the algorithm, for forming graphs.

import math
import sys
import os
import shutil

#Points, Old Centroids, and New Centroids
points = []
oldCent = []
newCent = []
clustCount = 0 #Number of clusters
clusters = [] #Clusters list, begins empty
iterCount = 0 #Number of k_means iterations
#For checking convergence. Customize if you wish. 
#Lower threshold = more accuracy but less speed.
threshold = 1

#Get Points
for line in sys.stdin:
    line = line.strip()
    (x,y) = line.split('\t')
    points.append((float(x),float(y)))
    
#Get centroids file.
#HDFS may require more than a simple open() call. It did for us.
dir_path = os.path.dirname(os.path.realpath(__file__))
centFile = os.path.join(dir_path, 'centroids.txt')  
f = open(centFile)

#Create or recreate a folder for output.
outputFolderName = "k_means_output"
output_path = os.path.join(dir_path,outputFolderName)

if os.path.exists(output_path):
  shutil.rmtree(output_path)
os.mkdir(output_path)

#Get Centroids
for line in f:
    line = line.strip()
    (x,y) = line.split(',')
    newCent.append((float(x),float(y)))
clustCount = len(newCent)

#Recreates clusters.
#Empties the cluster list, examines each point, finds the closest centroid, 
#and puts that point in the centroid's corresponding cluster.
def UpdateClusters():
    global points
    global oldCent
    global clusters
    #Unlike the centroids list, the cluster list in dynamic in size,
    #so it must be emptied.
    clusters = [[] for c in range(clustCount)]
    for point in points:
        minDist = float("inf") #How far away the closest centroid is.
        chosenCluster = -1 #Index for the closest cluster.
        for i in range(clustCount):
            centroid = oldCent[i]
            xDif = point[0] - centroid[0]
            yDif = point[1] - centroid[1]
            thisDist = math.sqrt(math.pow(xDif,2) + math.pow(yDif,2))
            if thisDist < minDist: 
                chosenCluster = i
                minDist = thisDist #Min() would be used instead if we did not need to assign to a cluster
        clusters[chosenCluster].append(point) #Add point to chosen cluster.
    
#Update the centroids based on the average of coordinates in each cluster.
def UpdateCentroids():
    global clusters
    global newCent
    for i in range(clustCount):
        (sumX,sumY) = (0,0)
        cluster = clusters[i]
        count = len(cluster)
        for point in cluster:
            (sumX,sumY) = (sumX + point[0],sumY + point[1])
        if count > 0: #Create a new centroid based on the averages of the cluster's coordinates.
            newCent[i] = (sumX/count,sumY/count)
       
#Compare the old centroids with a new one.
def centroidsConverged():
    global oldCent
    global newCent
    #Both centroid lists are the same size, so this is a perfect opportunity to use zip() 
    for thisOld, thisNew in zip(oldCent,newCent): 
        difX = abs(thisNew[0] - thisOld[0])
        difY = abs(thisNew[1] - thisOld[1])
        if (difX > threshold) or (difY > threshold):
            return False #Centroids have not converged. 
    #Centroids have converged. 
    return True

#Puts centroids and clusters in a txt file.
def writeOutput(iterCount):
    fileName = 'output_%s.txt'%iterCount
    centroids = oldCent   
    if iterCount == 0:
        fileName = 'beginning.txt'
        centroids = newCent
    filePath = os.path.join(output_path, fileName)
    newFile = open(filePath,"a")
        
    for centroid in centroids:
        newFile.write('%s\t%s\n' %(centroid[0],centroid[1]))
    for cluster in clusters:
        newFile.write('<Cluster Follows>\n') #Delimiter used for the grapher program.
        for point in cluster:
            newFile.write('%s\t%s\n' %(point[0],point[1]))
        
#The main function. Encompasses all others and is recursive.
def K_means(iterCount):
    global oldCent
    global newCent
    #New centroids become old ones. 
    #The newer centroids will be determined before the end.
    oldCent = list(newCent) #oldCent becomes a copy of newCent
    UpdateClusters() 
    if iterCount == 0:
        writeOutput(iterCount)
    iterCount = iterCount + 1
    UpdateCentroids() #newCent is updated.
    writeOutput(iterCount)
    converged = centroidsConverged() #Check for convergence
    if converged:
       #The centroids are accurate enough. It is time to print them.
        for centroid in newCent:         
            print('%s\t%s' %(centroid[0],centroid[1]))
    else:
        K_means(iterCount) #The centroids are not accurate enough. Iterate again.
K_means(0) #Start the first iteration.