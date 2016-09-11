import random

import pygame
import math
from math import *
from pygame import gfxdraw


def boundsColor(color):
    r, g, b, a = color
    r = max(min(255, r), 0)
    g = max(min(255, g), 0)
    b = max(min(255, b), 0)
    a = max(min(255, a), 0)
    return (r, g, b, a)


def almostEqual(x, y):
    return abs(x - y) < 10 ** -5


def drawAntiAliasedPolygon(surface, color, points):
    pygame.draw.polygon(surface, color, points)
    # pygame.gfxdraw.aapolygon(surface,points,color)
    # pygame.gfxdraw.filled_polygon(surface,points,color)


def randfloat(x, y):
    ran = abs(x - y)
    minn = min(x, y)
    return random.random() * ran + minn


# from stackoverflow and pygame http://www.pygame.org/docs/ref/gfxdraw.html
# http://stackoverflow.com/questions/30578068/pygame-draw-anti-aliased-thick-line
def drawAntiAliasedLine(surface, color_L1, X0, X1, thickness):
    length = ((X1[0] - X0[0]) ** 2 + (X1[1] - X0[1]) ** 2) ** 0.5
    center_L1 = ((X0[0] + X1[0]) / 2, (X0[1] + X1[1]) / 2)
    angle = math.atan2(X0[1] - X1[1], X0[0] - X1[0])
    UL = (center_L1[0] + (length / 2.) * cos(angle) - (thickness / 2.) * sin(angle),
          center_L1[1] + (thickness / 2.) * cos(angle) + (length / 2.) * sin(angle))
    UR = (center_L1[0] - (length / 2.) * cos(angle) - (thickness / 2.) * sin(angle),
          center_L1[1] + (thickness / 2.) * cos(angle) - (length / 2.) * sin(angle))
    BL = (center_L1[0] + (length / 2.) * cos(angle) + (thickness / 2.) * sin(angle),
          center_L1[1] - (thickness / 2.) * cos(angle) + (length / 2.) * sin(angle))
    BR = (center_L1[0] - (length / 2.) * cos(angle) + (thickness / 2.) * sin(angle),
          center_L1[1] - (thickness / 2.) * cos(angle) - (length / 2.) * sin(angle))
    pygame.gfxdraw.aapolygon(surface, (UL, UR, BR, BL), color_L1)
    pygame.gfxdraw.filled_polygon(surface, (UL, UR, BR, BL), color_L1)
