from src.AssetLoader import AssetLoader
from src.food import Food
from src.snake import Snake
import pygame as pg


class Game:
    def __init__(self, window_x, window_y, caption):
        pg.init()

        pg.display.set_caption(caption)
        self.scene = pg.display.set_mode((window_x, window_y))
        self.clock = pg.time.Clock()

        # GAME OBJECTS
        self.snake = Snake(self.scene)
        self.food = Food(self.scene)

    def start(self):
        while 1:
            self.event_handler()

            self.scene.fill('black')
            self.draw_background()

            self.snake.draw()
            self.snake.update()

            self.food.draw()
            self.food.update()

            if self.snake.game_over():
                print("GAME OVER")

            pg.display.flip()
            self.clock.tick(60)

    def event_handler(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()

            self.snake.handle_controls(e)

    def draw_background(self):
        x, y = self.scene.get_size()

        floor = AssetLoader.load("grass.png")

        for i in range(0, x, 40):
            for j in range(0, y, 40):
                self.scene.blit(floor, (i, j))
