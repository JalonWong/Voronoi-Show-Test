import numpy as np
import random

# Make a matrix with all zeros and increasing elements on the diagonal
PointColor = [0, 0, 0]
Points = []
MatrixSize = 0

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.color = [random.random(), random.random(), random.random()]

    def getChebyshev(self, x, y):
        if abs(self.x - x) > abs(self.y - y):
            return abs(self.x - x)
        else:
            return abs(self.y - y)
    
    def getDistance(self, x, y):
        return self.getChebyshev(int(x), int(y))


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