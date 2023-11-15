import time

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
        for i in range(1, len(self.body) - 1):
            before = self.body[i - 1]
            current = self.body[i]
            after = self.body[i + 1]

            """
            
            Whatever snake shape is everytime head is always after as well as tail is always before body part.
            self.body -> [TAIL ..., BODY ,... HEAD]
            """

            if before.type == 'tail' and current.type == 'body' and after.type == 'head':
                tail = before
                cbody = current
                abody = after

                tx, ty = tail.pos
                cbx, cby = cbody.pos
                abx, aby = abody.pos

                if tx < cbx < abx:
                    """
                    T - B - H
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'left'
                    cbody.direction = 'horizontal'

                elif tx > cbx > abx:
                    """
                     H - B - T
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'right'
                    cbody.direction = 'horizontal'


                elif ty > cby > aby:
                    """
                     H
                     |
                     B
                     |
                     T
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'down'
                    cbody.direction = 'vertical'


                elif ty < cby < aby:
                    """
                     T
                     |
                     B
                     |
                     H
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'up'
                    cbody.direction = 'vertical'


                elif ty == cby and aby < cby and abx > tx:
                    """
                    
                         H
                         |
                     T - B
                     
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'left'
                    cbody.direction = 'top_left'


                elif ty == cby and aby > cby and abx > tx:
                    """

                     T - B
                         |
                         H
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'left'
                    cbody.direction = 'bottom_left'


                elif ty == cby and aby > cby and abx < tx:
                    """

                         B - T
                         |
                         H
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'right'
                    cbody.direction = 'bottom_right'


                elif ty == cby and aby < cby and abx < tx:
                    """

                         H 
                         |
                         B - T
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'right'
                    cbody.direction = 'top_right'


                elif ty > cby and abx > cbx:
                    """

                         B - H
                         |
                         T
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'down'
                    cbody.direction = 'bottom_right'


                elif ty < cby and abx > cbx:
                    """

                         T  
                         |
                         B - H
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'up'
                    cbody.direction = 'top_right'



                elif ty > cby and abx < cbx:
                    """
                    H -  B
                         |
                         T
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'down'
                    cbody.direction = 'bottom_left'


                elif ty < cby and abx < cbx:
                    """
                         T
                         |
                     H - B
                    """
                    # tail texture name is reverse see textures images...
                    if i == 1:
                        tail.direction = 'up'
                    cbody.direction = 'top_left'

            elif before.type == 'body' and current.type == 'body' and after.type == 'head':
                # previous body
                tail = before
                # current body
                cbody = current
                abody = after

                tx, ty = tail.pos
                cbx, cby = cbody.pos
                abx, aby = abody.pos

                if tx < cbx < abx:
                    """
                    PB - CB - H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'horizontal'

                    if i == len(self.body) - 2:
                        abody.direction = 'right'

                elif tx > cbx > abx:
                    """
                     H - CB - PB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'horizontal'
                    if i == len(self.body) - 2:
                        abody.direction = 'left'

                elif ty > cby > aby:
                    """
                     H
                     |
                     CB
                     |
                     PB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'vertical'
                    if i == len(self.body) - 2:
                        abody.direction = 'up'

                elif ty < cby < aby:
                    """
                     PB
                     |
                     CB
                     |
                     H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'vertical'
                    if i == len(self.body) - 2:
                        abody.direction = 'down'


                elif ty == cby and aby < cby and abx > tx:
                    """

                         H
                         |
                    PB - CB

                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_left'
                    if i == len(self.body) - 2:
                        abody.direction = 'up'

                elif ty == cby and aby > cby and abx > tx:
                    """

                   PB - CB
                         |
                         H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_left'
                    if i == len(self.body) - 2:
                        abody.direction = 'down'

                elif ty == cby and aby > cby and abx < tx:
                    """

                         CB - PB
                         |
                         H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_right'
                    if i == len(self.body) - 2:
                        abody.direction = 'down'

                elif ty == cby and aby < cby and abx < tx:
                    """

                         H 
                         |
                         CB - PB
                    """
                    # tail texture name is reverse see textures images...

                    cbody.direction = 'top_right'
                    if i == len(self.body) - 2:
                        abody.direction = 'up'

                elif ty > cby and abx > cbx:
                    """

                         CB - H
                         |
                         PB
                    """
                    # tail texture name is reverse see textures images...

                    cbody.direction = 'bottom_right'
                    if i == len(self.body) - 2:
                        abody.direction = 'right'

                elif ty < cby and abx > cbx:
                    """

                         PB  
                         |
                         CB - H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_right'
                    if i == len(self.body) - 2:
                        abody.direction = 'right'


                elif ty > cby and abx < cbx:
                    """
                    H -  CB
                         |
                         PB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_left'
                    if i == len(self.body) - 2:
                        abody.direction = 'left'

                elif ty < cby and abx < cbx:
                    """
                         PB
                         |
                     H - CB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_left'
                    if i == len(self.body) - 2:
                        abody.direction = 'left'

            elif before.type == 'tail' and current.type == 'body' and after.type == 'body':
                # previous body
                tail = before
                # current body
                cbody = current
                abody = after

                tx, ty = tail.pos
                cbx, cby = cbody.pos
                abx, aby = abody.pos

                if tx < cbx < abx:
                    """
                    T - CB - H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'horizontal'

                    if i == 1:
                        tail.direction = 'left'

                elif tx > cbx > abx:
                    """
                     H - CB - T
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'horizontal'
                    if i == 1:
                        tail.direction = 'right'

                elif ty > cby > aby:
                    """
                     H
                     |
                     CB
                     |
                     T
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'vertical'
                    if i == 1:
                        tail.direction = 'down'

                elif ty < cby < aby:
                    """
                     T
                     |
                     CB
                     |
                     H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'vertical'
                    if i == 1:
                        tail.direction = 'up'


                elif ty == cby and aby < cby and abx > tx:
                    """

                         H
                         |
                    T - CB

                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_left'
                    if i == 1:
                        tail.direction = 'left'

                elif ty == cby and aby > cby and abx > tx:
                    """

                   T - CB
                         |
                         H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_left'
                    if i == 1:
                        tail.direction = 'left'

                elif ty == cby and aby > cby and abx < tx:
                    """

                         CB - T
                         |
                         H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_right'
                    if i == 1:
                        tail.direction = 'right'

                elif ty == cby and aby < cby and abx < tx:
                    """

                         H 
                         |
                         CB - T
                    """
                    # tail texture name is reverse see textures images...

                    cbody.direction = 'top_right'
                    if i == 1:
                        tail.direction = 'right'

                elif ty > cby and abx > cbx:
                    """

                         CB - H
                         |
                         T
                    """
                    # tail texture name is reverse see textures images...

                    cbody.direction = 'bottom_right'
                    if i == 1:
                        tail.direction = 'down'

                elif ty < cby and abx > cbx:
                    """

                         T  
                         |
                         CB - H
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_right'
                    if i == 1:
                        tail.direction = 'up'


                elif ty > cby and abx < cbx:
                    """
                    H -  CB
                         |
                         T
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_left'
                    if i == 1:
                        tail.direction = 'down'

                elif ty < cby and abx < cbx:
                    """
                         T
                         |
                     H - CB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_left'
                    if i == 1:
                        tail.direction = 'up'

            elif before.type == 'body' and current.type == 'body' and after.type == 'body':
                # previous body
                tail = before
                # current body
                cbody = current
                # after body
                abody = after

                tx, ty = tail.pos
                cbx, cby = cbody.pos
                abx, aby = abody.pos

                if tx < cbx < abx:
                    """
                    PB - CB - AB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'horizontal'



                elif tx > cbx > abx:
                    """
                     AB - CB - PB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'horizontal'

                elif ty > cby > aby and tx == cbx == abx:
                    """
                     AB
                     |
                     CB
                     |
                     PB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'vertical'

                elif ty < cby < aby:
                    """
                     PB
                     |
                     CB
                     |
                     AB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'vertical'

                elif ty == cby and aby < cby and abx > tx:
                    """

                         AB
                         |
                    PB - CB

                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_left'

                elif ty == cby and aby > cby and abx > tx:
                    """

                   PB - CB
                         |
                         AB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_left'

                elif ty == cby and aby > cby and abx < tx:
                    """

                         CB - PB
                         |
                         AB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_right'


                elif ty == cby and aby < cby and abx < tx:
                    """

                         AB 
                         |
                         CB - PB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_right'


                elif ty > cby and abx > cbx:
                    """

                         CB - AB
                         |
                         PB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_right'


                elif ty < cby and abx > cbx:
                    """

                         PB  
                         |
                         CB - AB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_right'



                elif ty > cby and abx < cbx:
                    """
                  AB -  CB
                         |
                         PB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'bottom_left'


                elif ty < cby and abx < cbx:
                    """
                         PB
                         |
                    AB - CB
                    """
                    # tail texture name is reverse see textures images...
                    cbody.direction = 'top_left'

            """ DEBUGGING """
            # pg.draw.rect(before.texture, 'red', (0, 0, 40, 40), 2)
            # pg.draw.rect(current.texture, 'blue', (0, 0, 40, 40), 2)
            # pg.draw.rect(after.texture, 'green', (0, 0, 40, 40), 2)

    def game_over(self) -> bool:
        if self.__check_collision_with_body() or self.__check_borders():
            return True

        return False

    # +++++++++++++++++++++ #

    def __grow(self):
        tail = self.body[0]

        # tail direction left means tail rounded part direction is left
        if tail.direction == 'left':
            tail.pos = (tail.pos[0] - 40, tail.pos[1])
            tail_x, tail_y = tail.pos
            new_body_part = SnakeBody((tail_x + 40, tail_y), 'body', 'horizontal')

        elif tail.direction == 'right':
            tail.pos = (tail.pos[0] + 40, tail.pos[1])
            tail_x, tail_y = tail.pos
            new_body_part = SnakeBody((tail_x - 40, tail_y), 'body', 'horizontal')

        elif tail.direction == 'up':
            tail.pos = (tail.pos[0], tail.pos[1] - 40)
            tail_x, tail_y = tail.pos
            new_body_part = SnakeBody((tail_x, tail_y + 40), 'body', 'vertical')

        elif tail.direction == 'down':
            tail.pos = (tail.pos[0], tail.pos[1] + 40)
            tail_x, tail_y = tail.pos
            new_body_part = SnakeBody((tail_x, tail_y - 40), 'body', 'vertical')
        else:
            raise Exception("invalid body part direction")

        self.body.insert(1, new_body_part)
        # tail.pos = (tail.pos[0], tail.pos[1] + 40)

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

            # DEBUGGING
            # elif e.key == pg.K_z:
            # self.animation_lock = False

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
