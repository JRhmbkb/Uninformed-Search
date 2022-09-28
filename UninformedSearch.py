############################################################
# CIS 521: Homework 2
############################################################

student_name = "Rui Jiang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy
import math
import random

############################################################
# Section 1: N-Queens
############################################################

# returns the number of all possible placements of n queens on an n × n board
def num_placements_all(n):

    # in total there are n*n total positions
    # in total there are n queens need to be placed
    # therefore, without any limitation, we can use combination factorial without distinction for (nxn choose n)
    # which is (n*n)!/(n!(n*n-n)!)

    return (math.factorial(n*n))/(math.factorial(n)*(math.factorial(n*n-n)))

# the number of possible placements of n queens on an n × n board such that each row contains exactly one queen.
def num_placements_one_per_row(n):
    # each row will have n possibilities
    # and there are n rows
    # therefore n^(n)
    
    return n**n


def n_queens_valid(board):
    #first, find the size of the board
    #which is either the max number, or len of the input
    n = max (len(board), max(board))

    # go through the whole board
    # cases to check: 1.if it's on the same row 2.if it's on the column 3. if it's on the same diagnoal
    # 1. since board is formed with differnt row as its expression, we dont need to check this
    # 2. we will loop through to see if repeated column number
    # 3. for two points (x1,y1) and (x2,y2), if |x1-x2| = |y1-y2|, then they are in diagonally  


    # check if there are same colum number
    col_set = []
    for row_location in range(len(board)):
        if board[row_location] not in col_set:
            col_set.append(board[row_location] )
        else:
            return False

    # check if any queens are in diagnonal locations
    diag_set = []         
    for row_location in range(len(board)):
        col_location = board[row_location]
        diag_set.append([row_location,col_location])


    #check if it's in diagnoal location with any
    for row_location in range(len(board)):
        col_location = board[row_location] 
        
        for [x,y] in diag_set:
            if abs(row_location - x) == abs(col_location - y) and x != row_location:#make sure it's not itself
                return False

    return True #finally return true if no false case triggered

def n_queens_solutions(n):
 
    #create return data structure
    board_final = []

    n_queens_helper(n,[],0,board_final)

    return board_final

# yields all valid placements which extend the partial solution denoted by board.
def n_queens_helper(n, board, row_counter, board_final):

    #terminal case
    #when we have enough number of rows, then stop
    if (row_counter == n):
        return board_final.append(board)

    # generate all the rows
    for row in range(n):
        if (n_queens_valid(board + [row])):
            n_queens_helper(n, board + [row], row_counter + 1, board_final)

