#Maze classes for Maze genpy
import random
from random import shuffle

class halls:


    #---------------------------------------------------------
    # False --> blocked
    # maze[0].append((True, False, False, True, True))
    #                 NORTH, EAST, SOUTH, WEST, was here
    #---------------------------------------------------------

    #Set init for the Maze
    def __init__(self):
        self.data = []

    #reseal the halls in the maze
    def seal_halls(self, width, height):
        self.data = [[[False, False, False, False, False] for y in range(height)] for x in range(width)]

    def open_doors(self, x, y, xx, yy):
        #outxxyy = "X Y:" + str(x) + " " + str(y) + "  XX YY:" + str(xx) + " " + str(yy)
        #sys.stdout.write(outxxyy)
        if xx == 1: #EAST
            self.data[x][y][1] = True
            self.data[x + xx][y][3] = True
            #print(" East")
        elif xx == -1: #WEST
            self.data[x][y][3] = True
            self.data[x + xx][y][1] = True
            #print(" West")
        elif yy == 1: #NORTH
            self.data[x][y][0] = True
            self.data[x][y + yy][2] = True
            #print(" North")
        elif yy == -1: #SOUTH
            self.data[x][y][2] = True
            self.data[x][y + yy][0] = True
            #print(" South")
            # For viewing the data set for maze

    def sealed_cell(self, cellx, celly, width, height):
        if cellx in range(width) and celly in range(height):
        # are all door closed?
            if any(self.data[cellx][celly]) == False:
                return "sealed"
            else:
                return "opened"
        else:
        #out of bounds are always sealed
            return "bounds"

    def solve(self, x, y, width, height):
        # directions for NORTH, EAST, SOUTH, WEST
        # F(n) = Goal
        # print("Start Solve", x, y, self.data[x][y][4])
        if x == (width - 1) and y == (height - 1):
            self.data[x][y][4] = True
            return True
        if self.sealed_cell(x, y, width, height) != "opened" or self.data[x][y][4] == True:
            return False
        self.data[x][y][4] = True  #Key entry, need to set breadcrumbs
        if self.data[x][y][0] == True and self.solve(x, y+1, width, height):
            return True
        if self.data[x][y][1] == True and self.solve(x+1, y, width, height):
            return True
        if self.data[x][y][2] == True and self.solve(x, y-1, width, height):
            return True
        if self.data[x][y][3] == True and self.solve(x-1, y, width, height):
            return True
        self.data[x][y][4] = False
        return False

    def build_maze(self, x, y, width, height):
        # directions for NORTH, EAST, SOUTH, WEST
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(directions)
        for (xx, yy) in directions:
            #print("Cell x y:",x ,y,"  Added directions to x y:", x + xx, y + yy, "Limits ", width, height)
            tested = self.sealed_cell(x + xx, y + yy, width, height)
            if tested == "sealed":
                self.open_doors(x, y, xx, yy)
                #print_val()
                #print("Good Cell:",x ,y, "Direction", xx, yy, "Added directions", x + xx, y + yy, " result:", tested, " Num: ", num )
                self.build_maze(x + xx, y + yy, width, height)
