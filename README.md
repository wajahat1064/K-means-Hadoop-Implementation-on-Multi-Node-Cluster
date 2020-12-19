# K-means-Hadoop-Implementation-on-Multi-Node-Cluster

# The "Code" folder contains the following:
Finalized source code: I wrote this with the goal of including scalability in regards 
to centroids and clusters. Simply put, this code can handle any number of centroids
and clusters.

# Mapper_wdb.py: The Mapper
reducer_wdb.py: the reducer, which prints the final centroids.
reducer_for_graphing_wdb.py: does what the previous code does, but also
prints the centroids and points in each cluster into a txt file at the start
of the algorithm (after the first cluster assignment) and at the end of each iteration.
grapher_wdb.py: takes one input file, in the form of reducer_for_graphing's output files,
and creates a scatter plot. Can plot every n-th point in each cluster to save time. Each
cluster is given a unique color, brightened for the cluster and darkened for the 
corresponding centroid.

# k_means_output: the folder created by reducer_for_graphing_wdb.py, which contains txt files
listing the centroids and points of each cluster, with a delimiter line in-between each group of points.
This can be deleted, as reducer_for_graphing already deletes the file if it exists and creates a new one.
It was left in in case you wanted to look at the data.

# centroids.txt: 
A text file that contains randomly chosen centroids. If you wish, you can add/subtract centroids
from it. I tested this with a fourth centroid and the code worked perfectly. 

# Other text files: 
Airbnb_edited and latlong are datasets I used as input for the mapper. 
I used airbnb_edited for testing and the report. 

# Plots: A folder that contains the plots I used in the report. 
Air_bnb data was used. I set my code to plot every hundredth point in each cluster when I generated these graphs so 
it would not take incredibly long to create a graph (plus the points are already crammed together anyway).

# Screenshots: Contains screenshots of the Multi-Node Cluster. 
 
# How to use: 

When in the code folder directory, you can do the following:
Simple mapreduce: cat airbnb_edited.txt | python mapper_wdb.py | python reducer_wdb.py
Graph mapreduce: cat airbnb_edited.txt | python mapper_wdb.py | python reducer_for_graphing_wdb.py
Graph creation: (NOTE: You may need to enter this in the terminal first: python -m pip install matplotlib)
	Beginning: cat k_means_output/beginning.txt | python grapher_wdb.py
	Iteration i (replace i with an iteration number): cat k_means_output/output_i.txt | python grapher_wdb.py

HDFS cluster: The input and output directories as well as the project folder directory
depending on where you place files in your HDFS cluster, so I put in placeholder names.

hadoop jar /usr/local/hadoop/hadoop-streaming-2.10.1.jar -mapper OurProjectFolderDirectory/Code/mapper_wdb.py -reducer OurProjectFolderDirectory/reducer_wdb.py -input /ClusterFolder/ClusterInput.txt -output /ClusterFolder/OutputFolder
