from src.snake_body import SnakeBody
from typing import List
import pygame as pg


class Snake:
    E_SNAKE_ANIMATION = pg.USEREVENT + 1
    E_SNAKE_CONTROL = pg.USEREVENT + 2

    def __init__(self, scene):
        self.scene = scene
        self.direction = "right"

        # initial body
        scene_center_y = self.scene.get_size()[1] // 2

        self.body: List[SnakeBody] = [
            SnakeBody((0, scene_center_y - 20), 'tail', 'left'),
            SnakeBody((40, scene_center_y - 20), 'body', 'horizontal'),
            SnakeBody((80, scene_center_y - 20), 'head', 'right'),

        ]
        self.head = self.body[-1]
        self.head_pos = self.body[-1].pos


        self.animation_lock = True
        pg.time.set_timer(Snake.E_SNAKE_ANIMATION, 100)

    def __check_collision_with_body(self):

        for i, body in enumerate(self.body):
            rect_list = [_.rect for x, _ in enumerate(self.body) if x != i]
            if body.rect.collidelist(rect_list) != -1:
                return True

        return False

    def __check_borders(self) -> bool:
        if self.head_pos[1] < 0 or self.head_pos[1] > 600:
            return True

        return False

    def __move(self):
        # TODO: MAKE SMOOTH ANIMATION

        head = self.body[-1]
        head_x, head_y = head.pos
        scene_x, scene_y = self.scene.get_size()

        # move head position
        if self.direction.lower() == 'up':
            self.head_pos = pg.Vector2(head_x, head_y - 40)
            head.direction = 'up'

        elif self.direction.lower() == 'down':
            self.head_pos = pg.Vector2(head_x, head_y + 40)
            head.direction = 'down'

        elif self.direction.lower() == 'left':
            self.head_pos = pg.Vector2(head_x - 40, head_y)
            head.direction = 'left'

        elif self.direction.lower() == 'right':
            self.head_pos = pg.Vector2(head_x + 40, head_y)
            head.direction = 'right'

        # snake exceeds border - RIGHT
        if head_x > scene_x:
            self.head_pos = (0, head_y)

        # snake exceeds border - LEFT
        if head_x < 0:
            self.head_pos = (scene_x, head_y)

        # -- change position of body parts corresponding to head -- #
        after = head.pos
        head.pos = self.head_pos

        for body in reversed(self.body[:-1]):
            current = body.pos
            body.pos = after
            after = current

    def __apply_texture(self):
        head_x, head_y = self.head_pos

        for body in sorted(self.body[:-1], key=lambda b: b.pos[1]):
            if body.pos[0] == head_x:
                body.direction = 'down' if body.type == 'tail' else 'vertical'

        prev_body = None
        for i, segment in enumerate(self.body):
            if segment.pos == body.pos:
                # body parts are reversed order in array head is the last index
                prev_body = self.body[i - 1]

        # just in case :)
        if not prev_body:
            raise Exception("No prev_body found")

        body_x, body_y = body.pos
        prev_x, prev_y = prev_body.pos

        if self.head.direction == 'up':

            # the last body is always had to be curvy
            if body.type == 'body':

                if body_x < prev_x and head_y < prev_y:
                    body.direction = 'top_right'

                else:
                    body.direction = 'top_left'

        elif self.head.direction == 'down':

            for body in sorted(self.body[:-1], key=lambda b: -b.pos[1]):

                if body.pos[0] == head_x:

                    body.direction = 'up' if body.type == 'tail' else 'vertical'

            # the last body is always had to be curve
            if body.type == 'body':

                if body_x < prev_x and head_y > prev_y:
                    print("A")
                    body.direction = 'bottom_right'

                else:
                    print("C")
                    body.direction = 'bottom_left'

        elif self.head.direction == 'right':

            for body in sorted(self.body[:-1], key=lambda b: -b.pos[0]):
                if body.pos[1] == head_y:
                    body.direction = 'left' if body.type == 'tail' else 'horizontal'
            # the last body is always had to be curve
            if body.type == 'body':

                if body.pos[0] > head_x:
                    body.direction = 'bottom_left'

                elif body.pos[0] < head_x:
                    body.direction = 'bottom_right'

                else:
                    body.direction = 'horizontal'

        elif self.head.direction == 'left':

            for body in sorted(self.body[:-1], key=lambda b: b.pos[0]):

                if body.pos[1] == head_y:

                    body.direction = 'right' if body.type == 'tail' else 'horizontal'

            if body.type == 'body':

                if body.pos[0] > head_x:
                    body.direction = 'top_right'

                elif body.pos[0] < head_x:
                    body.direction = 'top_left'





    def game_over(self) -> bool:
        if self.__check_collision_with_body() or self.__check_borders():
            return True

        return False

    # +++++++++++++++++++++ #

    def __grow(self):
        tail = self.body[0]
        tail_x, tail_y = tail.pos

        # tail direction left means tail rounded part direction is left
        if tail.direction == 'left':
            new_body_part = SnakeBody((tail_x + 40, tail_y), 'body', 'horizontal')
        elif tail.direction == 'right':
            new_body_part = SnakeBody((tail_x - 40, tail_y), 'body', 'horizontal')
        elif tail.direction == 'up':
            new_body_part = SnakeBody((tail_x, tail_y + 40), 'body', 'up')
        elif tail.direction == 'up':
            new_body_part = SnakeBody((tail_x, tail_y - 40), 'body', 'down')
        else:
            raise Exception("invalid body part direction")

        self.body.insert(1, new_body_part)


    def handle_controls(self, e):

        if e.type == pg.KEYDOWN:

            if e.key == pg.K_w and self.direction != "down" and self.body[-2].pos[0] != self.head_pos[0]:
                self.direction = "up"
            elif e.key == pg.K_s and self.direction != "up" and self.body[-2].pos[0] != self.head_pos[0]:
                self.direction = "down"
            elif e.key == pg.K_a and self.direction != "right" and self.body[-2].pos[1] != self.head_pos[1]:
                self.direction = "left"
            elif e.key == pg.K_d and self.direction != "left" and self.body[-2].pos[1] != self.head_pos[1]:
                self.direction = "right"

            elif e.key == pg.K_SPACE:
                self.__grow()

            elif e.key == pg.K_z:
                self.animation_lock = False

        # if e.type == Snake.E_SNAKE_ANIMATION:
        #     self.animation_lock = False

    def draw(self):
        for body in self.body:
            body.draw(self.scene)

    def update(self):
        if not self.animation_lock:

            self.__move()
            self.__apply_texture()

            self.animation_lock = True

