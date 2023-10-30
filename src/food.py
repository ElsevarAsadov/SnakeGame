import pygame as pg
from random import randrange
from src.AssetLoader import AssetLoader


class Food:
    def __init__(self, scene):
        self.scene = scene

        self.texture = AssetLoader.load('apple.png')
        self.rect = self.texture.get_rect()

        self.active = False

    def draw(self):
        self.scene.blit(self.texture, self.rect)

    def update(self):
        if not self.active:
            self.__generate()
            self.active = True

    def __generate(self):
        x, y = randrange(0, 800, 40), randrange(0, 600, 40)
        self.rect.topleft = (x, y)
