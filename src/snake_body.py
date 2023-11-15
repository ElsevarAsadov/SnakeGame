import pygame as pg
from os.path import join, dirname

from src.AssetLoader import AssetLoader

TEXTURE_PATH = join(dirname(__file__), 'Graphics')

TEXTURES = {
    'head': {
        'up': 'head_up.png',
        'down': 'head_down.png',
        'left': 'head_left.png',
        'right': 'head_right.png',
    },
    'body': {
        'horizontal': 'body_horizontal.png',
        'vertical': 'body_vertical.png',
        'top_left': 'body_topleft.png',
        'top_right': 'body_topright.png',
        'bottom_left': 'body_bottomleft.png',
        'bottom_right': 'body_bottomright.png',
    },
    'tail': {
        'up': 'tail_up.png',
        'down': 'tail_down.png',
        'left': 'tail_left.png',
        'right': 'tail_right.png',
    }
}


class SnakeBody:
    def __init__(self, pos, _type, direction):
        self.type = _type
        self.texture = AssetLoader.load(TEXTURES[self.type][direction])
        self.rect = self.texture.get_rect(topleft=pos)
        self._direction = direction

    def draw(self, scene):
        scene.blit(self.texture, self.rect)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction
        self.texture = AssetLoader.load(TEXTURES[self.type][direction])

    @property
    def pos(self):
        return self.rect.topleft

    @pos.setter
    def pos(self, value):
        self.rect.topleft = value


    def __str__(self):
        return f'{self.type} - {self.direction}'

    def __repr__(self):
        return f'{self.type} - {self.direction}'
