import pygame

from interaction import Interactable
from inventory import InventoryView


class UI(pygame.sprite.OrderedUpdates):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.backpack = Backpack(world, self)
        self.add(self.backpack)
        self.inventoryView = InventoryView(self, world.inventory)

    def hideBackpackIcon(self):
        self.remove(self.backpack)

    def showBackpackIcon(self):
        self.add(self.backpack)

    def showInventoryView(self):
        self.inventoryView.show()

    def hideInventoryView(self):
        self.inventoryView.hide()


class Backpack(Interactable):
    def __init__(self, world, ui):
        super().__init__()
        self.image = pygame.image.load("assets/inventoryicon.png").convert_alpha()
        w, h = self.image.get_size()
        self.x = 10
        self.y = world.height - h - 10
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.hover = True
        self.click = True
        world.interactionHandler.register(self)
        self.ui = ui

    def onHover(self):
        self.ui.hideBackpackIcon()
        self.ui.showInventoryView()

    def onStopHover(self):
        pass

    def onClick(self, mouseX, mouseY):
        pass
