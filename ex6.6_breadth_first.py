#!/usr/bin/env python
import numpy as np

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

node_list=np.copy(start) 
node_list=node_list.reshape(1,3,3) #this will be input to main function

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

#based on Psuedo code from AI script

def bfs(node_list,goal):
    
    new_nodes=np.array([])
    #depth=depth+1
    for i in range(len(node_list)):
        compare=node_list[i]== goal
        if compare.all()==True:
            print('Goal state reached')
            print(node_list[i])
            quit() #quit program when solution found, otherwise there will be endless loop
            
        #If soln is not found generate all successor nodes again
        new_nodes=np.append([new_nodes],[successor(node_list[i])])

        #Append without axis definiton will give flattened array. So we need to reshape.
        new_nodes=new_nodes.reshape(len(new_nodes)/9,3,3)
        
        i=i+1
    
    #Will tell how many nodes are generated in each depth
    print(len(new_nodes))
    
    if (new_nodes.size!=0) == True:
        bfs(new_nodes,goal)
        
    else:
        print('No solution found')


#call main function with defined problem
bfs(node_list,goal)

############################################################################################
##Few tweaks to be done

#Solution is on what depth? (check how many times a func is called)
#Total how many nodes generated (on each level)?
#Time taken to solve the problem?