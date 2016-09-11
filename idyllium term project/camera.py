# for camera panning / scrolling
import pygame


class Camera(object):
    def __init__(self):
        self.winX = 0
        self.winY = 0

    def apply(self, sprite):
        sprite.rect.x -= self.winX
        sprite.rect.y -= self.winY

    def applyGroup(self, group):
        for sprite in group.sprites():
            self.apply(sprite)
