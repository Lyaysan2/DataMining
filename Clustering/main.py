from math import sqrt

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import *
from scipy.spatial.distance import pdist
from sklearn import preprocessing

df = pd.read_csv("/Users/lyaysanz/Desktop/Mall_Customers.csv")

# select the columns by which we will analyze, it will be a 3d dimension
col = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']

# bring data back to normal
data = preprocessing.MinMaxScaler().fit_transform(df[col].values)

# using the elbow method, we estimate the optimal number of segments
data_dist = pdist(data, 'euclidean')
data_linkage = linkage(data_dist, method='average')
last = data_linkage[-10:, 2]
last_rev = last[::-1]
idxs = np.arange(1, len(last) + 1)
plt.plot(idxs, last_rev)
acceleration = np.diff(last, 2)
acceleration_rev = acceleration[::-1]
plt.plot(idxs[:-2] + 1, acceleration_rev)
plt.show()
k = acceleration_rev.argmax() + 2
print("Recommended number of clusters:", k) #график

# took 8 clusters
nClust = 8

# for each cluster I define a color
colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'orange', 5: 'c', 6: 'm', 7: 'y', 8: 'k'}

# find 8 centroids, the most distant from each other
centroids = []
start = data[0]
centroids.append(start)
point = 0
while len(centroids) < 8:
    max = -1
    for i in range(len(data)):
        dist = sqrt((data[i][0] - start[0]) ** 2 + (data[i][1] - start[1]) ** 2 + (data[i][2] - start[2]) ** 2)
        if dist > max:
            max = dist
            point = data[i]
    centroids.append(point)
    x = (point[0] + start[0]) / 2
    y = (point[1] + start[1]) / 2
    z = (point[2] + start[2]) / 2
    start = [x, y, z]

# I define each point in a cluster
c = 0
clusters = []
for i in range(len(data)):
    min = float('inf')
    for j in range(len(centroids)):
        dist = sqrt((data[i][0] - centroids[j][0]) ** 2 + (data[i][1] - centroids[j][1]) ** 2 + (data[i][2] - centroids[j][2]) ** 2)
        if dist < min:
            min = dist
            c = j
    clusters.append(c)
    centroids[c] = [(data[i][0] + centroids[c][0]) / 2, (data[i][1] + centroids[c][1]) / 2, (data[i][2] + centroids[c][2]) / 2]
print(clusters)

# build a 3D graph
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(len(data)):
    plt.scatter(data[i][0], data[i][1], data[i][2], color=colmap[clusters[i] + 1])
for i in range(len(centroids)):
    plt.scatter(centroids[i][0], centroids[i][1], centroids[i][2], color=colmap[i+1])
plt.show()

# add a column with cluster numbers to the original dataset
df['KMeans'] = clusters
res=df.groupby('KMeans')[col].mean()
res['Amount']=df.groupby('KMeans').size().values
df.to_csv('data_clust.csv')

# shows how many points are in the cluster
print(res)

# can print the data in the desired cluster, for example 0 cluster (the smallest one - 14 elements)
print(df[df['KMeans']==0])
