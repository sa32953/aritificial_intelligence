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

##############################
###   Successor Function   ###
##############################

#Function to switch 2 tiles (this will generate new successor node)
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
    #print(zero_posn)
    #Initialize empty successor node
    folger=np.array([])

    #Shift down
    shift_posn=np.copy(zero_posn)
    shift_posn[0]=shift_posn[0]+1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        down_shift_node = switch_place(zero_posn,shift_posn,node)
        folger=np.append([folger],[down_shift_node])
    
    #Shift up
    shift_posn=np.copy(zero_posn)
    shift_posn[0]=shift_posn[0]-1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        up_shift_node = switch_place(zero_posn,shift_posn,node)
        folger=np.append([folger],[up_shift_node])
           
    #Shift right
    shift_posn=np.copy(zero_posn)
    shift_posn[1]=shift_posn[1]+1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        right_shift_node = switch_place(zero_posn,shift_posn,node)
        folger=np.append([folger],[right_shift_node])
        
    #Shift left
    shift_posn=np.copy(zero_posn)
    shift_posn[1]=shift_posn[1]-1
    if 0<=shift_posn[0]<=2 and 0<=shift_posn[1]<=2:
        left_shift_node = switch_place(zero_posn,shift_posn,node)
        folger=np.append([folger],[left_shift_node])
        
    return folger #Return list of all successor nodes

##############################
###     Main Function      ###
##############################

def dfsb(node_list,goal,depth,d_limit):
    global n_c
    compare=node_list== goal
    
    if compare.all()==True:
        result=1
        return result
    else:
        new_nodes=successor(node_list)
        new_nodes=new_nodes.reshape(len(new_nodes)/9,3,3)
        
        

    while (new_nodes.size!=0) == True and depth<d_limit:
        result=dfsb(new_nodes[0],goal,depth+1,d_limit)
        n_c=n_c+len(new_nodes) #Counting nodes
        if result==1:
            print('Goal State reched:\n{}'.format(new_nodes[0]))
            print('Solution found at depth: {}'.format(d_limit))
            print('Total nodes generated (repeated nodes included): {}'.format(n_c))
            print('Time taken to solve: {} sec'.format(time.clock()-s_t))
            quit()
        new_nodes=new_nodes[1:]
    return ('No solution found !')
    
        
result=0

def itd(node_list,goal):
    global result
    d_limit=0
    
    while True:
        result=dfsb(node_list,goal,0,d_limit)
        d_limit=d_limit+1

n_c=0 #Intializing node counting variable
s_t=time.clock()

#Call main function with defined problem
itd(start,goal)

#Tweaks to be done
#1. Count nodes generated. No fun in counting this as same node will be generated...
#... multiple times
#2. Count time taken