# yields all valid placements which extend the partial solution denoted by board.


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        #simply assign self.board = board
        self.board = board

    def get_board(self):
        #simply return self.board
        return self.board

    def perform_move(self, row, col):
        # convert the corresponding location as its opposite (T->F or F->T)
        # also convert all its neighbors as its opposite if there is/are
        
        # first convert the target location from True to False or False to True
        if self.board[row][col] == True:
            self.board[row][col] = False
        else:
            self.board[row][col] = True

        # flip top if there is, from True to False or False to True
        if row - 1 >=0:
            if self.board[row - 1][col] == True:
                self.board[row - 1][col] = False
            else:
                self.board[row - 1][col] = True

        #flip right if there is, from True to False or False to True
        if col + 1 < len(self.board[0]):
            if self.board[row][col+1] == True:
                self.board[row][col+1] = False
            else:
                self.board[row][col+1] = True

        #flip bottom if there is, from True to False or False to True
        if row + 1 < len(self.board):
            if self.board[row + 1][col] == True:
                self.board[row + 1][col] = False
            else:
                self.board[row + 1][col] = True
        #flip left if there is, from True to False or False to True
        if col - 1 >= 0:
            if self.board[row][col-1] == True:
                self.board[row][col-1] = False
            else:
                self.board[row][col-1] = True
        

    def scramble(self):

        #loop through all the positions by each row and each column
        for row in range (len(self.board)):
            for col in range (len(self.board[0])):
                if random.random() < 0.5: #trigger random condition
                    self.perform_move(row,col)


    def is_solved(self):

        # loop through all the position by each row and each column
        # check if its all false
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == True:
                    return False
        return True #if no false was fouund

    # write a method copy(self)
    # that returns a new LightsOutPuzzle object initialized with a deep copy
    # of the current board. Changes made to the original puzzle should not be
    # reflected in the copy, and vice versa.
    def copy(self):
        new_self = copy.deepcopy(self)
        return new_self
    # write a method successors(self)
    # that yields all successors of the puzzle as (move, new-puzzle) tuples, where
    # moves themselves are (row, column) tuples. The second element of each
    # successor should be a new LightsOutPuzzle object whose board is the
    # result of applying the corresponding move to the current board
    def successors(self):
        # loop through all the positions
        # and move each one
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):        
                to_displaY_after_move = copy.deepcopy(self) # get a new copy so save the original template/copy
                to_displaY_after_move.perform_move(row, col)
                yield((row, col), to_displaY_after_move)  

    # returns an optimal solution to the current board as a list of moves,
    # represented as (row, column) tuples.
    def find_solution(self):

        #create the visited set of tuples
        visited = set()
        # adll all first, avoiding repeated ones due to the nature of set()
        visited.add(tuple(i) for i in self.get_board())
        
        #set up the frontier to check if it's a valid answer for each loop
        queue = [([],self)]

        # if self is already a solution, then return an empty list 
        if self.is_solved():
            return []
        #otherwise, lets go through the BFS loop and find possible solution
        while queue:
            move, puzzle = queue.pop(0) #get the first one (the default starting one)
            for new_move, new_puzzle in puzzle.successors(): #loop through all successors
                #add and find all possible next movements
                possible_solution_to_check = move + [new_move]
                if new_puzzle.is_solved(): #if it's a solved solution
                    return possible_solution_to_check #return the solution as a valid answer 

                else:
                    #get all the positions that visited by this move
                    new_puzzle_set = tuple(tuple(i) for i in new_puzzle.get_board()) #BFS
                    
                    # add this puzzle_set into the visited set and queue if it's not in the set already
                    if new_puzzle_set not in visited: 
                        visited.add(new_puzzle_set)
                        queue.append((possible_solution_to_check, new_puzzle))
        return None

# Write a top-level function create_puzzle(rows, cols) that
# returns a new LightsOutPuzzle of the specified dimensions with all lights
# initialized to the off state.
def create_puzzle(rows, cols):                                                                                                                  

    #create the specified board with all FALSE
    ret = [[False]*cols]*rows

    #return as the LightsOutPuzzle class
    return LightsOutPuzzle(ret)

    

############################################################
# Section 3: Linear Disk Movement
############################################################

