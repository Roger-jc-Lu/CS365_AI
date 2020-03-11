'''
Roger Lu, Ali Gokcelioglu
CS365 Lab B
node.py

includes the Node class contains node constructor for Minimax Tree expansion 
and the utility functions, also named global variables for future utility function call.
'''

import random
from environment_state import State

#this function takes heuristic function as the first letter 
#of the heuristic (e.g. 'e' for evasive),
#and an initial state
def play_game(heuristic_white, heuristic_black, state):
    global white_utility_function
    global black_utility_function 
    global utility_functions
    #the next three lines pick the utility function
    #and making it global, it allows the class to access it without copying
    utility_functions = {"e" : Node.evasive, "c" : Node.conqueror, \
    "w" : Node.winner_takes_all, "t": Node.tank}
    white_utility_function = heuristic_white
    black_utility_function = heuristic_black
    root = Node(state)
    moves = 0
    #look ahead is our minimax implementation it looks ahead three turns every time,
    #and returns the max for whoevers turn it is.
    while not root.state.is_terminal():
        root =  root.look_ahead(3)
        moves += 1
    #state.turn is False for white's turn, true for black's gurn
    winner = "White" if root.state.turn else "Black"
    #num_pieces is how many pieces each player had in the beginning of the games
    num_pieces = root.state.row * root.state.rowOfPiece
    #the number of black pieces left at the end of the game substracted
    #by the number of black pieces in the initial state is
    #how many pieces white captured, and vice versa 
    num_captured_by_white = num_pieces - len(root.state.black)
    num_captured_by_black = num_pieces - len(root.state.white) 
    print("{} won.\n White captured {} pieces.\n Black captured {} pieces.\n Total number of moves was {}"\
    .format(winner, num_captured_by_white, num_captured_by_black, moves))
    print(root.state)
    return root

