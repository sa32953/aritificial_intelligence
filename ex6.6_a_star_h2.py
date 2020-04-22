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

    folger=folger.reshape(len(folger)/9,3,3)    
    return folger #Return list of all successor nodes

##############################
###  Calculate Heuristics  ###
##############################

def h2(current_node,goal):
    
    target_node=np.copy(goal)
    
    h2=0
    for i in range(9):
        compare=(np.argwhere(current_node==i))==(np.argwhere(target_node==i))
        if compare.all()==False:
            diff_vec=(np.argwhere(target_node==i)-np.argwhere(current_node==i)).flatten()
            h2=h2+abs(diff_vec[0])+abs(diff_vec[1])
    return h2


##############################
###     Main Function      ###
##############################

def a_star_h2(start,goal):
    global result
    node_list=start.reshape(1,3,3)

    f_c = 0 #Intializing depth counting variable
    n_c = 0 #Intializing node counting variable

    while True:
        if node_list.size==0:
            result=0
            print('Nada !')
            return result

        node=node_list[0]
        node_list=node_list[1:]

        compare = node== goal
        if compare.all()==True:
            result=1
            print('Goal State reached:\n{}'.format(node))
            print('Solution found at depth {}'.format(f_c))
            print('Total nodes generated {}'.format(n_c))
            print('Time taken to solve: {} sec'.format(time.clock()-s_t))
            return result

        #Generating and Sorting the successor nodes
        folger=successor(node)
        n_c=n_c+len(folger) #Counting successor nodes generated
        node_list=np.append(node_list,folger)
        node_list=node_list.reshape(len(node_list)/9,3,3)
        f_c=f_c+1 #Counting depth of expansion

        #Computing heuristics values for each node
        h_value=np.array([])
        for i in range(len(node_list)):
            h_value=np.append(h_value,h2(node_list[i],goal))
        
        node_list= node_list[h_value.argsort()]

result=0
s_t=time.clock()

#Calling main function
result=a_star_h2(start,goal)