# create a linear disk movement class as helper functions for solve_indentical_disk and solve_distinct_disk
class LinearDiskMovement(object):
    def __init__(self, linear_grid):
        self.linear_grid = linear_grid
    
    def get_linear_grid(self):
        return self.linear_grid
    
    def copy(self):
        new_self = copy.deepcopy(self)
        return new_self
    
    def successors_for_identical(self, length):

        for i in range(length):
            # go to the next 1 location, if the next one is free to go
            if (i + 1) < length and self.linear_grid[i] == 1 and self.linear_grid[i+1] == 0:
                possible_linear_grid = copy.deepcopy(self.linear_grid) #deep copy it to have another real copy of it
                # step to the next location, if the next one is free to go
                possible_linear_grid[i] = 0 # mark the current as 0
                possible_linear_grid[i+1] = 1 # mark the next location as 1
                # yield the movement as tuple and new linear grid
                yield((i,i+1),LinearDiskMovement(possible_linear_grid)) 
            # go to the next 2 location, if the next 1 is NOT free to go
            if (i + 2) < length and self.linear_grid[i] == 1 and self.linear_grid[i+1] ==1 and self.linear_grid[i+2] == 0:
                possible_linear_grid = copy.deepcopy(self.linear_grid) # deep copy it to have another real copy of it
                # step to the next 2 location, if the next 1 location is NOT free to go
                possible_linear_grid[i] = 0 # mark the current as 0, since it's empty now
                possible_linear_grid[i+2] = 1 # mark the next 2 location as 1, since it's occupied now
                # yield the movement as tuple and new linear grid
                yield((i,i+2),LinearDiskMovement(possible_linear_grid))     

    def successors_for_differnt(self, length):

        for i in range(length):
            # go to the next 1 location, if the next one is free to go
            if (i + 1) < length and self.linear_grid[i] != 0 and self.linear_grid[i+1] == 0:
                possible_linear_grid = copy.deepcopy(self.linear_grid)
                # step to the next location, if the next one is free to go
                possible_linear_grid[i] = 0 # mark the current as 0
                possible_linear_grid[i+1] = self.linear_grid[i] # mark the next location as what the current grid is showing
                # yield the movement as tuple and new linear grid
                yield((i,i+1),LinearDiskMovement(possible_linear_grid)) 
            # go to the next 2 location, if the next 1 is NOT free to go
            if (i + 2) < length and self.linear_grid[i] != 0 and self.linear_grid[i+1] != 0 and self.linear_grid[i+2] == 0:
                possible_linear_grid = copy.deepcopy(self.linear_grid)
                # step to the next 2 location, if the next 1 location is NOT free to go
                possible_linear_grid[i] = 0 # mark the current as 0, since it's empty now
                possible_linear_grid[i+2] = self.linear_grid[i] # mark the next 2 location as what the current grid is showing
                # yield the movement as tuple and new linear grid
                yield((i,i+2),LinearDiskMovement(possible_linear_grid)) 


            # it might also have the need to go back 1 location
            if (i - 1) >= 0 and self.linear_grid[i] != 0 and self.linear_grid[i-1] == 0:
                possible_linear_grid = copy.deepcopy(self.linear_grid)
                # step to the previous 1 lication, if the previous 1 is free to go
                possible_linear_grid[i] = 0 # mark the current as 0 since it left already
                possible_linear_grid[i-1] = self.linear_grid[i] # mark the previous 1 location as what the current grid is showing
                yield((i,i-1), LinearDiskMovement(possible_linear_grid))
                        
            # it might also have the need to go back 2 location
            if (i - 2) >= 0 and self.linear_grid[i] != 0 and self.linear_grid[i-1] != 0 and self.linear_grid[i-2] == 0:
                possible_linear_grid = copy.deepcopy(self.linear_grid)
                # step to the previous 2 lication, if the previous 1 is not free to go and the previous 2 location is free to go
                possible_linear_grid[i] = 0 # mark the current as 0 since it left already
                possible_linear_grid[i-2] = self.linear_grid[i] # mark the previous 1 location as what the current grid is showing
                yield((i,i-2), LinearDiskMovement(possible_linear_grid))



    # check if it's all moved to the right side
    def is_solved_for_identical_disk(self, length, n):
        
        # initialize an empty list to make it as the correct solution for comparision 
        correct_solution = []
        for i in range(length):
            correct_solution.append(0)

        # make the trialing ones all as 1
        for i in range(n):
            correct_solution[-(i+1)] = 1
        
        # return true if it matches, false if not
        if self.linear_grid == correct_solution:
            return True
        else:
            return False    
    
        

    def is_solved_for_distinct_disk(self, length, n):
        
        #initialize an empty list to make it as the correct solution for comparision 
        correct_solution = []
        for i in range(length):
            correct_solution.append(0)

        #make the trialing ones reversed
        for i in range(n):
            correct_solution[-(i+1)] = i + 1

        # return true if it matches, false if not        
        if self.linear_grid == correct_solution:
            return True
        else:
            return False    
    


