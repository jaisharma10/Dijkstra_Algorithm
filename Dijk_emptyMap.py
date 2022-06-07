## ------------------------------------------------------------------------------------------
#                                  Depth First Search [Empty Map]
## ------------------------------------------------------------------------------------------

'''
Author: Jai Sharma
Task: implement Depth First Search [DFS] algorithm on an empty 10 x 10 map 
        between a given start and goal node
        
--> Path is visualized using pygame. 
    - Start Node is Red
    - Goal Node is Green
    - Solution Path is in Blue/Yellow
    - Explored Nodes are in White
    
--> 4 action steps. Search Sequence 
    1. Up
    2. Right
    3. Down
    4. Left
    
--> Heapq: In Queue, the oldest element is dequeued first. While, in Priority Queue, 
    an element based on the highest priority is dequeued.

--> Dijkstra uses f = g, total node cost = distance to start node. No heuristic.
'''

## ------------------------------------------------------------------------------------------
#                                        Import Libraries
## ------------------------------------------------------------------------------------------

import time
import copy
from collections import deque
import pygame
import sys
import numpy as np

start_time = time.time()
print("=======================================================================")

## ------------------------------------------------------------------------------------------
#                                     Node Class
## ------------------------------------------------------------------------------------------

class Node:
    
    '''
    Attributes:
        state: state of the node
        parent: parent of the node
        c2c: total cost to come
    '''
    
    def __init__(self, state, parent, c2c):
        self.state = state     # current node in the tree
        self.parent = parent   # parent of current node
        self.c2c = c2c   # parent of current node
        
    def __repr__(self):         # special method used to represent a class’s objects as string
        return(f' state: {self.state}, cost: {self.c2c} ')
    
    def moveUp(self, pos): # Swap node with the node Above
        row, col = pos[0], pos[1]
        if col < 10:  # node above exists
            upNode = Node(copy.deepcopy(self.state), Node(self.state, self.parent, self.c2c), self.c2c + 1)  # parent is also a Node in form (state, parent)
            upNode.state[0], upNode.state[1]  = row, col + 1
            return(upNode)    # Up is possible
        else:
            return(False)       # Up not possible
    
    def moveDown(self, pos): # Swap node with the node Below
        row, col = pos[0], pos[1]
        if col > 1:  # node below exists
            downNode = Node(copy.deepcopy(self.state), Node(self.state, self.parent, self.c2c), self.c2c + 1) 
            downNode.state[0], downNode.state[1]  = row, col - 1
            return(downNode)    # Down is possible         
        else:
            return(False)       # Down not possible

    def moveLeft(self, pos): # Swap node with the node on Left
        row, col = pos[0], pos[1]
        if row > 1:  # node to right exists
            leftNode = Node(copy.deepcopy(self.state), Node(self.state, self.parent, self.c2c), self.c2c + 1)  
            leftNode.state[0], leftNode.state[1]  = row - 1, col
            return(leftNode)    # Left is possible
        else:       
            return(False)       # Left not possible

    def moveRight(self, pos): # Swap node with the node on Right
        row, col = pos[0], pos[1]
        if row < 10: # node to left exists
            rightNode = Node(copy.deepcopy(self.state), Node(self.state, self.parent, self.c2c), self.c2c + 1)  
            rightNode.state[0], rightNode.state[1]  = row + 1, col
            return(rightNode)    # Right is possible         
        else:
            return(False)       # Right not possible

    def moveUpRight(self, pos): # Swap node with the node on Right
        row, col = pos[0], pos[1]
        if row < 10 and col < 10: # node to left exists
            uprightNode = Node(copy.deepcopy(self.state), Node(self.state, self.parent, self.c2c), self.c2c + 1.4)  
            uprightNode.state[0], uprightNode.state[1]  = row + 1, col + 1
            return(uprightNode)    # Right is possible         
        else:
            return(False)       # Right not possible
   
    def getNeighbours(self, pos): # check for neighbours in the 4 directions
        neighbours = []
        up = self.moveUp(pos) 
        down = self.moveDown(pos) 
        left = self.moveLeft(pos) 
        right = self. moveRight(pos) 
        upRight = self. moveUpRight(pos) 

        neighbours.append(up) if up else None
        neighbours.append(right) if right else None
        neighbours.append(down) if down else None
        neighbours.append(left) if left else None
        neighbours.append(upRight) if upRight else None

        return(neighbours)
        
## ------------------------------------------------------------------------------------------
#                                         Dijkstra Function
## ------------------------------------------------------------------------------------------

