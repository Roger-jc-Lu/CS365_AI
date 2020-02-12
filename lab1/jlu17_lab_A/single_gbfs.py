'''
Roger Lu, Liam Peachey, Yanzhi Li
CS365 Lab1
single_gbfs.py

single_gbfs API
'''

from state_and_transition import StateRepresentation,transitionFunction,goalTest
from maze_initializer import maze_initializer
import argparse

parser = argparse.ArgumentParser(description="maze reader")
parser.add_argument('-i', '--input', help = 'Enter the input maze .txt file', \
	required = True, dest = "inMaze")

args = parser.parse_args()

inputMaze = args.inMaze

class FrontierNodeWithWeight():
    def __init__(self,state,parent, weight):
        self.state=state
        self.parent=parent #Obj of FrontierNode
        self.weight=weight

def path(node,nodesExpanded):#Takes a node, and returns directions
    cost=-1
    currentNode=node
    while currentNode!=None:
        cost+=1
        node.state.maze[currentNode.state.mouseX][currentNode.state.mouseY]="#"
        currentNode=currentNode.parent
    node.state.printState()
    print("Cost:",cost)
    print("Nodes expanded:", nodesExpanded)

def weightCalc(state,prizeLocation):
    return abs(state.mouseX-prizeLocation[0])+abs(state.mouseY-prizeLocation[1])
    
def binaryNodeSearch(array,start,stop,searchFor):
    if start>stop:
        return start
    middle=(stop+start)//2
    if array[middle].weight==searchFor:
        return middle
    elif array[middle].weight>searchFor:
        return binaryNodeSearch(array,start,middle-1,searchFor)
    else:
        return binaryNodeSearch(array,middle+1,stop,searchFor)

def single_gbfs(initialState,prizeLocation):
    frontier=[FrontierNodeWithWeight(initialState,None,weightCalc(initialState,prizeLocation))]
    visitedLocations=[(frontier[0].state.mouseX,frontier[0].state.mouseY)]
    nodesExpanded=0
    while True:
        currentNode=frontier.pop(0)
        for i in range(4):
            nodesExpanded+=1
            temp=transitionFunction(currentNode.state,i)
            newNode=FrontierNodeWithWeight(temp,currentNode,weightCalc(temp,prizeLocation))
            if goalTest(temp):
                return path(newNode,nodesExpanded)
            if (temp.mouseX,temp.mouseY) not in visitedLocations:
                frontier.insert(binaryNodeSearch(frontier,0,len(frontier)-1,newNode.weight),newNode)                
                visitedLocations.append((temp.mouseX,temp.mouseY))
        if len(frontier)==0:
            break
    return "No Path!!"

mousePos,prizePos,mazeArray = maze_initializer(inputMaze)
state=StateRepresentation(mousePos[0],mousePos[1],len(prizePos),mazeArray)
single_gbfs(state,prizePos[0])