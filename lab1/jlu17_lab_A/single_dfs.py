'''
Roger Lu, Liam Peachey, Yanzhi Li
CS365 Lab1
single_dfs.py

single_dfs API
'''

from state_and_transition import StateRepresentation,transitionFunction,goalTest
from maze_initializer import maze_initializer
import argparse

parser = argparse.ArgumentParser(description="maze reader")
parser.add_argument('-i', '--input', help = 'Enter the input maze .txt file', \
	required = True, dest = "inMaze")

args = parser.parse_args()

inputMaze = args.inMaze

class FrontierNode:
    def __init__(self,state,parent):
        self.state=state
        self.parent=parent #Obj of FrontierNode

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

def single_dfs(initialState):
    frontier=[FrontierNode(initialState,None)]
    visitedLocations=[(frontier[0].state.mouseX,frontier[0].state.mouseY)]
    nodesExpanded=0
    while True:
        currentNode=frontier.pop()
        for i in range(4):
            nodesExpanded+=1
            temp=transitionFunction(currentNode.state,i)
            if goalTest(temp):
                return path(FrontierNode(temp,currentNode),nodesExpanded)
            if (temp.mouseX,temp.mouseY) not in visitedLocations:
                frontier.append(FrontierNode(temp,currentNode))
                visitedLocations.append((temp.mouseX,temp.mouseY))
        if len(frontier)==0:
            break
    return "No Path!!"

mousePos,prizePos,mazeArray = maze_initializer(inputMaze)
state=StateRepresentation(mousePos[0],mousePos[1],len(prizePos),mazeArray)
single_dfs(state)