def dijkstra(s, g):
    
    pygame.init()
    magf = 50 # magnification factor
    screen = pygame.display.set_mode(((13)*magf, (13)*magf))
    screen.fill((30,30,30))
    
    startNode = Node(s, None, 0)
    goalNode = Node(g, None, float('inf'))

    queue = []                    # all neighbour states to explore
    visited = []                  # all visited lists fall here
    queue.append(startNode)       # add start node to queue
    visited.append(startNode.state)
    
    while queue != []:
        # print("===========================================")
        # print("queue",queue)
        queue.sort(key = lambda x: x.c2c)                # sort queue based on c2c
        currentNode = queue.pop(0)                        # pop node with lowest cost 
        # print("currentNode:", currentNode.state)
        # print("visited:", visited)

        pygame.draw.circle(screen, (0,128,0), (magf*(1 + goalNode.state[0]), 12*magf-magf*goalNode.state[1]), 16)   # Goal Node
        pygame.draw.circle(screen, (255,0,0), (magf*(1 + startNode.state[0]), 12*magf-magf*startNode.state[1]), 16) # Start Node
        pygame.draw.circle(screen, (255,255,255), (magf*(1 + currentNode.state[0]), 12*magf-magf*currentNode.state[1]), 9)   # Current Node
        pygame.display.update()
        
        # Case 1 --> Goal Reached
        if currentNode.state == goalNode.state:  # check if goal state reached
            print("Goal Reached !") 
            backTrackList = backtrack(currentNode, startNode)  # backtrack list is goal to start
            reversed_backTrackList = backTrackList[::-1] # reversed --> list is start to goal
            prev = reversed_backTrackList[0]
            print("backTrackList", backTrackList)
            for route in reversed_backTrackList:   # visualize the search algorithm
                pygame.draw.circle(screen, (0,0,250), (magf*(1 + route[0]), 12*magf-magf*route[1]), 7)   # Current Node     
                pygame.draw.line(screen, (255, 255, 0), (magf*(1 + route[0]), 12*magf-magf*route[1]), (magf*(1 + prev[0]), 12*magf-magf*prev[1]),5)
                pygame.draw.circle(screen, (0,0,250), (magf*(1 + prev[0]), 12*magf-magf*prev[1]), 7)   # Current Node     
                pygame.display.update()
                prev = route
            time.sleep(2)
            print("Cost to reach Goal Node -->", round(currentNode.c2c, 3))
            break

        # Case 2: goal not reached, evaluate neighbours to the queue 
        else: 
            Neighbours = currentNode.getNeighbours(currentNode.state)  # get neighbours of current node
            # print("Neighbours", Neighbours) 
            for child in Neighbours:

                # Case2A: previosly explored, update if needed
                # print("child", child)

                if child.state in visited:
                    # print("B")
                    if child.parent != currentNode.state:
                        parentNode = child.parent     
                        if child.c2c > parentNode.c2c + 1: # update node if needed
                            child.c2c = parentNode.c2c + 1
                     
                # Case2B: add to queue, previosly not explored
                else:
                    queue.append(child)
                    visited.append(child.state)   
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
    return(None)
        
        
## ------------------------------------------------------------------------------------------
#                                  Backtracking Function
## ------------------------------------------------------------------------------------------

def backtrack(current, start):
    backtrackList = [current.state]   # new list to collect backtracked list
    while(current.state != start.state):
        current = current.parent
        backtrackList.append(current.state)
    return(backtrackList)
        
## ------------------------------------------------------------------------------------------
#                                       Main Function
## ------------------------------------------------------------------------------------------

if __name__== "__main__":
    
    s = [1,1] # Start State
    g = [10,6] # Goal State

    # Map Size is set as:
    mapWidth = 10
    mapHeight = 10
    
    # Build a Map
    mapCord = []
    for x in range(1, mapWidth + 1, 1):
        for y in range(1, mapHeight + 1,1):
            mapCord.append([x,y])

    # checks if inputs are Valid
    if s not in mapCord:
        print("Start Node outside Map")
    elif g not in mapCord:
        print("Goal Node outside Map")
    elif s == g: # Check if start node is goal node
        print("Start node is Goal Node!!")
    else: 
        print("Implementing Dijkstra Search")
        print("===============================================================================================")
        dijkstra(s, g)
    
## ------------------------------------------------------------------------------------------
#                                Display --> Forward and Backward Path
## ------------------------------------------------------------------------------------------

end_time = time.time()

print("===============================================================================================")
print("Time to Find Solution Path", round((end_time - start_time), 3), "seconds")
print("===============================================================================================")

print('\n')
