from math import pi , acos , sin , cos
import pickle
from time import time
from tkinter import *
from heapq import *

frame = Tk()
canvas = Canvas(frame, bg="black", height=700, width=800)

class Graph:
    def __init__(self, g, dist, cities):
        self.graph = g
        self.distance = dist
        self.cities = cities

    def getDist(self):
        return self.distance

    def getCities(self):
        return self.cities

    def getNeighbours(self, node):
        return list(self.graph[node].keys())

    def getLongLat(self, node):
        return self.distance[node]

    def getEdgeLength(self,v1,v2):
        d = self.graph[v1]
        return d[v2]

    def get(self, node):
        return self.graph[node]

    def getCoords(self, node):
        return self.distance[node]

def calcd(y1,x1,y2,x2):
   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)

   R   = 3958.76


   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   rounded = (round( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1), 15))
   #return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R
   return acos(rounded) * R

def genGraph():
    dist = {}
    graph = {}
    CITIES = {}
    edges = open("rrEdges.txt", "r")
    nodes = open("rrNodes.txt", "r")
    cities = open("rrNodesCity.txt", "r")

    for l in cities:
        arr = l.split(" ")
        CITIES[arr[0]] = l[8:].strip()

    for l in nodes:
        arr = l.split(" ")
        key = arr[0]
        if (key in CITIES):
            key = CITIES[key]
        dist[key] = (arr[1], arr[2].strip())

    for l in edges:
        arr = l.split(" ")
        key = arr[0]
        val = arr[1].strip()
        if (key in CITIES):
            key = CITIES[key]

        if (val in CITIES):
            val = CITIES[val]

        addD = graph.get(key, {}) #Add Key
        x,y = dist[key]
        x1, y1 = dist[val]
        calculated =  calcd(x,y,x1,y1)
        addD[val] = calculated
        graph[key] = addD

        addD = graph.get(val, {}) #Add Value
        addD[key] = calculated
        graph[val] = addD


    finalGraph = Graph(graph, dist, CITIES)
    pickle.dump(finalGraph, open("graph.p", "wb"))

def astar(start, end, graph):
    node = start
    visited = set()
    q = []
    p = []

    gone = {}

    p.append(node)
    heappush(q, (0, 0, 0, p))
    x2,y2 = graph.getLongLat(end)


    while (len(q) > 0):
        f, h, g , path = heappop(q)
        current = path[-1]
        if current == end:
            return (gone,path, f)

        temp = gone.get(current, [])
        temp = path
        gone[current] = temp

        if current not in visited:
            visited.add(current)
            for x in graph.getNeighbours(current):
                if x not in visited:
                    newPath = path.copy()
                    newPath.append(x)
                    hnew = h + (graph.getEdgeLength(current, x))
                    x1, y1 = graph.getLongLat(x)
                    gnew = calcd(x1,y1,x2,y2)
                    f = hnew + gnew
                    heappush(q, (f, hnew,gnew, newPath))

def pixelate(tuple):
    x1, x2, y1, y2 = tuple
    x1 = (float(x1) * 15 * -1) + 900
    x2 = (float(x2) * 15 * -1) + 900
    y1 = ((float(y1) + 130)) * 12
    y2 = ((float(y2) + 130)) * 12
    return (x1, x2, y1, y2)

