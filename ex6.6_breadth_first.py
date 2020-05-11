#!/usr/bin/env python
import numpy as np
import time

##############################
###   Problem definiton    ###
##############################

#Define start state
s_row1=[1,0,3] #Zero means empty tile
s_row2=[4,2,6]
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
node_list=[None]
node_list[0]=np.array([base,start])

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
    global path

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

#based on Psuedo code from AI script

def bfs(node_list,goal):
    global f_c, new_nodes
    global n_c, all_nodes, path
    
    new_nodes=[] #Empty the list of new nodes every time function is called
    
    for i in range(len(node_list)):
        compare = node_list[i][1] == goal #Compare 'y' node-array with goal 
        if compare.all() == True:
            print('Goal state reached:\n{}'.format(node_list[i][1]))
            print('Solution found at depth {}'.format(f_c))
            print('Total nodes generated {}'.format(n_c))
            print('Time taken to solve: {} sec'.format(time.clock()-s_t))
            print('Predecessor path is as follows:')
            path = [node_list[i][1]]
            predecessor(node_list[i][1])
            
        #If soln is not found generate all successor nodes again
        new_nodes = new_nodes + successor(node_list[i][1])
                   
        i=i+1
    
    #Store each and every node produced
    all_nodes = all_nodes + new_nodes
    n_c=n_c+len(new_nodes)
    #Will tell how many nodes are generated in each depth
    
    if new_nodes != []:
        f_c=f_c+1 #Calculates to what depth we have expanded
        bfs(new_nodes,goal)
        
    else:
        print('No solution found')

##############################
###          RUN           ###
##############################

f_c=0 #Intializing depth counting variable
n_c=0 #Intializing node counting variable

#call main function with defined problem
s_t=time.clock()
bfs(node_list,goal)


