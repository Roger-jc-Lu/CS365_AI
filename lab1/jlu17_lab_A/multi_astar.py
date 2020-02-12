'''
Roger Lu, Liam Peachey, Yanzhi Li
CS365 Lab1
multi_astar.py

multi_astar API
'''

from state_and_transition import StateRepresentation,transitionFunction,goalTest
from maze_initializer import maze_initializer
import argparse
import copy

parser = argparse.ArgumentParser(description="maze reader")
parser.add_argument('-i', '--input', help = 'Enter the input maze .txt file', \
	required = True, dest = "inMaze")

args = parser.parse_args()

inputMaze = args.inMaze

class FrontierAstarNodeWithWeight():
    def __init__(self,state,parent,weight,depth, weightList, prizeLocation):
        self.state=state
        self.parent=parent
        self.weight=weight
        self.depth=depth
        self.weightList = weightList
        self.prizeLocation = prizeLocation

def weightCalc(state,prizeLocation):
    return abs(state.mouseX-prizeLocation[0])+abs(state.mouseY-prizeLocation[1])

def recursiveWeightFinder(prizeList, start,end, elist):
    
    if start >= end:
        temp=0
        for i in range(len(prizeList)-1):
            temp=temp+abs(prizeList[i+1][0]-prizeList[i][0])+abs(prizeList[i+1][1]-prizeList[i][1])     
           
        elist.append(temp)
        
    else:
        for i in range(start,end):
            prizeList[start],prizeList[i] = prizeList[i],prizeList[start]
            recursiveWeightFinder(prizeList, start+1, end,elist)
            prizeList[start], prizeList[i] = prizeList[i], prizeList[start]

def optimalPrizePathSetFinder(prizeList):
    end = len(prizeList)
    elist=[]
    recursiveWeightFinder(prizeList, 0,end,elist)
    smallist=[]
    num=int(len(elist)/end)
    
    start=0
    while start<=len(elist)-num:
        small=min(elist[start:start+num])
        
        smallist.append(small)
        start+=num
    return smallist

def wholeHeuristicFunction(state,prizeLocations,prizePath):
    hlist=[]
    for i in range(len(prizeLocations)):
        hlist.append(weightCalc(state,prizeLocations[i])+prizePath[i])
    return min(hlist)

def binaryNodeSearch(array,start,stop,searchFor):
    if start>stop:
        return start
    middle=(stop+start)//2
    goal=array[middle].depth+array[middle].weight
    if goal==searchFor:
        return middle
    elif goal>searchFor:
        return binaryNodeSearch(array,start,middle-1,searchFor)
    else:
        return binaryNodeSearch(array,middle+1,stop,searchFor)

def path(node,nodesExpanded,originalPrizeList):#Takes a node, and returns directions
    cost=node.depth
    currentNode=node
    prizeNumber=len(originalPrizeList)
    while currentNode.parent!=None:
        if currentNode.state.prizeCount!=currentNode.parent.state.prizeCount:
            if prizeNumber>9 and prizeNumber<36:
                node.state.maze[currentNode.state.mouseX][currentNode.state.mouseY]=chr(87+prizeNumber)
            elif prizeNumber>=36:
                node.state.maze[currentNode.state.mouseX][currentNode.state.mouseY]=chr(29+prizeNumber)
            else:
                node.state.maze[currentNode.state.mouseX][currentNode.state.mouseY]=prizeNumber
            prizeNumber-=1
        currentNode=currentNode.parent
    node.state.printState()
    print("Cost:",cost)
    print("Nodes expanded:", nodesExpanded)

def multi_astar(initialState,prizeLocation):
    prizePath = optimalPrizePathSetFinder(prizeLocation)
    #print("original path done!")
    frontier=[FrontierAstarNodeWithWeight(initialState,None,wholeHeuristicFunction(initialState,prizeLocation,prizePath),0,prizePath, prizeLocation)]
    nodesExpanded=0
    while True:
        currentNode=frontier.pop(0)
        for i in range(4):
            nodesExpanded+=1
            temp=transitionFunction(currentNode.state,i)
            #if goalTest(temp):
            #    return path(newNode,nodesExpanded,prizeLocation)
            newNode=FrontierAstarNodeWithWeight(temp,currentNode,wholeHeuristicFunction(initialState,prizeLocation,prizePath),currentNode.depth+1,currentNode.weightList, currentNode.prizeLocation)
            if newNode.state.prizeCount != currentNode.state.prizeCount:
                newLocation = copy.deepcopy(newNode.prizeLocation)
                newLocation.remove((newNode.state.mouseX,newNode.state.mouseY))
                newNode.prizeLocation = newLocation
                if goalTest(temp):
                    return path(newNode,nodesExpanded,prizeLocation)
                newNode.weightList = optimalPrizePathSetFinder(newLocation)
                #print("path calculated")
                newNode.weight = wholeHeuristicFunction(newNode.state,newNode.prizeLocation,newNode.weightList)
            
            add=True
            parent=newNode.parent
            while parent!=None:
                if temp.prizeCount!=parent.state.prizeCount:
                    break
                if temp.mouseX==parent.state.mouseX and temp.mouseY==parent.state.mouseY:
                    add=False
                    break
                parent=parent.parent
            if add:
                frontier.insert(binaryNodeSearch(frontier,0,len(frontier)-1,newNode.weight+newNode.depth),newNode) 
                """
                print("Frontier: ",end="")
                for i in frontier:
                    print(i.weight+i.depth,end=", ")
                print()
                """
        if len(frontier)==0:
            break
    return "No Path!!"

mousePos,prizePos,mazeArray = maze_initializer(inputMaze)
state=StateRepresentation(mousePos[0],mousePos[1],len(prizePos),mazeArray)
multi_astar(state,prizePos)