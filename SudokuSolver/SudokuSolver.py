"""
@author: PREETIKA KULSHRESTHA
This program accepts an input Sudoku puzzle and outputs the solved Sudoku to a csv file in the same directory.
Reference README.txt in the folder for further information.
"""
import sys
import csv

# Sudoku defines an instance of a Sudoku game, initialized from an input file
# containing a CSV representation of a Sudoku game. An exception is raised if
# the provided filepath cannot be accessed.
class Sudoku:
    N = 9    # Class variable to store sudoku grid dimensions, this program is for 9x9 Sudoku puzzles
    
    def __init__(s, filePath):
        with open(filePath, 'r') as file:
            s.inputFilePath = filePath            
            if (not s.newSudoku(file)):
                print "Invalid sudoku input, please ensure grid complies with game rules"
                sys.exit(1)                                 

    def newSudoku(s, file):
        s.grid = [[0]*(s.N) for i in range(s.N)]        # Initialize a 2D array (list of lists) for storing the input grid 
        s.exists = [[0]*(s.N+1) for i in range(3*s.N)]  # Initialize constraints matrix for storing row, col and region constraints
        s.vector = [0 for i in range(2*s.N)]            # Initialize vector for storing the number of filled entries for rows and cols
        data = [row.rstrip().split(",") for row in file.readlines()]
        if len(data) != 9:
            return False
        for i in range(0, len(data)):
            if len(data[i]) != 9:
                return False    
            for j in range(0, len(data[i])):
                if not s.setEntry(i, j, int(data[i][j])):
                    return False
        return True
            
    # region returns the region number for the 3x3 region of a given row,col pair.
    def region(s,i,j):
        startRow = i - i%3
        startCol = j - j%3
        return (startRow + startCol/3)
    
    # setEntry updates the Sudoku grid cell (i,j) with value k, returning 
    # false if the update is incompatible with the exsiting grid constraints.
    def setEntry(s, i, j, k):
        if k == 0:                                      
            return True
        if (s.exists[i][k] or s.exists[s.N + j][k] or s.exists[2*s.N + s.region(i,j)][k]):
            return False
        s.exists[i][k], s.exists[s.N + j][k], s.exists[2*s.N + s.region(i,j)][k] = 1, 1, 1
        s.grid[i][j] = k
        s.vector[i], s.vector[j + s.N] = s.vector[i] + 1, s.vector[j + s.N] + 1
        return True

    # unsetEntry unsets the Sudoku grid cell (i,j) and restores its value to 0.
    def unsetEntry(s, i, j):
        k = s.grid[i][j]
        s.exists[i][k], s.exists[s.N + j][k], s.exists[2*s.N + s.region(i,j)][k] = 0, 0, 0
        s.grid[i][j] = 0
        s.vector[i], s.vector[j + s.N] = s.vector[i] - 1, s.vector[j + s.N] - 1
        
    # getNextBox finds the next valid blank box to fill in the grid. It uses the 
    # vector to check which is the most filled row (or column) with one or
    # more entires remaining, and then selects the first unfilled cell in row
    # (or column) and returns its coordinates. 
    def getNextBox(s):
        try:
            maxIndex = s.vector.index(max(filter(lambda x: x < s.N, s.vector)))  
        except(ValueError):
            return -1, -1      # whole grid is filled
        
        if maxIndex < s.N:
            return maxIndex, [i for i, val in enumerate(s.grid[maxIndex]) if val == 0][0] 
    
        if maxIndex >= s.N and maxIndex < 2*s.N:
            maxIndex -= s.N
            return [i for i in range(0, 9) if s.grid[i][maxIndex] == 0][0], maxIndex
          
    # solveSudoku solves the Sudoku grid using recursive backtracking.
    # It returns True if a solution is reached, False otherwise
    def solveSudoku(s):
        i, j = s.getNextBox()
        if (i == -1):
            return True     # Grid is filled
        for k in range(1,10):
            if not s.setEntry(i, j, k): # Check if k can be assigned to grid[i][j]
                continue
            if (s.solveSudoku()):       # Recursive call 
                return True
            s.unsetEntry(i, j)          # If call fails, unset the values and try next value
        return False

    # checkSudokuSol verifies that the resulting solution produced by sudoku solver 
    # is consistent with the rules of Sudoku
    def checkSudokuSol(s):
        result = [i for i in range(1, 10)] # Each row, col, region should be a permutation of this result
        for k in range(9):
            rowValid = sorted([s.grid[i][k] for i in range(0, s.N)]) == result   # matching sorted row with result 
            colValid = sorted([s.grid[k][i] for i in range(0, s.N)]) == result   # matching sorted col with result 
            regionValid = sorted([s.grid[i][j] for i in range(0, s.N) for j in range(0, s.N) if s.region(i,j) == k]) == result # matching sorted region with result 
            if not rowValid or not colValid or not regionValid: # If any of them dont match, the grid has an error
                    return False
        return True

    # writeOutput writes the output solution of a Sudoku puzzle into a csv file
    # named <input_file>_output.csv where <input_file> is the path to the file with
    # which this object was initialized.
    def writeOutput(s):
        destination = s.inputFilePath.rstrip('.csv') + '_output.csv'
        csvfile = open(destination, 'wb')
        writeData = csv.writer(csvfile, delimiter = ",")
        for i in range (0, s.N):
            writeData.writerow(s.grid[i])                 # Populate output file
    
    # This function is used for printing the Sudoku grid, it can be used to print the input or the solution
    def printSudoku(s):
       print "Grid" 
       for i in range(s.N):
           print s.grid[i]
    
#main()       
f = sys.argv[1]
try:
    newGame = Sudoku(f)    
    if not newGame.solveSudoku():
        print "No Solution Found"
        exit(1)
    newGame.writeOutput()
except EnvironmentError:
    print "Unable to open given file, please check file path"