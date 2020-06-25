import numpy as np 
import matplotlib.pyplot as plt

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

# Making 1 full dataset
total_data = pts_vec + test_vec

##############################
###   Normalization Func   ###
##############################

def norm(x, minx, maxx):
    x = (x - minx)/(maxx - minx)
    return x

#for every vector in dataset each point is normalized with above function
for i in range(len(total_data)):
    for k in range(len(total_data[0])):
        total_data[i][k] = norm( total_data[i][k] , min(a[k] for a in total_data) , max(a[k] for a in total_data) )

#print(total_data[0])

##############################
###     Distance Func      ###
##############################

# Distance function b/w test_vec[i] and all pts_vec (calculating Manhattan distance)
def dist(v1, v2):
    d = 0
    for m in range(len(v1)):
        d = d + abs(v1[m]-v2[m])
    return d

# Choose i-th point from total_data and predict class of this point wrt all other points
# ...if predicted class doesn't match with actual class then increment error by 1
# ... repeat by changing value if i and average error over total data
error = 0

def classify(kn):
    error = 0
    for a in range(len(total_data)):
    
        known = total_data.copy()
        unknown = known.pop(a)
        
        dist_vec = [None] * len(known)
    
        for i in range(len(known)):
            dist_vec[i]=dist(unknown,known[i])
    
        set_closeset = [None] * kn

        # Find set of closest classes
        for j in range(kn):
            closest = dist_vec.index(min(dist_vec)) # Find argmin
            set_closeset[j] = known[closest][15]
            dist_vec.pop(closest)
    
        # Count which of the two classes has more points
        class0 = 0
        class1 = 0      

        for m in range(len(set_closeset)):
            if set_closeset[m] == 1.0:
                class1 = class1 + 1

            elif set_closeset[m] == 0.0:
                class0 = class0 + 1

        # Prediction
        if class1 > class0:
            new_class = 1.0

        elif class0 > class1:
            new_class = 0.0

        elif class0 == class1:
            new_class = 2.0 # couldn't classify

        if new_class != unknown[15]:
            error = error + 1

    return error

k_max=10
err = [None] * k_max
knn = [None] * k_max
print('Generating plot ....')
for p in range(k_max):
    err[p] = classify(p+1)/len(total_data)
    knn[p] = p+1


plt.plot(knn,err,color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)
plt.xlabel('k (Number of Nearest Neighbours)') 
plt.ylabel('Error Rate') 
plt.title('Error Rate vs k') 
plt.show()

#print(err/len(total_data))