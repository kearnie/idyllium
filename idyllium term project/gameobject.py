'''
GameObject.py

implements the base GameObject class, which defines the wraparound motion
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''

# modified from Lukas http://blog.lukasperaza.com/getting-started-with-pygame/
# removed parts i don't need and added interaction
import pygame

from interaction import Interactable


class GameObject(Interactable):
    def __init__(self, x, y, width, height, radius=1):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.radius = x, y, radius
        try:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        except:
            print(width, height)
        self.image = self.image.convert_alpha()
        self.baseImage = self.image.copy()  # non-rotated version of image
        w, h = self.image.get_size()
        self.updateRect()
        self.velocity = (0, 0)
        self.angle = 0
        self.dirty = True
        self.lastDrawnAngle = 0

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def update(self, screenWidth, screenHeight):
        if self.dirty or self.lastDrawnAngle != self.angle:
            self.image = pygame.transform.rotate(self.baseImage, self.angle)
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
