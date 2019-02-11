from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import VoronoiPoint as vp

WW = 0
WH = 0
WOffsetX = 0
WOffsetY = 0
MatrixSize = 128.0
LastColor = [0, 0, 0]
RefreshFlag = False

def drwaPoint(x, y, color):
    global LastColor

    if LastColor != color:
        glColor3fv(color)
        LastColor = color
    
    glVertex2i(x, y)

def drawFunc():
    global RefreshFlag

    # glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    if RefreshFlag:
        RefreshFlag = False
        vp.GenerateMatrix()
    else:
        vp.UpdateMatrix()
    
    glEnd()
    glFlush()

def reshape(w, h):
    global WW
    global WH
    global WOffsetX
    global WOffsetY

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    size = MatrixSize
    WW = w
    WH = h

    if w <= h:
        WOffsetX = 0
        WOffsetY = ((size * h / w - size) / 2)
        gluOrtho2D(-1, size, -1 - WOffsetY, size + WOffsetY)
        glPointSize(float(w) / size + 1)
    else:
        WOffsetY = 0
        WOffsetX = ((size * w / h - size) / 2)
        gluOrtho2D(-1 - WOffsetX, size + WOffsetX, -1, size)
        glPointSize(float(h) / size + 1)

    global RefreshFlag
    RefreshFlag = True


def ConverToMatrixCoordinate(x, y):
    x = x * (MatrixSize + WOffsetX * 2) / WW - WOffsetX
    y = (WH - y) * (MatrixSize + WOffsetY * 2) / WH - WOffsetY
    return int(x), int(y)

def mouse(button, state, x, y):
    # print(button)
    # print(state)
    # print(x)
    # print(y)
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:
            # print('x1: {}, y1: {}'.format(x, y))
            x, y = ConverToMatrixCoordinate(x, y)
            vp.AddPoint(x, y)
            glutPostRedisplay()


def keyboard(key, x, y):
    k = ord(key)
    if k == 27 or k == ord('q'):  # Esc is 27
        sys.exit(0)
    elif k == ord('c'):
        vp.ClearPoints()
        glClear(GL_COLOR_BUFFER_BIT)
        glutPostRedisplay()
    elif k == ord('1') or k == ord('2') or k == ord('3'):
        vp.ChangeDistanceFunc(k - ord('0'))
        global RefreshFlag
        RefreshFlag = True
        glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glShadeModel(GL_FLAT)
    glClear(GL_COLOR_BUFFER_BIT)
    

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(400, 400)
glutCreateWindow("Voronoi")
vp.Init(MatrixSize, MatrixSize, drwaPoint)
init()
glutDisplayFunc(drawFunc)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
# glutIdleFunc(drawFunc)
glutMainLoop()
