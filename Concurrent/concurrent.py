#!\home\thoma\main\Final_Project\Concurrent\concurrent.py
"""
Title          : concurrent.py
Description    : Cellular Life Simulator
Author         : Thomas Cook
Date           : 04/29/2024
Version        : 1.0
Usage          : python concurrent.py -i <path_to_input_file> -o <path_to_output_file> -p <int>
Notes          : The input file will contain a matrix of cells. The matrix will be a square matrix of size m x n where m and n are positive integers
Python Version : 3.11.1
"""
#-i <path_to_input_file> Input type: string, required
#-o <path_to_output_file> Input type: string, required
#-p <int> Input type: int, not required, default value is 1

import argparse
import sys
import copy
import multiprocessing as mp

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

def create_chunks(matrix, num_chunks):
    chunk_size = len(matrix) // num_chunks
    chunked_matrix = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk = matrix[start:end]
        
        # Add the row above the current chunk
        if i > 0:
            chunk.insert(0, matrix[start-1])
        else:
            chunk.insert(0, matrix[-1])  # Add the last row for the first chunk
        
        # Add the row below the current chunk
        if i < num_chunks - 1:
            chunk.append(matrix[end])
        else:
            chunk.append(matrix[0])  # Add the first row for the last chunk
        
        chunked_matrix.append(chunk)
    return chunked_matrix


def main():
    print("Project :: 11788009")
    try:
        with open(args.input, "r") as input_file: #Read the input file
            matrix = [list(line.strip()) for line in input_file] #Stores lines of input file in a 2D list
    except FileNotFoundError:
        print("Input file not found")
        sys.exit(1)

    #We need to create chunks of the matrix to be processed by each process
    #chunked_matrix = create_chunks(matrix, args.processes)
    #print(chunked_matrix)

    #Implement the concurrent part of the program
    pool = mp.Pool(processes = args.processes) #Create a pool of processes given user input
    for _ in range(100):
        chunked_matrix = create_chunks(matrix, args.processes)
        simulated_chunks = pool.map(simulate, chunked_matrix)

        matrix = []
        for chunk in simulated_chunks:
            matrix.extend(chunk[1:-1])
        #print(matrix)
    
    pool.close()
    pool.join()

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

