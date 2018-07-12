#!/usr/bin/python3 -tt

#Maze Generator

import sys, pygame, os
from pygame.locals import *
from Maze_class import halls
#import pdb
import random
from random import randrange, randint

#Globals
#base maze 0 elemets

col = 0
row = 0
black = (  0,   0,   0)
white = (255, 255, 255)
yellow =(255, 255,   0)
# there if needed
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def draw_maze(screen, maze1, size, col, row):
    #Block size
    blocksz = ((size[0] / (col * 2 + 1)), (size[1] / (row * 2 + 1)))
    #solve block size
    solvesz = (blocksz[0]/2, blocksz[1]/2)
    solveoffset = (solvesz[0]/2, solvesz[1]/2)
    #boarder around the maze
    #Top boarder
    pygame.draw.rect(screen, white, [0, 0, (blocksz[0] * (col * 2 + 2)), blocksz[1]])
    #Left boarder
    pygame.draw.rect(screen, white, [0, 0, blocksz[0], (blocksz[1] * (row * 2 + 2))])
    #Bottom boarder
    pygame.draw.rect(screen, white, [0, blocksz[1] * (row * 2), blocksz[0] * (col * 2 + 1), blocksz[1] * (row * 2 + 2)])
    #right boarder
    pygame.draw.rect(screen, white, [blocksz[0] * (col * 2), 0, blocksz[0] * (col * 2 + 1), blocksz[1] * (row * 2 + 1)])
    #Draw the cells
    for y in range(row):
        yy = (row - 1) - y
        for x in range(col):      # [ [(T, T, T, T) ...][() () () () () ][][][][]  ]
            if (x + 1) < col and (y + 1) < row:  #Central Blocks
                centerblk = (((x * 2 + 1)*blocksz[0]) + blocksz[0],((y * 2 + 1)*blocksz[1]) + blocksz[1])
                pygame.draw.rect(screen, white, [centerblk[0], centerblk[1], blocksz[0]+1, blocksz[1]+1])
            if maze1.data[x][y][1] == False and (x + 1) < col:  #If there is a EAST blocked
                eastgate = (((x * 2 + 2) * blocksz[0]),((yy * 2 + 1) * blocksz[1]))
                pygame.draw.rect(screen, white, [eastgate[0], eastgate[1], blocksz[0]+1, blocksz[1]+1])
            if maze1.data[x][y][2] == False and (yy + 1) < row:  #If there is a SOUTH blocked
                southgate = (((x * 2 + 1) * blocksz[0]),((yy * 2 + 2) * blocksz[1]))
                pygame.draw.rect(screen, white, [southgate[0], southgate[1], blocksz[0]+1, blocksz[1]+1])
            if maze1.data[x][yy][4]:
                #if solver path then draw path inite yellow
                solveoffset = (((x * 2 + 1) * blocksz[0]) + (solvesz[0] / 2), ((y * 2 + 1) * blocksz[1]) + (solvesz[1] / 2))
                pygame.draw.rect(screen, yellow, [solveoffset[0], solveoffset[1], solvesz[0], solvesz[1]])

# This resets the maze creating a new pattern method calls for the insatnce maze1
def makemaze(maze1, col, row):
    maze1.seal_halls(col, row)
    maze1.build_maze(0, 0, col, row)
    maze1.solve(0, 0, col, row)


#standard out for main function
def main():
    #create new instance of halls
    maze1 = halls()
    random.seed()
    #size of graphic window
    size = (800, 600)
    if len(sys.argv) == 3:
        colwidth = int(str(sys.argv[1]))
        rowheight = int(str(sys.argv[2]))
        if (colwidth < 2 or colwidth > 40) or (rowheight < 2 or rowheight > 40):
            print("Both values need to greater than 2 and less then 40.\n")
            sys.exit(1)
    else:
        #if no input then use 10 as default size
        colwidth = rowheight = 10


    #initalize pygame screen
    pygame.init()
    backscreen = pygame.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
    #set current size of the display as the starting size
    backscreen.fill(black)
    backscreen.blit(backscreen, (0,0))

    #inital maze and graphical output of maze and inital display
    makemaze(maze1, colwidth, rowheight)
    draw_maze(backscreen, maze1, size, colwidth, rowheight)
    pygame.display.flip()

    #Do main loop untill quit event
    while True:
        mouse = cursor = space = False
        pygame.event.pump()
        #event = pygame.event.wait()
        #get input
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                or (event.type == KEYDOWN and event.key == K_ESCAPE) \
                or (event.type == KEYDOWN and event.key == K_q):
                    sys.exit()
            #If window resize event, set new window size
            #Very finiky setup, sometimes it works, sometimes not
            elif event.type == VIDEORESIZE:
                size = event.size
                backscreen = pygame.display.set_mode(size, HWSURFACE | DOUBLEBUF | RESIZABLE)
                draw_maze(backscreen, maze1, size, colwidth, rowheight)
            #If keyboard press then parse what key
            elif (event.type == KEYDOWN):
                if (event.key == K_SPACE):
                    space = True
                # if cursor key is pressed then add or remove one (1) from a maze size
                elif (event.key == K_RIGHT):
                    if (colwidth < 40): colwidth += 1
                    cursor = True
                elif (event.key == K_UP):
                    if (rowheight < 40): rowheight += 1
                    cursor = True
                elif (event.key == K_LEFT):
                    if (colwidth > 3):colwidth -= 1
                    cursor = True
                elif (event.key == K_DOWN):
                    if (rowheight > 3): rowheight -= 1
                    cursor = True
                # if either cursor key or space pressed
                if space or cursor:
                    #print("screen, col-row :", size, colwidth, rowheight)
                    # change formating on maze to new
                    backscreen.fill(black)
                    makemaze(maze1, colwidth, rowheight)
                    # Graphical output of maze
                    draw_maze(backscreen, maze1, size, colwidth, rowheight)
                    cursor = space = False

# This is the standard boiler plate call for main
if __name__=='__main__':
        main()
