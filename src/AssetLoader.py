import pygame as pg
from os.path import join, dirname


class AssetLoader:
    TEXTURE_PATH = join(dirname(__file__), 'Graphics')

    def __init__(self):
        ...

    @staticmethod
    def load(name: str) -> pg.Surface:
        return pg.image.load(join(AssetLoader.TEXTURE_PATH, name)).convert_alpha()
