#!/usr/bin/env python

import numpy as np 
import time

# Define the training data as two classes

plus = [ [8,4] , [8,6] , [9,2] , [9,5] ] # Class = 1
minus =  [ [6,1] , [7,3] , [8,2] , [9,0] ] # Class = -1

# Link points with their class; using linked list where each element is of type [a,b,c]
# c is 1 for plus class and -1 for minus class

pts_vector = [a + [1] for a in plus] + [b + [-1] for b in minus]

# Define new point to be classified
t = [8, 3.5]

# Manhatten Distance
def dist(pt1, pt2):
    d = abs(pt1[0]-pt2[0]) + abs(pt1[1]-pt2[1])
    return d

dist_vector = [None] * len(pts_vector)

# Compute distance to all points
for i in range(len(dist_vector)):
    dist_vector[i] = dist(t, pts_vector[i])

# How many close points to be identified ?
k = 1
set_closeset = [None] * k
closest= None

# Find set of closest classes
for j in range(k):
    closest = dist_vector.index(min(dist_vector)) # Find argmin
    set_closeset[j] = pts_vector[closest][2]
    dist_vector.pop(closest)

# Count which of the two classes has more points
plus_count = 0
minus_count = 0

for m in range(len(set_closeset)):
    if set_closeset[m] == 1:
        plus_count = plus_count + 1

    elif set_closeset[m] == -1:
        minus_count = minus_count + 1    


# Prediction
if plus_count > minus_count:
    new_class = 1
    print('New data is classified as {}'.format(new_class))

elif plus_count < minus_count:
    new_class = -1
    print('New data is classified as {}'.format(new_class))

elif plus_count == minus_count:
    new_class = 0
    print('Cannot define class based on given info')
