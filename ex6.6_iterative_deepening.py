#!/usr/bin/env python
import numpy as np
import time

##############################
###   Problem definiton    ###
##############################

#Define start state
s_row1=[4,1,3] #Zero means empty tile
s_row2=[0,2,6]
s_row3=[7,5,8]
start = np.array([s_row1,s_row2,s_row3])
#Define Goal state
g_row1=[1,2,3]
g_row2=[4,5,6]
g_row3=[7,8,0]
goal = np.array([g_row1,g_row2,g_row3])

# Base is defined as null array. This denote the predecessor of starting node.
base = (np.array([0]*9)).reshape(3,3)

#First input to the function
node_s=[None]
node_s[0]=np.array([base,start])

#Intializations
all_nodes = []
new_nodes = []

#Notes: 
#1. All nodes generated in this process are saved in a list for finding the predecessor.
#2. Each node is a list of of [x,y] type where x is the predecossor of y.
#3. x and y are 2 dimensional numpy arrays.

##############################
###   Successor Function   ###
##############################

#Function to switch 2 tiles (this will generate new successor node)
#Takes 3 arguments > 2 positions to be exchanged and the Node in which this has to be done
def switch_place(zp,sf,node):
    switch=np.copy(node)
    temp=switch[zp[0]][zp[1]]
    switch[zp[0],zp[1]]=switch[sf[0],sf[1]]
    switch[sf[0],sf[1]]=temp
    return switch

#Func to find all possible successors of any node- There may be at max 4 cases....
#... depending on location of empty space
def successor(node):
    
    #Find argument where zero exist
    zero_posn=np.argwhere(node==0)
    zero_posn=zero_posn.flatten()

    folger= [] #Intialize empty list of successors

    #Shift down
    shift_posn=np.copy(zero_posn)
    shift_posn[0]=shift_posn[0]+1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        down_shift_node = switch_place(zero_posn,shift_posn,node)
        down_shift_node = np.array([node,down_shift_node]) #Associate predecessor with successor
        
        folger = folger + [down_shift_node] #Append list of successors
    
    #Shift up
    shift_posn=np.copy(zero_posn)
    shift_posn[0]=shift_posn[0]-1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        up_shift_node = switch_place(zero_posn,shift_posn,node)
        up_shift_node = np.array([node,up_shift_node]) #Associate predecessor with successor
       
        folger = folger + [up_shift_node] #Append list of successors
          
    #Shift right
    shift_posn=np.copy(zero_posn)
    shift_posn[1]=shift_posn[1]+1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        right_shift_node = switch_place(zero_posn,shift_posn,node)
        right_shift_node = np.array([node,right_shift_node]) #Associate predecessor with successor
     
        folger = folger + [right_shift_node] #Append list of successors
       
    #Shift left
    shift_posn=np.copy(zero_posn)
    shift_posn[1]=shift_posn[1]-1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        left_shift_node = switch_place(zero_posn,shift_posn,node)
        left_shift_node = np.array([node,left_shift_node]) #Associate predecessor with successor
 
        folger = folger + [left_shift_node] #Append list of successors
       
    return folger #Return list of all successor nodes


##############################
###  Predecessor Function  ###
##############################

def predecessor(node):
    #This function finds out the predecessor by calling recursively
    global path, all_nodes

    compare = node == start
    #While calling recursively, predecessor is equal to start node, then our job is over !
    if compare.all() == True:
        print np.array(path)
        quit()
    
    #Find element where 'y' array is eqaul to the node for which predecessor is to be found
    #Once done, take the 'x' array > this is one of the path elements
    #Set this 'x' and new 'y' and find its predecessor until we reach start node.

    else: 
        for k in range(len(all_nodes)):
            if (all_nodes[k][1] == node).all() == True:                
                new_node = all_nodes[k][0]
                path = path + [new_node]
                predecessor(new_node) #Call recursively
            k=k+1

##############################
###     Main Function      ###
##############################

# as per Pseudo code in AI script

def dfsb(node_list,goal,depth,d_limit):
    global n_c, path, all_nodes

    compare = node_list[0][1] == goal #Comparing the first node of list
    if compare.all()==True:
        result=1
        return result
    
    else:
        new_nodes = successor(node_list[0][1])
        n_c=n_c+len(new_nodes) #Counting nodes
        #However, this will be redundant as same nodes will be computed again and again when...
        #... we increment the depth limit

    all_nodes = all_nodes + new_nodes #Storing all nodes to compute the predecessors
        
    while depth < d_limit and new_nodes!=[]:
        
        result=dfsb(new_nodes,goal,depth+1,d_limit) #Calling recursively but following depth limit criteria
        
        if result==1:
            print('Goal State reached:\n{}'.format(new_nodes[0][1]))
            print('Solution found at depth: {}'.format(d_limit))
            print('Total nodes generated (repeated nodes included): {}'.format(n_c))
            print('Time taken to solve: {} sec'.format(time.clock()-s_t))
            print('Predecessor path is as follows:')
            path = [new_nodes[0][1]]
            predecessor(new_nodes[0][1])
            quit()
        new_nodes=new_nodes[1:] #Remove the first node from the list and go ahead
    return ('No solution found !')
    
        
result=0 #Initialization of variable

def itd(node_list,goal):
    global result
    d_limit=0
    
    #True loop because this method is complete and will find ...
    #... a soln if there exists any
    while True:
        result=dfsb(node_list,goal,0,d_limit)
        d_limit=d_limit+1
        

##############################
###          RUN           ###
##############################

n_c=0 #Intializing node counting variable
s_t=time.clock()

#Call main function with defined problem
itd(node_s,goal)

# NOTES: 
#1. Count nodes generated. No fun in counting this as same node will be generated...
#... multiple times
#2. Count time taken