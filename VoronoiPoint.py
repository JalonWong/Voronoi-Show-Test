import numpy as np
import random

# Make a matrix with all zeros and increasing elements on the diagonal
PointColor = [0, 0, 0]
Points = []
MatrixSize = 0

# Euclidean distance
def getEuclidean(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2
    # omit square root to decrease computation (it's monotonic function)


# Chebyshev distance
def getChebyshev(x1, y1, x2, y2):
    a = abs(x1 - x2)
    b = abs(y1 - y2)

    return max(a, b)


# Manhattan distance
def getManhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

DistanceFunc = getEuclidean

def ChangeDistanceFunc(n):
    global DistanceFunc

    if n == 1:
        DistanceFunc = getEuclidean
    elif n == 2:
        DistanceFunc = getChebyshev
    else:
        DistanceFunc = getManhattan

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.color = [random.random(), random.random(), random.random()]
    
    def getDistance(self, x, y):
        return DistanceFunc(self.x, self.y, int(x), int(y))


def findNearestPoint(x, y):
    min_dist = Points[0].getDistance(x, y)
    ret = Points[0]
    
    for p in Points:    
        d = p.getDistance(x, y)
        if d < min_dist:
            min_dist = d
            ret = p
    
    return ret

def GenerateMatrix(drawPoint):
    if len(Points) == 0:
        return

    w = MatrixSize
    h = MatrixSize
    for i in range(w):
        for j in range(h):
            p = findNearestPoint(i, j)
            drawPoint(i, j, p.color)

    for p in Points:
        drawPoint(p.x, p.y, PointColor)

def VerticalScan(pn, i, h, drawPoint):
    for j in range(pn.y, h):
        p = findNearestPoint(i, j)
        if p is pn:
            drawPoint(i, j, p.color)
    
    for j in range(pn.y, -1, -1):
        p = findNearestPoint(i, j)
        if p is pn:
            drawPoint(i, j, p.color)

def UpdateMatrix(drawPoint):
    if len(Points) == 0:
        return

    pn = Points[-1]
    
    w = MatrixSize
    h = MatrixSize
    for i in range(pn.x, w):
        VerticalScan(pn, i, h, drawPoint)
    
    for i in range(pn.x, -1, -1):
        VerticalScan(pn, i, h, drawPoint)
    
    drawPoint(pn.x, pn.y, PointColor)

def GetNewColor():
    if len(Points) == 0:
        return PointColor
        
    return Points[-1].color
        
def ClearPoints():
    Points.clear()

def AddPoint(x, y):
    if x < 0 or y < 0 or x >= MatrixSize or y >= MatrixSize:
        return
    
    Points.append(Point(x, y))

def AddRamdomPoints(n):
    for i in range(n):
        Points.append(Point( random.random() * 100, random.random() * 100))

def Init(size):
    global MatrixSize
    MatrixSize = int(size)