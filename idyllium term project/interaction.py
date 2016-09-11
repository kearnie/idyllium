import pygame


# We created this in main and pass it to the world
class InteractionHandler(object):
    def __init__(self):
        self.hoverables = []
        self.clickables = []
        self.interactables = []
        self.currentlyHovering = set()
        InteractionHandler.instance = self
        self.clickActivated = False
        self.onCursor = None

    """"
    must be called on interactable objects for them to work.
    self.click and self.hover must already be set by the time this is called
    """

    def register(self, interactable):
        assert (isinstance(interactable, Interactable))
        self.interactables.append(interactable)
        if interactable.hover:
            self.hoverables.append(interactable)
        if interactable.click:
            self.clickables.append(interactable)

    def unregister(self, interactable):
        if interactable in self.interactables:
            self.interactables.remove(interactable)
        if interactable in self.hoverables:
            self.hoverables.remove(interactable)
        if interactable in self.clickables:
            self.clickables.remove(interactable)

    def onTick(self, mouse, wasClicked):
        mouseX, mouseY = mouse
        self.clickActivated = False
        if self.onCursor != None:
            self.onCursor.rect.x = mouseX
            self.onCursor.rect.y = mouseY
        if wasClicked:
            # we want to click the lowest priority thing and only that
            possible = [inter for inter in self.clickables
                        if inter.contains(mouseX, mouseY)]
            if (self.onCursor != None):
                possible.remove(self.onCursor)
            clicked = min(possible, key=lambda x: x.priority, default=None)
            if clicked != None:
                if (self.onCursor != None and self.onCursor.use):
                    self.onCursor.onUse(clicked, mouseX, mouseY)
                else:
                    clicked.onClick(mouseX, mouseY)
                    self.clickActivated = True
        else:
            for inter in self.hoverables:
                isHovering = inter.contains(mouseX, mouseY)
                if inter not in self.currentlyHovering and isHovering:
                    self.currentlyHovering.add(inter)
                    inter.onHover()
                if inter in self.currentlyHovering and not isHovering:
                    self.currentlyHovering.remove(inter)
                    inter.onStopHover()


# super class to extend for interactable sprites
class Interactable(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hover = False
        self.click = False
        self.priority = 0
        self.use = False

    def contains(self, x, y):
        return self.rect.collidepoint(x, y)

    def onClick(self, mouseX, mouseY):
        pass

    def onUse(self, otherSprite, mouseX, mouseY):
        pass

    def onHover(self):
        pass

    def onStopHover(self):
        pass
