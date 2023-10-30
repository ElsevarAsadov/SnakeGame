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


    # ------- CORE -------- #
    def __move(self):
        # TODO: SEPERATE ANIMATION AND MOVEMENT AND MAKE SMOOTH ANIMATION

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

        # ++ ---------------------------------------------------- ++ #

    def __apply_texture(self):
        # -- apply texture -- #
        for i in range(len(self.body) - 2, 0, -1):
            prev_segment = self.body[i - 1]
            curr_segment = self.body[i]
            next_segment = self.body[i + 1]

            if prev_segment.type == 'tail' and next_segment.type == 'head':

                if prev_segment.direction == 'left' and curr_segment.direction == 'horizontal' and next_segment.direction == 'right':
                    curr_segment.direction = 'horizontal'

                elif prev_segment.direction == 'left' and curr_segment.direction == 'horizontal' and next_segment.direction == 'down':
                    curr_segment.direction = 'bottom_left'

                elif prev_segment.direction == 'left' and curr_segment.direction == 'horizontal' and next_segment.direction == 'up':
                    curr_segment.direction = 'top_left'

                elif prev_segment.direction == 'left' and curr_segment.direction == 'bottom_left' and next_segment.direction == 'down':
                    prev_segment.direction = 'up'
                    curr_segment.direction = 'vertical'

                elif prev_segment.direction == 'left' and curr_segment.direction == 'bottom_left' and next_segment.direction == 'right':
                    prev_segment.direction = 'up'
                    curr_segment.direction = 'top_right'

                elif prev_segment.direction == 'left' and curr_segment.direction == 'bottom_left' and next_segment.direction == 'left':
                    prev_segment.direction = 'up'
                    curr_segment.direction = 'top_left'

                elif prev_segment.direction == 'left' and curr_segment.direction == 'top_left' and next_segment.direction == 'up':
                    curr_segment.direction = 'vertical'
                    prev_segment.direction = 'down'

                elif prev_segment.direction == 'left' and curr_segment.direction == 'top_left' and next_segment.direction == 'right':
                    curr_segment.direction = 'bottom_right'
                    prev_segment.direction = 'down'

                elif prev_segment.direction == 'left' and curr_segment.direction == 'top_left' and next_segment.direction == 'left':
                    curr_segment.direction = 'bottom_left'
                    prev_segment.direction = 'down'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'vertical' and next_segment.direction == 'down':
                    curr_segment.direction = 'vertical'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'vertical' and next_segment.direction == 'left':
                    curr_segment.direction = 'top_left'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'vertical' and next_segment.direction == 'right':
                    curr_segment.direction = 'top_right'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'top_left' and next_segment.direction == 'left':
                    curr_segment.direction = 'horizontal'
                    prev_segment.direction = 'right'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'top_left' and next_segment.direction == 'down':
                    curr_segment.direction = 'bottom_right'
                    prev_segment.direction = 'right'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'top_left' and next_segment.direction == 'up':
                    curr_segment.direction = 'top_right'
                    prev_segment.direction = 'right'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'top_right' and next_segment.direction == 'right':
                    curr_segment.direction = 'horizontal'
                    prev_segment.direction = 'left'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'top_right' and next_segment.direction == 'up':
                    curr_segment.direction = 'top_left'
                    prev_segment.direction = 'left'

                elif prev_segment.direction == 'up' and curr_segment.direction == 'top_right' and next_segment.direction == 'down':
                    curr_segment.direction = 'bottom_left'
                    prev_segment.direction = 'left'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'horizontal' and next_segment.direction == 'left':
                    curr_segment.direction = 'horizontal'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'horizontal' and next_segment.direction == 'up':
                    curr_segment.direction = 'top_right'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'horizontal' and next_segment.direction == 'down':
                    curr_segment.direction = 'bottom_right'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'top_right' and next_segment.direction == 'up':
                    curr_segment.direction = 'vertical'
                    prev_segment.direction = 'down'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'top_right' and next_segment.direction == 'right':
                    curr_segment.direction = 'bottom_right'
                    prev_segment.direction = 'down'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'top_right' and next_segment.direction == 'left':
                    curr_segment.direction = 'bottom_left'
                    prev_segment.direction = 'down'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'bottom_right' and next_segment.direction == 'down':
                    curr_segment.direction = 'vertical'
                    prev_segment.direction = 'up'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'bottom_right' and next_segment.direction == 'left':
                    curr_segment.direction = 'top_left'
                    prev_segment.direction = 'up'

                elif prev_segment.direction == 'right' and curr_segment.direction == 'bottom_right' and next_segment.direction == 'right':
                    curr_segment.direction = 'top_right'
                    prev_segment.direction = 'up'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'bottom_right' and next_segment.direction == 'right':
                    curr_segment.direction = 'horizontal'
                    prev_segment.direction = 'left'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'bottom_right' and next_segment.direction == 'up':
                    curr_segment.direction = 'top_left'
                    prev_segment.direction = 'left'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'bottom_right' and next_segment.direction == 'down':
                    curr_segment.direction = 'bottom_left'
                    prev_segment.direction = 'left'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'bottom_left' and next_segment.direction == 'left':
                    curr_segment.direction = 'horizontal'
                    prev_segment.direction = 'right'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'bottom_left' and next_segment.direction == 'up':
                    curr_segment.direction = 'top_right'
                    prev_segment.direction = 'right'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'bottom_left' and next_segment.direction == 'down':
                    curr_segment.direction = 'bottom_right'
                    prev_segment.direction = 'right'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'vertical' and next_segment.direction == 'up':
                    curr_segment.direction = 'vertical'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'vertical' and next_segment.direction == 'right':
                    curr_segment.direction = 'bottom_right'
                    prev_segment.direction = 'down'

                elif prev_segment.direction == 'down' and curr_segment.direction == 'vertical' and next_segment.direction == 'left':
                    curr_segment.direction = 'bottom_left'
                    prev_segment.direction = 'down'

                else:
                    ...
                    # TODO BUG HERE
                    print("ERROR")
                    print(prev_segment.direction, curr_segment.direction, next_segment.direction)

        # ++ ---------------------------------------------------- ++ #

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

        if e.type == Snake.E_SNAKE_ANIMATION:
            self.animation_lock = False

    def draw(self):
        for body in self.body:
            body.draw(self.scene)

    def update(self):
        if not self.animation_lock:

            self.__move()
            self.__apply_texture()

            self.animation_lock = True