class Node:

    def __init__(self, state):
        self.state = state
        #the utility function depends on whose turn it is
        #white_utility_function and black_utility function are
        #global variables declared in the play_game function
        if not self.state.turn:
            self.utility_function = utility_functions[white_utility_function]
        else:
            self.utility_function = utility_functions[black_utility_function]
        #self.value will be calculated in the look_ahead function,
        #which is our implementation of minimax
        self.value = None
        #a list of all possible children of this state
        self.childList = []
        self.parent = None
        self.depth = 0
    #overriding the < operator for minimax, so we can call the built-in min funcion
    def __lt__(self, other):
        if self.value < other.value:
            return True
        return False
    #overriding the > operatir for minimax, so we can call the built-in max function
    def __gt__(self, other):
        if self.value < other.value:
            return False
        return True
    #heuristic for eavsive
    def evasive(self, turn):
        if not turn:
            value =  len(self.state.white) + random.random()
        else:
            value = len(self.state.black) + random.random()
        return value
    #heuristic for conqueror
    def conqueror(self, turn):
        if not turn:
            value = 0 - len(self.state.black) + random.random()
        else:
            value = 0 - len(self.state.white) + random.random()
        return value
    #our first heuristic gives terminals states positive or negative infinite
    #value depending on who is winning,
    #and then calculates number of its own pieces -  number of opponents pieces
    def winner_takes_all(self, turn):
        if self.state.is_terminal():
            if turn == self.state.turn:
                value = float("inf")
            else:
                value = float("-inf")
        elif not turn:
            value = len(self.state.white) - len(self.state.black) + random.random()
        else:
            value = len(self.state.black) - len(self.state.white) + random.random()
        return value

    # The second utility function maintains the essential "one step away from winning"
    # detecting, adding a more detailed value distributing for a good attaching formation
    # and defending formation when there are more than two rows of pieces to start with.
    def tank(self, turn):
        value = random.random()
        
        if self.state.is_terminal():
            if turn == self.state.turn:
                value = float("inf")
            else:
                value = float("-inf")
            
            return value
        
        elif not turn:

            for i in self.state.white:
                if i < (self.state.row - self.state.rowOfPiece + 1) * 10:
                    if i + 1 in self.state.white:
                        value += 1
                    if i - 1 in self.state.white:
                        value += 1
                    if i + 10 in self.state.white:
                        value += 2
                    if i + 9 in self.state.white:
                        value += 2
                    if i + 11 in self.state.white:
                        value += 2
                if (i - 10 in self.state.white_terminals) and (i - 9 not in self.state.black) and (i - 11 not in self.state.black):
                    value = float("inf")
                    return value

            #if self.state.rowOfPiece >= 2:
            for j in range((self.state.row - 1) * 10 + 2, (self.state.row - 1) * 10 + self.state.column):
                if (j not in self.state.white) and (j + 9 not in self.state.white) and (j + 11 not in self.state.white):
                    value -= 5
                if (j in self.state.black) and (j + 9 not in self.state.white) and (j + 11 not in self.state.white):
                    value = float("-inf")
                    return value
                if ((((self.state.row - 1) * 10 + self.state.column) not in self.state.white) and ((self.state.row * 10 + self.state.column - 1) not in self.state.white)) or \
                ((((self.state.row - 1) * 10 + 1) not in self.state.white) and ((self.state.row * 10 + 2) not in self.state.white)):
                    value -= 5
            if ((((self.state.row - 1) * 10 + self.state.column) in self.state.black) and ((self.state.row * 10 + self.state.column - 1) not in self.state.white)) or \
            ((((self.state.row - 1) * 10 + 1) in self.state.black) and ((self.state.row * 10 + 2) not in self.state.white)):
                value = float("-inf")
                return value

            value += 10 * (len(self.state.white) - len(self.state.black))
        
        else:
            
            for i in self.state.black:
                if i > (self.state.rowOfPiece + 1) * 10:
                    if i + 1 in self.state.black:
                        value += 1
                    if i - 1 in self.state.black:
                        value += 1
                    if i - 10 in self.state.black:
                        value += 2
                    if i - 9 in self.state.black:
                        value += 2
                    if i - 11 in self.state.black:
                        value += 2
                if (i + 10 in self.state.black_terminals) and (i + 9 not in self.state.white) and (i + 11 not in self.state.white):
                    value = float("inf")
                    return value

            #if self.state.rowOfPiece >= 2:
            for j in range(22, 20 + self.state.column):
                if (j not in self.state.black) and (j - 9 not in self.state.black) and (j - 11 not in self.state.black):
                    value -= 5
                if (j in self.state.white) and (j - 9 not in self.state.black) and (j - 11 not in self.state.black):
                    value = float("-inf")
                    return value
                if (((20 + self.state.column) not in self.state.black) and ((10 + self.state.column - 1) not in self.state.black)) or \
                ((21 not in self.state.black) and (12 not in self.state.black)):
                    value -= 5
            if (((20 + self.state.column) in self.state.white) and ((10 + self.state.column - 1) not in self.state.black)) or \
            ((21 in self.state.white) and (12 not in self.state.black)):
                value = float("-inf")
                return value

            value += 10 * (len(self.state.black) - len(self.state.white))

        return value
                
    #this function makes all board states attainable in one move 
    #from the current board states
    def make_child(self):
        stateList = self.state.move_generator()
        for i in stateList:
            child = Node(i)
            child.parent = self
            child.depth = self.depth + 1
            self.childList.append(child)
            
    #finds max of all chidlren, for minimax
    def _find_max(self):
        return max(self.childList)

    #finds min of all chidlrene, for minimax
    def _find_min(self):
        return min(self.childList)

    #wrapper function for our minimax implementation
    #steps is how many steps it should look ahead
    def look_ahead(self, steps):
        self._look_ahead(steps, self.state.turn)
        maxNode = self._find_max()
        #setting the current node to an initial state
        maxNode.depth = 0
        maxNode.childList = []
        return maxNode

    #This is our minimax implementation. It recursively goes down the tree,
    #and once it goes deep enougn, it calculates the values of the children,.
    #it then goes up the tree and does minimax 
    def _look_ahead(self, target, turn):
        if self.depth < target:
            #if the node is a terminal state, it will be assinged the appropriate
            #value and its children will not be explired
            if self.state.is_terminal():
                self.value = self.utility_function(self, turn)
                return
            #generate child nodes of the current node
            self.make_child()
            #this iterates through the list of all children, and recursively
            #continue traversing the search tree for each child. It expands the 
            #the next sibling after all the children are expanded, and the 
            #leaf children have been assigned their heuristic funcitons
            for i in self.childList:
                i._look_ahead(target, turn)
            #if it's our turn, do max, else, do min
            if self.depth % 2 == 0:
                self.value = self._find_max().value
            else:
                self.value = self._find_min().value
        #if we have reached the bottom of the search tree, 
        #calculate the value of the node using the heuristic function
        else:
            self.value = self.utility_function(self,turn)
        return