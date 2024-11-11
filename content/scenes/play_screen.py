import os
from math import pi, cos, sin, radians
from typing import Tuple
import pygame as pg
import content.game_state as gs
from content.assets.ui.textbox import TextBox
from content.assets.ui.button import Button
from content.utilities import tools

class GameObject():
    def __init__(self, rotation_angle: int, position: Tuple[int, int], path, speed: int):
        self.sprite = path
        self.rotation_angle = rotation_angle
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.speed = speed
        self.surface = pg.Surface(self.sprite.get_size(), pg.SRCALPHA)
        self.surface.blit(self.sprite, self.position)

    def move(self, direction: int):
        self.x += direction * self.speed * cos(radians(self.rotation_angle + 90))
        self.y -= direction * self.speed * sin(radians(self.rotation_angle + 90))

        self.position = self.x, self.y

    def render(self):
        pos = self.position
        w, h = self.sprite.get_size()
        originPos = w / 2, h / 2

        # offset from pivot to center
        image_rect = self.surface.get_rect(topleft = (pos[0] - originPos[0], pos[1] - originPos[1]))
        offset_center_to_pivor = pg.math.Vector2(pos) - image_rect.center

        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivor.rotate(-self.rotation_angle)

        #rotated image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pg.transform.rotate(self.surface, self.rotation_angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        # rotate and blit the image
        gs.SCREEN.blit(rotated_image, rotated_image_rect)
        self.surface.blit(self.sprite, (0, 0))

class Asteroid(GameObject):
    def __init__(self, rotation_angle: int, position: Tuple[int, int], speed: int):
        super().__init__(rotation_angle, position, pg.image.load(os.path.join("content", "assets", "sprites", "asteroid.png")), speed)

class Bullet(GameObject):
    def __init__(self, rotation_angle: float, position: Tuple[int, int], speed: int):
        super().__init__(rotation_angle, position, pg.image.load(os.path.join("content", "assets", "sprites", "bullet.png")), speed)

    def DetectHit(self, asteroids: list[Asteroid]):
        for asteroid in asteroids:
            print("hit")

class Spaceship(GameObject):
    def __init__(self, position: Tuple[int, int], speed: int):
        super().__init__(0, position, pg.image.load(os.path.join("content", "assets", "sprites", "spaceship.png")), speed)
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.angular_vel = 40
    
    def rotate(self, angle: float):
        self.rotation_angle += angle * self.angular_vel

    def shoot(self, bullets: list[Bullet]):
        bullet = Bullet(self.rotation_angle, self.position, 100)
        bullets.append(bullet)

spaceship = Spaceship((gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT - 200), 5)
clock = pg.time.Clock()

# shoot cooldown
bullets: list[Bullet] = []
max_shoot_cooldown = 500
shoot_cooldown = max_shoot_cooldown

# asteroid generation cooldown
asteroids: list[Asteroid] = []
max_asteroid_cooldown = 300
asteroid_cooldown = max_asteroid_cooldown

def update():
    global spaceship, clock, bullets, max_shoot_cooldown, shoot_cooldown, asteroids, max_asteroid_cooldown, asteroid_cooldown

    # for shoot and skill cooldown
    clock.tick()
    millisec = clock.get_time()

    # update cooldowns
    shoot_cooldown += millisec
    asteroid_cooldown += millisec

    ## INPUT ##
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                quit()

    keyevent = pg.key.get_pressed()

    if keyevent[pg.K_RIGHT] or keyevent[pg.K_d]:
        spaceship.rotate(-millisec * (2 * pi / 1000))
    
    if keyevent[pg.K_LEFT] or keyevent[pg.K_a]:
        spaceship.rotate(millisec * (2 * pi / 1000))

    if keyevent[pg.K_SPACE]:
        if shoot_cooldown > max_shoot_cooldown:
            shoot_cooldown = 0
            spaceship.shoot(bullets)

    if keyevent[pg.K_UP] or keyevent[pg.K_w]:
        spaceship.move(1)

    if keyevent[pg.K_DOWN] or keyevent[pg.K_s]:
        spaceship.move(-1)

    spaceship.render()

    for bullet in bullets:
        if bullet.x > gs.SCREEN_WIDTH or bullet.x < 0 or bullet.y < 0 or bullet.y > gs.SCREEN_HEIGHT:
            bullets.remove(bullet)
        else:
            bullet.move(1)
            bullet.render()

    if asteroid_cooldown > max_asteroid_cooldown:
        asteroid_cooldown = 0

        asteroid = Asteroid(315, (50, 50), 10)
        asteroids.append(asteroid)

    for asteroid in asteroids:
        if asteroid.x > gs.SCREEN_WIDTH or asteroid.x < 0 or asteroid.y < 0 or asteroid.y > gs.SCREEN_HEIGHT:
            asteroids.remove(asteroid)
        else:
            asteroid.move(1)
            asteroid.render()