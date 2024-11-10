import os
from math import pi
import pygame as pg
import content.game_state as gs
from content.assets.ui.textbox import TextBox
from content.assets.ui.button import Button
from content.utilities import tools

class Spaceship():
    def __init__(self):
        self.sprite = pg.image.load(os.path.join("content", "assets", "sprites", "spaceship.png")).convert_alpha()
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.rect.center = (gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT - 200)
        self.rotation_angle = 0
    
    def rotate(self, angle):
        self.rotation_angle += angle
        self.update()

    def update(self):
        prev_center = self.rect.center

        self.sprite = pg.transform.rotate(self.sprite, self.rotation_angle)
        self.rect = self.sprite.get_rect()
        self.rect.center = prev_center

    def render(self):
        gs.SCREEN.blit(self.sprite, self.rect)
        #(gs.SCREEN_WIDTH / 2 - self.sprite.get_width() / 2, gs.SCREEN_HEIGHT - 200)

spaceship = Spaceship()
millisec = pg.time.Clock().get_time()

def update():
    global spaceship, millisec

    ## INPUT ##
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                quit()
            elif event.key == pg.K_RIGHT:
                spaceship.rotate(5)

    '''
    keyevent = pg.key.get_pressed()

    if keyevent[pg.K_RIGHT] or keyevent[pg.K_d]:
        spaceship.rotate(5)
    elif keyevent[pg.K_LEFT] or keyevent[pg.K_s]:
        spaceship.rotate(-5)
    '''

    spaceship.render()