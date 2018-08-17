# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 22:37:26 2016

@author: Eric
"""

'''
Hebbian_learning
Parameters:
fcm(FCM): an fcm already created 
restraints:dictionary(tuple): dictionary that contains the range of the desired output of concepts 
stabilizers(dictionary): concepts to stabilize on and their stabilization threshold
transferFunct(function(1 argument)): function to keep values in desired range
neu(float): a float in range [0,1] that is the learning coefficient
k(int):default is max system size, how many steps the system should use to learn 
Returns: The new edge matrix for the FCM
Description: Will take an FCM and using the Nonlinear Hebbian Learning method http://biomine.ece.ualberta.ca/papers/WCCI2008.pdf
to get optimal edge values for an FCM starting from an initial state.
'''
from sys import maxsize
import numpy as np
import networkx as nx
from Simulation import simulation
#from FCM import FCM
#from FCM import Simulation
def hebbian_learning(fcm, restraints, stabilizers, transferFunct, neu, k = maxsize):
    #get error checking on all parameters...
    limit = k
    count = 0
    oldValues = [] #list for values of concepts
    done = False
    nodeOrder = fcm._fcm_graph.nodes() 
    edgeMatrix = nx.to_numpy_matrix(fcm._fcm_graph) #edge matrix not transposed(input to concept in the column)
    #get the list of values in node order
    for node in nodeOrder:
                oldValues.append(fcm.concepts()[node])
    shape = edgeMatrix.shape#get dimensions of the matrix
    numRows = shape[0]
    numCols = shape[1]
    stableConcepts = stable_concepts(fcm) #find any concepts that have no input vectors(equation does not maintain edges it seems)
    while count < limit:
        if count == 0:
            oldConceptValues = fcm.concepts()#get concepts before changes to compare to loop break
        else:
            oldConceptValues = newConceptValues
        for row in range(0,numRows): #call equation to update edge values for each value in edgematrix
            #for col in range(0,numCols):#column is target
                #pass edge to edgeupdate
                
            newRow = updateEdge(edgeMatrix[row],oldValues[row],oldValues,neu)#pass oldvalues source as a single digit as it wont change. send targets as list to work through with row
            #set new values in edge matrix
            edgeMatrix[row] = newRow
                
        #calculate new concempt values:refer to update nodes in simulation method. will only need slight modifications
        newValues = updateConcepts(edgeMatrix,oldValues,transferFunct,stableConcepts)
        
        #set values of fcm to the new values from the equation
        index = 0
        for node in fcm._fcm_graph.nodes():#keep things in node order
            fcm.set_value(node,newValues[index])
            index += 1
        
        #set the edge strengths to the new edge values
        for row in range(0,numRows):
            for col in range(0,numCols):
                if edgeMatrix.item((row,col)) == 0:
                    continue
                fcm.add_edge(fcm._fcm_graph.nodes()[row],fcm._fcm_graph.nodes()[col],edgeMatrix.item((row,col)))
                
        #now start a simultion with fcm
        sim = simulation(fcm)
        
        for key in stabilizers:
            sim.stabilize(key,stabilizers[key])
            
        #simulate til 10000 steps or stability reached
        sim.steps(10000)
        sim.changeTransferFunction(transferFunct)
        
        ValuesList = sim.run() #run simuation. returns a dict of final values as well as print them
        newConceptValues = ValuesList[len(ValuesList)-1] 
        print newConceptValues, "New values are here"
        #if the values returned from the simulation are in the desired range, and 
        #the change is less than the stabilization threshold used in the simulationthen exit the loop 
        print newConceptValues
        print restraints
        print stabilizers
        print oldConceptValues
        for key in restraints:
            if newConceptValues[key] > restraints[key][0] and newConceptValues[key] < restraints[key][1] and (abs(newConceptValues[key]-oldConceptValues[key])) < stabilizers[key]:
                done = True
                
            else:
                done = False
                break #learning not done. continue in main loop
                
        if done:
            break
        #else continue in loop
        count += 1
    return edgeMatrix
    
    
    
    
    
    
    '''
UpdateEdge
arguments: edge: row of the edge matrix to be updated
        j: Value of the source concept
        targetList: List of values of the target concepts
        neu(double [0,1]): the learning coefficient
returns: The vector of updated edge values
Description: Uses the nonlinear hebbian algorithm for updating edge values and returns the new edge values for that row.
'''
from numpy import sign
def updateEdge(edge,j,targetList,neu):
    edgeList = edge.tolist()[0]
    returnList = []
    for i in range(0,len(edgeList)):
     
        if edgeList[i] == 0: #if there is no connection between the concepts
            returnList.append(0) #do not change the concepts
        else:    
            #print sign(edgeList[i])
            #print edgeList[i]
            newEdge = edgeList[i]+neu*(j)*(targetList[i]-(sign(edgeList[i])*(j*edgeList[i])))
            if newEdge > 1:
                newEdge = 1.0
                
            elif newEdge < -1:
                newEdge = -1.0
            #print newEdge
            returnList.append(newEdge)
    rowVector = np.asarray(returnList)
    return rowVector
    
'''
    stable_concepts
    arguments: FCM: A valid fcm from the fcm class
    Returns: iterabl List: List of the index positions for nodes to remain stable
    Description: Checks which nodes have no incoming edges and marks them as to remain stable throughout the simulation
    '''
def stable_concepts(fcm):
    stableList = []
    index = 0
    for node in fcm._fcm_graph.nodes():
        if fcm._fcm_graph.in_degree(node) == 0:
            stableList.append(index)
        index += 1
    return stableList
    
    
    
    
'''     
    updateNodes
    parameters: edgeMatrix: The edgematrix for the FCM
                nodevalues(iterable list): a list in node order that machtes the edge matrix 
                transferFunction: Function to keep values in range of [-1,1]
                stableList(iterable list): list of the concepts with no incoming edges
    returns: the updated values of the nodes after one time step
    Description: will convert the list into a numpy array and multiply it with the edge list to get the changes to each node.
     the changes will be applied. Applies all nodes to the transfer function. If a node has no incoming edges it is declared 
    stable and returned to its old value
    '''
def updateConcepts(edgeMatrix, nodeValues, transferFunction, stableList):
    edgeMatrix_T = edgeMatrix.transpose()
    values_vector = np.asarray(nodeValues) #make list into a numpy vector
    update = np.dot(edgeMatrix_T,values_vector)# get new vector of values to be added
    newValues = np.add(values_vector, update) #values after addition
    newValList = newValues.tolist()[0] #convert to list
        #only apply if hs an incom,ing edge(consider this for hebbian learning. not in the method anymore would need O(n^2) check)
    newNodeValueTrans = [transferFunction(x) for x in newValList] #appl stransfer function to each value
        
    for index in stableList:
        newNodeValueTrans[index] = nodeValues[index]
    return newNodeValueTrans