# returns an optimal solution to the above problem as a list of moves, where
# length is the number of cells in the row and n is the number of disks. Each
# move in the solution should be a two-element tuple of the form (from,
# to) indicating a disk movement from the cell from to the cell to.
def solve_identical_disks(length, n):

    #initialize the linear grid
    linear_grid = []
    for i in range(length):
        if i < n:
            linear_grid.append(1) #since it's all identical, we'll use 1 as occupied position
        else:
            linear_grid.append(0) #use 0 as empty position

    #make it into a LinearDiskMovement object to use all the methods/functions
    linear_grid_object = LinearDiskMovement(linear_grid)

    # create and load all the visited movement
    visited = set()
    visited.add(tuple(linear_grid))

    #initialize the froniter to queue through, load the initial stage
    froniter = [([], linear_grid_object)]

    #check if it's a solution already
    if linear_grid_object.is_solved_for_identical_disk(length, n):
        return []
   
   # loop throught the queue to do BFS
    while froniter:
        #get the first/top in the queue
        movement, linear_grid = froniter.pop(0)
        for possible_move, possible_grid in linear_grid.successors_for_identical(length): #BFS
            current_movement = movement + [possible_move]
            # terminal statement, if there is the solution, then stop
            if possible_grid.is_solved_for_identical_disk(length, n):
                return current_movement
            # otherwise, add it to the visited and froniter queue
            else:
                linear_grid_set = tuple(possible_grid.get_linear_grid())
                if linear_grid_set not in visited:
                    visited.add(linear_grid_set)
                    froniter.append((current_movement, possible_grid))
    # return None if no solution found
    return None

def solve_distinct_disks(length, n):
    # basically follow the same logic as the identical one above
    # initalize the linear grid a bit differently
    
    linear_grid = []
    for i in range(length):
        if i < n:
            linear_grid.append(i+1) #since it's all diffent now, we'll name them from 1,2,3.... to be distinguished
        else:
            linear_grid.append(0) #use 0 as empty position

    #make it into a LinearDiskMovement object to use all the methods/functions
    linear_grid_object = LinearDiskMovement(linear_grid)

    # create and load all the visited movement
    visited = set()
    visited.add(tuple(linear_grid))

    #initialize the froniter to queue through, load the initial stage
    froniter = [([], linear_grid_object)]

    #check if it's a solution already
    if linear_grid_object.is_solved_for_distinct_disk(length, n):
        return []
   
   #loop throught the queue 
    while froniter:
        movement, linear_grid = froniter.pop(0)
        for possible_move, possible_grid in linear_grid.successors_for_differnt(length): # BFS
            current_movement = movement + [possible_move]
            # terminal statement, if there is the solution, then stop
            if possible_grid.is_solved_for_distinct_disk(length, n):
                return current_movement
            # otherwise, add it to the visited and froniter queue            
            else:
                linear_grid_set = tuple(possible_grid.get_linear_grid())
                if linear_grid_set not in visited:
                    visited.add(linear_grid_set)
                    froniter.append((current_movement, possible_grid))
    # return None if no solution found
    return None

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Maybe 40 hours...
"""

feedback_question_2 = """
The writing the DFS and BFS parts were the hardest and took most of the time, 
since I did petition for this course (I am taking 596 concurrently, rather than a preprequisite).
So I have to do a lot of Google search and learn how to write DFS and BFS myself first.
But it was VERY rewarding! Even though it was hard, I am so glad that I got this!!!
"""

feedback_question_3 = """
Again, like what I said in HW1, I REALLY LOVE how each little questions are built upon each other.
I can use the function/method that I built in the previous questions to be implemented in the next question
as a helper function. This is very logical and handy to proceed forward!
"""
