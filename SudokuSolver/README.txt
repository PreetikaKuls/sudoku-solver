************** README FOR SUDOKUSOLVER.PY ****************
AUTHOR: PREETIKA KULSHRESTHA
CREATED ON: NOV 3, 2014

CONTENTS
I.      USING SudokuSolver.py
II.     SUDOKU SOLVING ALGORITHM
III.    DATA STRUCTURES
IV.     ERROR CHECKING

I. USING sudoku.py
Upon execution, the program asks the user to enter the path of a file containing the Sudoku puzzle to be solved. The input should be a csv file, with the puzzle formatted as below:

   	0,3,5,2,9,0,8,6,4
	0,8,2,4,1,0,7,0,3
	7,6,4,3,8,0,0,9,0
	2,1,8,7,3,9,0,4,0
	0,0,0,8,0,4,2,3,0
	0,4,3,0,5,2,9,7,0
	4,0,6,5,7,1,0,0,9
	3,5,9,0,2,8,4,1,7
	8,0,0,9,0,0,5,2,6

The sudoku solver solves the given puzzle and saves the output in the same format as indicated above. The output file is also a csv, it is stored in the same folder as the input file. It is titled as <input_file>_output.csv. For e.g. if input file is Users/abc/Docs/sample.csv, the output file is stored as Users/abc/Docs/sample_output.csv.
If a file with such a name already exists in the directory, it is overwritten. See item IV for exception handling on improper inputs.
Sample usage:
python SudokuSolver.py <input_file>.csv
Generates <input_file>_output.csv with the solved sudoku.

II. SUDOKU SOLVING ALGORITHM

The given program uses a recursive backtracking algorithm to solve the Sudoku puzzle. It also uses constrained search. 

a. At every iteration, it identifies the most constrained cell: (i,j) which is defined as the cell in the grid whose associated row or column is maximally filled. It selects this cell and attempts to place a value k (in the range 1 to 9).
 
b. It assigns the first valid value of k in the range(1, 9) to the cell (i,j). Validity is based on the game rules (rows/columns/regions can not have duplicate values). 

c. The program then recursively solves the grid with k assigned to cell (i,j). If the recursive solution is not possible, the code backtracks to cell (i,j) and attempts to place the next valid value of k. If no other valid value of k solves the grid, the code backtracks another step to its previous assignment. 

d. The program halts when all the empty cells in the grid have been assigned a value, in adherence to the game rules.

e. Finally, it saves the output to a file. If no solution is found, “No solution found” is printed on the console.

III. DATA STRUCTURES

The variables and functions for the game of Sudoku are structured within a Class titled ‘Sudoku’. A new instance of the class is created at every execution of the program. The following are the significant data structures used for computation, which are members of the Sudoku class:

a. N - This is a class variable and is set to 9 for a 9x9 Sudoku

b. grid[N][N] - This is a 2D array (or list of lists in python) used for storing the state of the Sudoku grid. It is first initialized with 0s, then populated with the input provided by the user. At the end of a successful execution, it contains the solved sudoku grid.

c. exists[3N][N+1] - This is a 2D array (list of lists) used for storing the constraints of each cell in the grid.   It is modeled with:

   exists[0] to exists[N-1] representing rows: Columns k: 1 to 9 in rows i: 0 to N-1 represent whether row i in the grid contains item k.
   exists[N] to exists[2N-1] representing the columns: Columns k: 1 to 9 in rows j: N to 2N-1 represent whether column j in the grid contains k
   exists[2N] ti exists[3N] representing the regions (3x3 grids within sudoku): Columns k: 1 to 9 in rows 2N to 3N-1 represent whether region r in the grid contains k

Each row in exists[i] is of length N + 1 (0th column is unused), each entry ‘k’ in a row stores a 1 if that row, col or region contains value k and 0 otherwise. 

d. vector[2N] - This is a list that stores the total number of entries that are already set in a row or column. Thereby, this indicates the extent to which a given row or column is “constrained”. This vector is used by the algorithm to identify the most constrained cell for any iteration. Note: Further enhancements can also include entries for regions in addition to row and column for this vector.

e. Region (not a data structure) - The regions are defined as 3x3 sub grids in the Sudoku grid. They are numbered from 0 through 8, with the sub grid [(0,2) to (2,2)] representing region 0 and sub grid [(6,8), (8,8)] representing region 8.

IV. ERROR CHECKING

The following error conditions are handled by the code:
a. Invalid file name
b. Incorrect input
   1. Number of rows or columns is not equal to 9
   2. The provided grid is invalid (violates Sudoku rules)
c. Sudoku is unsolvable