def astarAnimated(start, end, graph):
    node = start
    visited = set()
    drawUS(graph.getDist(), graph.getCities())
    canvas.pack()

    q = []
    p = []
    up = 0
    p.append(node)
    heappush(q, (0, 0, 0, p))
    x2,y2 = graph.getLongLat(end)

    while (len(q) > 0):
        up = 0
        f, h, g , path = heappop(q)
        current = path[-1]
        if current == end:
            for x in range(0,len(path) - 1):
                one = path[x]
                two = path[x + 1]
                xOne, yOne = graph.getLongLat(one)
                xTwo, yTwo = graph.getLongLat(two)
                xOne, xTwo, yOne, yTwo = pixelate((xOne, xTwo, yOne, yTwo))
                canvas.create_line(yOne, xOne, yTwo, xTwo, fill="springGreen", width="0.7m")

            for x in range(0, len(q)):
                a,b,c, path = heappop(q)
                one = path[-1]
                two = path[-2]
                xOne, yOne = graph.getLongLat(one)
                xTwo, yTwo = graph.getLongLat(two)
                xOne, xTwo, yOne, yTwo = pixelate((xOne, xTwo, yOne, yTwo))
                canvas.create_line(yOne, xOne, yTwo, xTwo, fill = "white")
            return (path, f)

        if current not in visited:
            visited.add(current)
            for x in graph.getNeighbours(current):
                if x not in visited:
                    newPath = path.copy()
                    newPath.append(x)
                    hnew = h + (graph.getEdgeLength(current, x))
                    x1, y1 = graph.getLongLat(x)
                    gnew = calcd(x1,y1,x2,y2)
                    f = hnew + gnew
                    heappush(q, (f, hnew,gnew, newPath))

                    #Animation of visited
                    xTwo,yTwo = graph.getLongLat(current)
                    x1, xTwo, y1, yTwo = pixelate((x1, xTwo, y1, yTwo))
                    canvas.create_line(y1,x1,yTwo,xTwo, fill = "SteelBlue")
                    canvas.pack()
    frame.mainloop()
def drawUS(dist, cities):
    edges = open("rrEdges.txt", "r")
    for l in edges:
        arr = l.split(" ")
        one = arr[0]
        two = arr[1].strip()
        if (one in cities):
            one  = cities[one]
        if (two in cities):
            two = cities[two]

        x1, y1 = dist[one]
        x2, y2 = dist[two]
        x1,x2,y1,y2 = pixelate((x1,x2,y1,y2))
        canvas.create_line(y1, x1, y2, x2, fill = "gray")
        canvas.pack()

#Draws Path, USA, Visited, Uses local tkinter
def drawAfter(dist, cities, path, visited):
    edges = open("rrEdges.txt", "r")
    canvas.pack()
    #Drawing USA
    for l in edges:
        arr = l.split(" ")
        one = arr[0]
        two = arr[1].strip()
        if (one in cities):
            one  = cities[one]
        if (two in cities):
            two = cities[two]

        xOne, yOne = dist[one]
        xTwo, yTwo = dist[two]
        xOne = (float(xOne) * 15 * -1) + 900
        xTwo = (float(xTwo) * 15 * -1) + 900
        yOne = ((float(yOne) + 130)) * 12
        yTwo = ((float(yTwo) + 130)) * 12

        canvas.create_line(yOne, xOne, yTwo, xTwo, fill = "white")

    canvas.pack()

    #Drawing Path
    for x in range (0, len(path) - 1):
        one = path[x]
        two = path[x + 1]
        if (one in cities):
            one = cities[one]
        if (two in cities):
            two = cities[two]

        xOne, yOne = dist[one]
        xTwo, yTwo = dist[two]
        xOne, xTwo, yOne, yTwo = pixelate((xOne,xTwo,yOne, yTwo))
        canvas.create_line(yOne, xOne, yTwo, xTwo, fill = "red", width = "0.7m")

    canvas.pack()

    #Drawing Visited
    for a in visited.keys():
        y = visited[a]
        for x in range (0, len(y) - 1):
            one = y[x]
            two = y[x + 1]
            if (one in cities):
                one = cities[one]
            if (two in cities):
                two = cities[two]

            xOne, yOne = dist[one]
            xTwo, yTwo = dist[two]
            xOne, xTwo, yOne, yTwo = pixelate((xOne, xTwo, yOne, yTwo))
            canvas.create_line(yOne, xOne, yTwo, xTwo, fill = "green")

    print("Done " + str(len(visited)))
    canvas.pack()
    frame.mainloop()

def main():
    start = input("Enter start city: ")
    end = input("Enter end city: ")
    graph = pickle.load(open("graph.p", "rb"))

    t0 =time()
    gone, path, dist = (astar(start.strip(), end.strip(), graph))
    print("Total Distance between " + start + " and " +  end + " is " + str(dist) + "KM")
    t1 = time()
    print("Time " + str(t1 - t0))

    astarAnimated(start.strip(), end.strip(), graph)
    #print("Total Distance between " + start + " and " +  end + " is " + str(dist) + "KM")
    canvas.update()
    frame.mainloop()


main()