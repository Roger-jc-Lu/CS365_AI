'''
Roger Lu, Ali Gokcelioglu
CS365 Lab B
environment_state.py

includes the state class which represents the states during a game, with
initial_state, is_terminal, make_move, move_generator and print_state method 
'''

from copy import deepcopy

class State():

    def __init__(self, turn = False):
        #self.white and self.black will be initialized as the initial positions
        self.white = None
        self.black = None
        #whose turn it is, False for white, True for black
        self.turn = turn
        #these will be a list of game ending squares for each player
        #self.white_terminals is where white needs to get to win the game
        self.white_terminals = []
        self.black_terminals = []
    #to initialize a state, this state needs to be called
    def initial_state(self, row, column, rowOfPiece):
        #initialize white and black positions, where each position is and integer
        #yx where y is the y position and x is the x position of the square
        white_state = set()
        black_state = set()
        for i in range(1, rowOfPiece + 1):
            for j in range(1, column + 1):
                black_state.add(i * 10 + j)

        for i in range((row - rowOfPiece) + 1, (row + 1)):
            for j in range(1, column + 1):
                white_state.add(i * 10 + j)
        #self.white is this states white positions, and vice versa
        self.white = white_state
        self.black = black_state
        #the number of rows and columns for the board
        self.row = row
        self.column = column
        #how many rows of pieces each player has
        self.rowOfPiece = rowOfPiece
        #these will be a list of game ending squares for each player
        #self.white_terminals is where white needs to get to win the game
        self.black_terminals = [row*10 + x for x in range(1,column+1)]
        self.white_terminals = [10+x for x in range(1, column+1)]
        
    #returns True if a state is terminal, regarldess of who won
    def is_terminal(self):
        # since white's turn is false, if self.turn will be true on black's turn
        if self.turn:
            #self.black is black's pieces, and if they have none left, they lose
            if len(self.black) == 0:
                return True
            #checks if any of the  pieces are in an opponents final row
            #by iterating through the final rows and checking if any of them is 
            #in the self.white, which consists of white positions
            for pos in self.white_terminals:
                if pos in self.white:
                    return True
        elif not self.turn:
            if len(self.white) == 0:
                return True
            for pos in self.black_terminals:
                if pos in self.black:
                    return True
        return False
    
    #takes a 4 figit integer, the first two digits are the postion yx
    #of the moving piece, the second two are the position of the target square
    #illegal moves are not geneterade by the move generator, hence there is 
    #no need to check if the moves are valid
    def make_move(self, move):
        #by dividing by 100, we get the first two digits
        # of the four digit move, which is the original square
        #the moving piece was on
        moving_square = move // 100
        #by taking the modulo by 100,
        #we get the last two digits of the 
        target_square = move % 100
        new_state = deepcopy(self)
        #black's turn        
        if self.turn:
            #if the target square has a white piece on it, remove it
            if target_square in new_state.white:
                new_state.white.remove(target_square)
            #remove old position from black positions
            new_state.black.remove(moving_square)
            #add new new position to black positions
            new_state.black.add(target_square)
        #white's turn
        else:
            if target_square in new_state.black:
                new_state.black.remove(target_square)
            new_state.white.remove(moving_square)
            new_state.white.add(target_square)
        new_state.turn = not self.turn
        return new_state
    
    #each move is represented as a four digit number 
    def move_generator(self):
        #this will be filled with all possible moves from this state
        stateList = []
        #if it's whites turn
        if not self.turn:
            #this look iterates through all white positions
            for i in self.white:
                #since each position is an integer yx where 
                #y is the y position and x is x position, for white all moves 
                #forward will be yx - 9, 10, or 11
                moves = [i-9, i-10, i-11]
                #each move is represented as a four digit integer where the 
                #the first two digits are the position of the current square
                #and the second two digits is the target square
                #this loop iterates through all target squares, generates
                #the all possible moves that can be made, and appends
                #legal moves to thee list
                for k, j in enumerate(moves):
                    #generate move
                    move = i * 100 + j
                    #if it is non-diagonal forward move and that square is 
                    #occupied by the opponen, it is illegal
                    if k == 1 and j in self.black:
                        continue
                    #if the move is out of the board bounds, it is illegal
                    if j%10 < 1 or j%10 > self.column:
                        continue
                    #if the target square is occupied by white, it is illegal
                    if j in self.white:
                        continue
                    #if the move is not illegal, append to list
                    stateList.append(self.make_move(move))
        #do the same thing for black
        else:
            for i in self.black:
                moves = [i+9, i+10, i+11]
                for k, j in enumerate(moves):
                    move = i*100 + j 
                    if k == 1 and j in self.white:
                        continue
                    if j % 10 < 1 or j % 10 > self.column:
                        continue
                    if j in self.black:
                        continue 
                    stateList.append(self.make_move(move))
        return stateList
        
    #converts the state to a strings, used in printing
    def __str__(self):
        state = ""
        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                pos = i*10 + j
                if pos in self.black:
                    state += "X"
                elif pos in self.white:
                    state += "O"
                else:
                    state+= "."
            state+= "\n"
        return state