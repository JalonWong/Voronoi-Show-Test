import numpy as np
import random

PointColor = [0, 0, 0]
Points = []
MatrixWidth = 0
MatrixHeight = 0

# Euclidean distance
def getEuclidean(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2
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
DrawPointFunc = None

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
    minDist = Points[0].getDistance(x, y)
    ret = Points[0]
    
    for p in Points:    
        d = p.getDistance(x, y)
        if d < minDist:
            minDist = d
            ret = p
    
    return ret

def GenerateMatrix():
    if len(Points) == 0:
        return

    w = MatrixWidth
    h = MatrixHeight
    for i in range(w):
        for j in range(h):
            p = findNearestPoint(i, j)
            DrawPointFunc(i, j, p.color)

    for p in Points:
        DrawPointFunc(p.x, p.y, PointColor)

def ScanArea(pn, l, u, r, b):
    cnt = 0

    for i in range(l, r + 1):
        if i < 0 or i >= MatrixWidth:
            continue
        
        if b >= 0:
            p = findNearestPoint(i, b)
            if p is pn:
                DrawPointFunc(i, b, p.color)
                cnt += 1

        if u < MatrixHeight:
            p = findNearestPoint(i, u)
            if p is pn:
                DrawPointFunc(i, u, p.color)
                cnt += 1
        
    
    for j in range(b + 1, u):
        if j < 0 or j >= MatrixHeight:
            continue
        
        if l >= 0:
            p = findNearestPoint(l, j)
            if p is pn:
                DrawPointFunc(l, j, p.color)
                cnt += 1
        
        if r < MatrixWidth:
            p = findNearestPoint(r, j)
            if p is pn:
                DrawPointFunc(r, j, p.color)
                cnt += 1
    
    return (cnt != 0)

def UpdateMatrix():
    try:
        pn = Points[-1]
    except IndexError:
        return

    x = pn.x
    y = pn.y
    r = 1

    while ScanArea(pn, x - r, y + r, x + r, y - r):
        r += 1
    
    DrawPointFunc(pn.x, pn.y, PointColor)
        
def ClearPoints():
    Points.clear()

def AddPoint(x, y):
    if x < 0 or y < 0 or x >= MatrixWidth or y >= MatrixHeight:
        return
    
    Points.append(Point(x, y))

def AddRamdomPoints(n):
    for i in range(n):
        Points.append(Point( random.random() * MatrixWidth, random.random() * MatrixHeight))

def Init(w, h, drawPoint):
    global DrawPointFunc
    global MatrixWidth
    global MatrixHeight
    MatrixWidth = int(w)
    MatrixHeight = int(h)
    DrawPointFunc = drawPoint
