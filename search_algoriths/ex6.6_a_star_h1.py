#!/usr/bin/env python
import numpy as np
import time

##############################
###   Problem definiton    ###
##############################

#Define start state
s_row1=[1,0,3]
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
node_s=[None]
node_s[0]=np.array([base,start, 0, 0])

#Intializations
all_nodes = []
new_nodes = []

#Notes: 
#1. All nodes generated in this process are saved in a list for finding the predecessor.
#2. Each node is a list of of [x,y,z,w] type where x is the predecossor of y.
#3. x and y are 2 dimensional numpy arrays.
#4. z is the value of Heuristics cost function.
#5. w is the depth value of said sucessor node.

##############################
###  Calculate Heuristics  ###
##############################

#Just calculating how many tiles are in wrong place

def h1(current_node,goal):
    global f_c, depth
    current_node=current_node.flatten()
    target_node=np.copy(goal)
    target_node=target_node.flatten()
    h1=0
    depth = 0
    f1=0
    
    for i in range(9):
        if current_node[i]!=target_node[i]:
            if current_node[i] != 0:
                h1=h1+1

    return h1

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

def successor(node,level):
    global all_nodes
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
        
        all_nodes = all_nodes + [down_shift_node]
        heuristics = h1(down_shift_node[1], goal)+level+1 # f=g+h
        down_shift_node = np.array([down_shift_node[0], down_shift_node[1], heuristics, level+1])
        folger = folger + [down_shift_node] #Append list of successors

    #Shift up
    shift_posn=np.copy(zero_posn)
    shift_posn[0]=shift_posn[0]-1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        up_shift_node = switch_place(zero_posn,shift_posn,node)
        up_shift_node = np.array([node,up_shift_node]) #Associate predecessor with successor

        all_nodes = all_nodes + [up_shift_node]
        heuristics = h1(up_shift_node[1], goal)+level+1
        up_shift_node = np.array([up_shift_node[0], up_shift_node[1], heuristics, level+1])
       
        folger = folger + [up_shift_node] #Append list of successors
          
    #Shift right
    shift_posn=np.copy(zero_posn)
    shift_posn[1]=shift_posn[1]+1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        right_shift_node = switch_place(zero_posn,shift_posn,node)
        right_shift_node = np.array([node,right_shift_node]) #Associate predecessor with successor
     
        all_nodes = all_nodes + [right_shift_node]
        heuristics = h1(right_shift_node[1], goal)+level+1
        right_shift_node = np.array([right_shift_node[0], right_shift_node[1], heuristics, level+1])
        folger = folger + [right_shift_node] #Append list of successors
       
    #Shift left
    shift_posn=np.copy(zero_posn)
    shift_posn[1]=shift_posn[1]-1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        left_shift_node = switch_place(zero_posn,shift_posn,node)
        left_shift_node = np.array([node,left_shift_node]) #Associate predecessor with successor
 
        all_nodes = all_nodes + [left_shift_node]
        heuristics = h1(left_shift_node[1], goal)+level+1
        left_shift_node = np.array([left_shift_node[0], left_shift_node[1], heuristics, level+1])
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

def a_star_h1(node_list,goal):
    global result, f_c, all_nodes, path, visited_nodes
    
    f_c = 0 #Intializing depth counting variable
    n_c = 0 #Intializing node counting variable
    level=0
    while True:
        if node_list == []:
            result=0
            print('Nada !')
            return result

        node = node_list[0][1]
        level = node_list[0][3]
        node_list = node_list[1:]
       
        #print node
        compare = node == goal #Comparing node under consideration with goal 
        if compare.all()==True:
            result=1
            print('Goal State reached:\n{}'.format(node))
            print('Solution found at depth {}'.format(level))
            print('Total nodes generated {}'.format(n_c))
            print('Time taken to solve: {} sec'.format(time.clock()-s_t))
            print('Predecessor path is as follows:')
            path = [node]
            predecessor(node)
            return result

        ##Generating and Sorting the successor nodes
        folger=successor(node,level)
        
        #Appending node list
        node_list = folger + node_list #This is wrong (maybe), use bisection

        node_list= sorted(node_list, key= lambda x:x[2])
        
        f_c=f_c+1 #Counting depth of expansion
        n_c=n_c+len(folger) #Counting successor nodes generate
        
        

result=0
s_t=time.clock()

#Calling main function
result=a_star_h1(node_s,goal)

