'''
Roger Lu, Liam Peachey, Yanzhi Li
CS365 Lab1
state_and_transition.py

takes the input from maze_initializer and creates the initial states using
StateRepresentation class, 
provides transitionFunction and goalTest.
'''

from maze_initializer import maze_initializer

class StateRepresentation:
    def __init__(self,mouseX,mouseY,pCount,mazeList):
        #using two variables for the mouse's coordinates makes it easy
        # to separate them for transition checks

        self.mouseX=mouseX
        self.mouseY=mouseY

        self.prizeCount=pCount
        #keeps a running tally of how many prizes are left. 
        # For bredth and depth searches, the actual location doesn't matter, 
        # so this is enough.

        self.maze=mazeList
        #the maze itself. 2D arrays allow for the coordinates to work fine, 
        # as well as maintaining the tile structure in an easier way.

    def copy(self):
        #Makes a deep copy so that we can remove prizes when we use 
        # a transition function and not mess up other state representations.
        mazeCopy=[None]*len(self.maze)

        #creates the column bases for the maze    
        for i in range(len(self.maze)):
        #we have to populate each culumn with the row lists
            mazeCopy[i]=[None]*len(self.maze[i])
            #creates the rows for each column.
            for j in range(len(self.maze[i])):
                #For filling in the actual tiles of the maze
                mazeCopy[i][j]=self.maze[i][j]
                #Just copies what was there previously

        return StateRepresentation(self.mouseX,self.mouseY,self.prizeCount,mazeCopy)
        #Returns a full state representation. Maze was deep copied, 
        # and the others are ints so they're immutable
    
    def __eq__(self,other):#For comparing individual state representations.
        if self.mouseX==other.mouseX and self.mouseY==other.mouseY and \
        self.prizeCount==other.prizeCount and self.maze==other.maze:
            #If mouse positions or prize counts are different, 
            # then there's no way for the state to be the same. 
            # They're also the fastest to test, so it makes sense to 
            # try to short circuit with the fast stuff. Mazes are lists 
            # and python lets you compare the actual lists with == instead 
            # of the pointers so this works fine too.
            return True    # True if they're the same

        return False    #False if not.

    def printState(self):#For easy printing. Just a nice thing to have.
                        # Also inserts the mouse into the maze. 
                        # We know where it is otherwise, but we can't 
                        # actually see it in the maze.
        for i in range(len(self.maze)):     #Through columns
            for j in range(len(self.maze[i])):      #through rows
                if self.mouseX==i and self.mouseY==j:
                    #Checks to see if we hit the mouse's position.
                    
                    print("P",end="")
                    #Prints the P if we do. Changes end to "" so that we don't have 
                    # a new line yet. We only need those for each new row of the maze.
                else:       #we haven't found the mouse
                    print(self.maze[i][j],end="")
                    #so we just print whatever's in the maze normally.

            print()#Prints a new line for the next column, 
                   #or for when the whole maze is out.

def transitionFunction(state,direction):
    #Takes a state representation and a direction to move in. 

    newState=state.copy()
    # Creates the new state to work from. Prizes are removed once found, 
    # so this is necessary to not affect other state representations.
    
    if direction==0:#0 is North
        if(newState.maze[newState.mouseX-1][newState.mouseY]!="%"):
            #0 in the columns is the top of the maze, so moving up decreases the value. 
            # If there's a wall in that spot, we skip moving.
            
            newState.mouseX-=1
            # Changes the mouse's position in the new state. 
            # Same for the other directions.
        else:
            return newState

    elif direction==1:#1 is East
        if(newState.maze[newState.mouseX][newState.mouseY+1]!="%"):
            newState.mouseY+=1
        else:
            return newState

    elif direction==2:#2 is South
        if(newState.maze[newState.mouseX+1][newState.mouseY]!="%"):
            newState.mouseX+=1
        else:
            return newState

    elif direction==3:#3 is West
        if(newState.maze[newState.mouseX][newState.mouseY-1]!="%"):
            newState.mouseY-=1
        else:
            return newState

    if newState.maze[newState.mouseX][newState.mouseY]==".":
        #Checks the new adjusted position for a prize.
        newState.prizeCount-=1
        #Decrease the number of prizes by 1, since we took the prize from the maze.
        newState.maze[newState.mouseX][newState.mouseY]=" "
        #The tile now is empty since the prize is gone. 
    return newState#Returns the final state.
    
def goalTest(state):#Checks if there's success in any given state representation.
    if state.prizeCount==0:#If there are no more prizes to be found,
        return True#we're done!
    return False