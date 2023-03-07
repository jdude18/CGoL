"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from prettytable import PrettyTable 
import datetime


inputFile = "input/input.in"

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid,output, height,width):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    # TODO: Implement the rules of Conway's Game of Life
    for i in range(height):
        for j in range(width):
            # compute 8-neighbor sum
            # using toroidal boundary conditions so when the grid ends it continues in the other side
            # ssimulation in toroidal surface
            total = int((grid[i, (j-1)%width] + grid[i, (j+1)%width] +
                         grid[(i-1)%height, j] + grid[(i+1)%height, j] +
                         grid[(i-1)%height, (j-1)%width] + grid[(i-1)%height, (j+1)%width] +
                         grid[(i+1)%height, (j-1)%width] + grid[(i+1)%height, (j+1)%width])/255)
            # Conway's game of life rules
            if grid[i, j]  == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    countEntities(grid,output,frameNum)                
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def countEntities(grid,output,frameNum):
    # Make a dictionary that will keep track of the entities counted
    entityCounts = {
        "Block": 0,
        "Beehive": 0,
        "Loaf": 0,
        "Boat": 0,
        "Tub": 0,
        "Blinker": 0,
        "Toad": 0,
        "Beacon": 0,
        "Glider": 0,
        "Lightweight spaceship": 0
    }
    
    # Count entities iterating through the grid with cycles
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if i < len(grid)-1 and j < len(grid[0])-1:
                if grid[i][j] == ON and grid[i+1][j] == ON and grid[i][j+1] == ON and grid[i+1][j+1] == ON:
                    entityCounts["Block"] += 1
                elif i < len(grid)-2 and j < len(grid[0])-2:
                    if grid[i][j+1] == ON and grid[i+1][j] == ON and grid[i+2][j] == ON and grid[i+3][j+1] == ON and grid[i+1][j+2] == ON and grid[i+2][j+2] == ON:
                        entityCounts["Beehive"] += 1
                    elif grid[i][j+1] == ON and grid[i+1][j] == ON and grid[i+2][j] == ON and grid[i+1][j+2] == ON and grid[i+2][j+3] == ON and grid[i+3][j+1] == ON and grid[i+3][j+2] == ON:
                        entityCounts["Loaf"] += 1
                if i < len(grid)-2 and j < len(grid[0])-2:
                    if grid[i][j] == ON and grid[i][j+1] == ON and grid[i+1][j] == ON and grid[i+2][j+1] == ON and grid[i+1][j+2] == ON:
                        entityCounts["Boat"] += 1
                    elif grid[i+1][j+1] == ON and grid[i+1][j+2] == ON and grid[i+2][j+1] == ON and grid[i+2][j+3] == ON and grid[i+3][j+2] == ON:
                        entityCounts["Tub"] += 1
                if j < len(grid[0])-2:
                    if grid[i][j] == ON and grid[i][j+1] == ON and grid[i][j+2] == ON:
                        entityCounts["Blinker"] += 1
                    elif j < len(grid[0])-3:
                        if grid[i][j] == ON and grid[i][j+1] == ON and grid[i][j+2] == ON and grid[i+1][j-1] == ON and grid[i+1][j+3] == ON and grid[i+2][j-1] == ON and grid[i+2][j+3] == ON and grid[i+3][j] == ON and grid[i+3][j+2] == ON:
                            entityCounts["Toad"] += 1

    #create table
    table = PrettyTable()
    table.field_names = ["", "Count", "Percent"]
    #get total
    total = 0
    for item in entityCounts.items():
        total+=item[1]
    fakeTotal = max(1,total)
    #insert data in table
    for item in entityCounts.items():
        table.add_row([item[0],item[1],int(item[1]/fakeTotal*100)])
    table.add_row(["Total",total,100])
    #insert data in file
    output.write(f"Iteration: {frameNum+1}\n")
    output.write(f"{table}\n\n")
    print(table)

    
    # x.add_row(["Adelaide", 1295, 1158259, 600.5])
    # print (entityCounts)        
# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments
    
    # set animation update interval
    updateInterval = 50

    # declare grid
    grid = np.array([])
    neighbor = np.array([])
    # populate grid with random on/off - more off than on
    #grid = randomGrid(N)
    # Uncomment lines to see the "glider" demo
    #grid = np.zeros(N*N).reshape(N, N)
    #addGlider(1, 1, grid)
    f = open(inputFile, "r")
    lines = f.readlines()

    width, heigth = map(int,lines[0].split())


    generations = int(lines[1])
    grid = np.zeros((width,heigth))
    neighbor = np.zeros((width,heigth))
    for line in lines[2:]:
        i, j = line.split()
        i, j = int(i), int(j)
        grid[i, j] = ON

    #open file
    output = open(r"output.out","w")
    output.write(f"Simulation at {datetime.date.today()}\n")
    output.write(f"universe size {width}x{heigth}\n\n")
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid,output, heigth,width),frames = generations,interval=updateInterval,repeat = False)

    plt.show()

# call main
if __name__ == '__main__':
    main()