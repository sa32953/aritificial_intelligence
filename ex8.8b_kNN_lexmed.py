import numpy as np 
import pandas as pd

data_path = '/home/sa0102/ai/aufgaben/kapitel8/c5/lexmed.data'
test_path = '/home/sa0102/ai/aufgaben/kapitel8/c5/lexmed.test'

##############################
###   Get Training Data    ###
##############################

pts_vec = [] # All training data is stored in this list

# Read the file having text data
with open(data_path) as d:
    for line in d.readlines():
        pts_vec.append([line]) # append each line(text data) as element of list
        for i in line.split(','):
            pts_vec[-1].append(i) # splits data after comma and appends it as new element
            # Note that even after splitting data it will remain as 'str' type

# Removing the first element because it has already been split for usage 
for i in range(len(pts_vec)):
    pts_vec[i] = pts_vec[i][1:] 
    for b in range(len(pts_vec[0])):
        pts_vec[i][b]= float(pts_vec[i][b]) #conversion of text data to float

     

#Class 1 = Appendicitis +ve
#Class 0 = Appendicitis -ve

##############################
###     Get Test Data      ###
##############################

# (same process as getting training data)
test_vec = []
with open(test_path) as t:
    for line in t.readlines():
        test_vec.append([line])
        for i in line.split(','):
            test_vec[-1].append(i)

for i in range(len(test_vec)):
    test_vec[i] = test_vec[i][1:] 
    for b in range(len(test_vec[0])):
        test_vec[i][b]= float(test_vec[i][b]) #conversion of text data to float

# Initializing
correct = 0

##############################
###   Normalization Func   ###
##############################

def norm(x, minx, maxx):
    x = (x - minx)/(maxx - minx)
    return x

#for every vector in dataset each point is normalized with above function
for i in range(len(pts_vec)):
    for k in range(len(pts_vec[0])):
        pts_vec[i][k] = norm( pts_vec[i][k] , min(a[k] for a in pts_vec) , max(a[k] for a in pts_vec) )

for i in range(len(test_vec)):
    for k in range(len(test_vec[0])):
        test_vec[i][k] = norm( test_vec[i][k] , min(a[k] for a in test_vec) , max(a[k] for a in test_vec) )
#print(pts_vec[0])
#print(test_vec[0])

##############################
###     Distance Func      ###
##############################

# Distance function b/w test_vec[i] and all pts_vec (calculating Manhattan distance)
def dist(v1, v2):
    d = 0
    for m in range(len(v1)):
        d = d + abs(v1[m]-v2[m])
    return d

##############################
###     Classificaion      ###
##############################

# Finding he class for every point based on 1-NN and comparing with class already defined in test data
# ...if prediction by algorith matches the true value then variable 'correct' is incremented
# ...and finally accuracy is computed

for a in range(len(test_vec)):

    # Distance of all pts as vector
    dist_vec = [None] * len(pts_vec)
    for i in range(len(pts_vec)):
        dist_vec[i]=dist(test_vec[a],pts_vec[i])

    # find argument of closest point
    closest = dist_vec.index(min(dist_vec))

    # check what is the class of closest point and allot that as the new class
    if pts_vec[closest][15] == 1.0:
        new_class = 1.0 
    if pts_vec[closest][15] == 0.0:
        new_class = 0.0

    # if allotted class matched the true value then increment variable
    if new_class == test_vec[a][15]:
        correct = correct + 1

print('Accuracy (after normalization) @ test data is {} %.'.format(100*correct/len(test_vec)))