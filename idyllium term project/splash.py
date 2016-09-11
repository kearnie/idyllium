import pygame


class Splash(pygame.sprite.Group):
    def __init__(self):
        super().__init__()


class TitleBG(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/splashscreen.png")
        w, h = self.image.get_size()
        self.rect = pygame.Rect(0, 0, w, h)


class HelpBG(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/instructions.png")
        w, h = self.image.get_size()
        self.rect = pygame.Rect(0, 0, w, h)
