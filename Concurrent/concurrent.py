#In this program, I want to practice using the argparse library, to parse command line arguments so that the program can take an input file
#This is the concurrent part of the project, where we want to use the multiprocessing library to spawn multiple processes to simulate the game of life
#We determine the number of processes to spawn using the command line argument -p
#-i <path_to_input_file> Input type: string, required
#-o <path_to_output_file> Input type: string, required
#-p <int> Input type: int, not required, default value is 1

import argparse
import sys
import copy
from multiprocessing import Process

parser = argparse.ArgumentParser(description = "Cellular Life Simulator")
parser.add_argument("-i", "--input" , type = str, help = "Path to input file", required = True)
parser.add_argument("-o", "--output" ,type = str, help = "Path to output file", required = True)
parser.add_argument("-p", "--processes" ,type = int, help = "An integer that determines the number of processes to spawn", default = 1)
args = parser.parse_args()

#The input file will contain a matrix of cells. The matrix will be a square matrix of size m x n where m and n are positive integers
#The matrix contains two symbols. "." and "O" where "." represents a dead cell and "O" represents a living cell
#The output file will contain the 100th generation of the matrix following the rules of the game of life

neighbors = 0
aliveCondition = {2, 3, 5, 7}
deadCondition = {2, 4, 6, 8}
period = "."
O = "O"

def simulate(matrix):
    new_matrix = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])): #Beginning of the matrix
            neighbors = addNeighbors(matrix, i, j)
            if matrix[i][j] == period:
                if neighbors in deadCondition:
                    new_matrix[i][j] = "O"
            else:
                if neighbors in aliveCondition:
                    new_matrix[i][j] = "O"
                else:
                    new_matrix[i][j] = "."
    matrix = copy.deepcopy(new_matrix)
    return new_matrix

def addNeighbors(matrix, i, j):
    #Neighbors of the matrix are the 8 cells surrounding the current cell, we can define a sub array on sides adjacent to the current cell
    #If the cell is at the end of the matrix wrap around. This is done using the modulo operator.
    neighbors = 0
    for x in range(-1, 2): 
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if matrix[(i + x) % len(matrix)][(j + y) % len(matrix[i])] == O:
                neighbors += 1
    return neighbors


def main():
    print("Project :: 11788009")
    try:
        with open(args.input, "r") as input_file: #Read the input file
            matrix = [list(line.strip()) for line in input_file] #Stores lines of input file in a 2D list
    except FileNotFoundError:
        print("Input file not found")
        sys.exit(1)
    #print(matrix)
    #Implement the concurrent part of the program
    for _ in range(100): #Simulate the matrix for 100 generations
        processes = []
        for i in range(args.processes):
            start = i * (len(matrix) // args.processes)
            end = (i + 1) * (len(matrix) // args.processes)
            processes.append(Process(target = simulate, args = (matrix[start:end],)))
            processes[i].start()
        
        for i in range(args.processes):
            processes[i].join()
    #for _ in range(100): #Simulate the matrix for 100 generations
    #    matrix = simulate(matrix)



    print(matrix)
    try:
        with open(args.output, "w") as output_file: #Writes to an output file. With try, it will create a file if it doesn't exist
            for row in matrix:
                output_file.write("".join(row) + "\n")
    except FileNotFoundError:
        print("Error writing to output file")
        sys.exit(1)

if __name__ == "__main__":
    main()

