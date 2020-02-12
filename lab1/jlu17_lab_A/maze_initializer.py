'''
Roger Lu, Liam Peachey, Yanzhi Li
CS365 Lab1
maze_intializer.py

takes a txt file as maze input.
'''

import argparse

parser = argparse.ArgumentParser(description="maze reader")
parser.add_argument('-i', '--input', help = 'Enter the input maze .txt file', \
	required = True, dest = "inMaze")

args = parser.parse_args()

inputMaze = args.inMaze

def maze_initializer(inputMaze):
	text = open(inputMaze, "r")
	maze_contents = text.readlines()
	text.close()

	maze_array = list()
    # the 2D array used to represent the maze

	prize_position = list()
    # a list record the position of the prizes
	for i in maze_contents:
		maze_array.append(list(i.strip()))
	# 2D array generated


	# code to print the maze for easier visualization
	'''
	for i in maze_array:
		for j in i:
			print(j, end = "")
		print()
	'''

	for i in range(len(maze_array)):
	# iterate through the array to get the position of the mouse, append the prize position
		for j in range(len(maze_array[i])):
			if maze_array[i][j] == "P":
				mouse_position = (i,j)
				maze_array[i][j]=" "#removes standard representation of the mouse from the maze.
			if maze_array[i][j] == ".":
				prize_position.append((i,j))

	return (mouse_position, prize_position, maze_array)
