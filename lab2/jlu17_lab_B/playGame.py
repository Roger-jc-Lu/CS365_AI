'''
Roger Lu, Ali Gokcelioglu
CS365 Lab B
playGame.py

Calls the function to play the game and display the result, need argparse input
result has: Who won; pieces captured by each player; total number of moves 
and the board when gameover.
'''

from node import play_game
from environment_state import State
import argparse

parser = argparse.ArgumentParser(description="game setter")
parser.add_argument('-y', '--row', help = 'Enter the number of rows for the board', \
required = True, dest = "row")
parser.add_argument('-x', '--column', help = 'Enter the number of columns for the board', \
required = True, dest = "column")
parser.add_argument('-p', '--pieces', help = 'Enter the number of rows of pieces', \
required = True, dest = "rowOfPiece")
parser.add_argument('-a', '--utility_function1', \
help = "Enter the utility function white will use" + "\n" + "****Choices: e: Evasive | " \
+ "c: Conqueror | w: Winner takes all | ?:???" , required = True, dest = "utility_function1")
parser.add_argument('-b', '--utility_function2', \
help = "Enter the utility function white will use" + "\n" + "****Choices: e: Evasive | " \
+ "c: Conqueror | w: Winner takes all | ?:???" , required = True, dest = "utility_function2")

args = parser.parse_args()

row = int(args.row)
column = int(args.column)
rowOfPiece = int(args.rowOfPiece)
utility_function1 = args.utility_function1
utility_function2 = args.utility_function2

trail = State()
trail.initial_state(row, column, rowOfPiece)
root = play_game(utility_function1, utility_function2, trail)