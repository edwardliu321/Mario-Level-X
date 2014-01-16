__author__ = 'justinarmstrong'


import pygame as pg
from .. import setup
from .. import constants as c


class Enemy(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)


    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        return image


    def set_velocity(self):
        if self.direction == c.LEFT:
            self.x_vel = -2
        else:
            self.x_vel = 2

        self.y_vel = 0


    def setup_enemy(self, x, y, direction, name, setup_frames):
        self.sprite_sheet = setup.GFX['smb_enemies_sheet']
        self.frames = []
        self.frame_index = 0
        self.animate_timer = 0
        self.death_timer = 0
        self.gravity = 1.5
        self.state = c.WALK

        self.name = name
        self.direction = direction
        setup_frames()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.set_velocity()



    def handle_state(self, current_time):
        if self.state == c.WALK:
            self.walking(current_time)
        elif self.state == c.FALL:
            self.falling(current_time)
        elif self.state == c.JUMPED_ON:
            self.jumped_on(current_time)
        elif self.state == c.SHELL_SLIDE:
            self.shell_sliding()



    def walking(self, current_time):
        if (current_time - self.animate_timer) > 125:
            if self.frame_index == 0:
                self.frame_index += 1
            elif self.frame_index == 1:
                self.frame_index = 0

            self.animate_timer = current_time


    def falling(self, current_time):
        if self.y_vel < 10:
            self.y_vel += self.gravity


    def jumped_on(self, current_time):
        pass


    def animation(self):
        self.image = self.frames[self.frame_index]


    def update(self, current_time):
        self.handle_state(current_time)
        self.animation()




class Goomba(Enemy):

    def __init__(self, x, y, direction, name):
        Enemy.__init__(self)
        self.setup_enemy(x, y, direction, name, self.setup_frames)


    def setup_frames(self):
        """Put the image frames in a list to be animated"""

        self.frames.append(
            self.get_image(0, 4, 16, 16))
        self.frames.append(
            self.get_image(30, 4, 16, 16))
        self.frames.append(
            self.get_image(61, 0, 16, 16))


    def jumped_on(self, current_time):
        self.frame_index = 2

        if (current_time - self.death_timer) > 500:
            self.kill()




class Koopa(Enemy):

    def __init__(self, x, y, direction, name):
        Enemy.__init__(self)
        self.setup_enemy(x, y, direction, name, self.setup_frames)


    def setup_frames(self):

        self.frames.append(
            self.get_image(150, 0, 16, 24))
        self.frames.append(
            self.get_image(180, 0, 16, 24))
        self.frames.append(
            self.get_image(360, 5, 16, 15))


    def jumped_on(self, current_time):
        self.x_vel = 0
        self.frame_index = 2
        shell_y = self.rect.bottom
        shell_x = self.rect.x
        self.rect = self.frames[self.frame_index].get_rect()
        self.rect.x = shell_x
        self.rect.bottom = shell_y


    def shell_sliding(self):
        if self.direction == c.RIGHT:
            self.x_vel = 10
        elif self.direction == c.LEFT:
            self.x_vel = -10












