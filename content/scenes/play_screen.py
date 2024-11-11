import os
from math import pi, cos, sin, radians, atan2, degrees
import random
from typing import Tuple
import pygame as pg
import content.game_state as gs
from content.assets.ui.textbox import TextBox
from content.utilities import tools
import content.scenes.player_hud as hud

class GameObject():
    def __init__(self, rotation_angle: int, position: Tuple[int, int], path: pg.Surface, speed: int):
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
    def __init__(self, rotation_angle: int, position: Tuple[int, int], speed: int, angular_vel: int, destination: Tuple[int, int], scale_factor: float):
        super().__init__(rotation_angle, position, pg.image.load(os.path.join("content", "assets", "sprites", "asteroid.png")), speed)
        self.sprite = pg.transform.scale(self.sprite, (self.sprite.get_size()[0] * scale_factor, self.sprite.get_size()[1] * scale_factor))
        self.angular_vel = angular_vel
        self.destination = destination
        self.direction = self.calcDirection()
        self.vx = 0
        self.vy = 0
    
    def calcDirection(self):
        dx = self.destination[0] - self.x
        dy = self.destination[1] - self.y
        rad = atan2(-dy, dx)
        rad %= 2 * pi
        deg = degrees(rad)

        return deg

    def asteroid_fly(self):
        self.x += self.speed * cos(radians(self.direction))
        self.y -= self.speed * sin(radians(self.direction))

        self.position = self.x, self.y

    def rotate(self, angle: float):
        self.rotation_angle += angle * self.angular_vel

    def updatePosition(self, millisec, thrust_vector = (0, 0), gravity_sources = []):
        ax, ay = thrust_vector
        gx, gy = gravitational_field(gravity_sources, self.x, self.y)
        
        ax += gx
        ay += gy

        self.vx += ax * millisec / 1000
        self.vy += ay * millisec / 1000

        dx, dy = self.vx * millisec / 1000.0, self.vy * millisec / 1000.0

        self.x, self.y = tuple(map(sum, zip((self.x, self.y), (dx, dy))))

    def detectHit(self, spaceship):
        if tools.isCollided(self.surface.get_rect(center = self.position), spaceship.surface.get_rect(center = spaceship.position)):
            if not spaceship.isInvincible:
                gs.SPACESHIP_LIVES -= 1

                if gs.SPACESHIP_LIVES <= 0:
                    gs.GAME_OVER = True

                return True
        
        return False

class Bullet(GameObject):
    def __init__(self, rotation_angle: float, position: Tuple[int, int], speed: int):
        super().__init__(rotation_angle, position, pg.image.load(os.path.join("content", "assets", "sprites", "bullet.png")), speed)
        self.sprite = pg.transform.scale(self.sprite, (self.sprite.get_size()[0] * gs.BULLET_SCALE_FACTOR, self.sprite.get_size()[1] * gs.BULLET_SCALE_FACTOR))

    def detectHit(self, asteroids: list[Asteroid]):
        if not len(asteroids) == 0:
            for asteroid in asteroids:
                if tools.isCollided(self.surface.get_rect(center = self.position), asteroid.surface.get_rect(center = asteroid.position)):
                    gs.SCORE += 1
                    asteroids.remove(asteroid)
                    return True
        
        return False
    
class Blackhole(GameObject):
    def __init__(self, rotation_angle: float, position: Tuple[int, int], speed):
        super().__init__(rotation_angle, position, pg.image.load(os.path.join("content", "assets", "sprites", "blackhole.png")), speed)
        self.sprite = pg.transform.scale(self.sprite, (self.sprite.get_size()[0] * gs.BLACKHOLE_SCALE_FACTOR, self.sprite.get_size()[1] * gs.BLACKHOLE_SCALE_FACTOR))
        self.direction = rotation_angle
        self.angular_vel = 10
        self.gravity = gs.GRAVITY

    def rotate(self, angle: float):
        self.rotation_angle += angle * self.angular_vel

    def blackhole_fly(self):
        self.x += self.speed * cos(radians(self.direction + 90))
        self.y -= self.speed * sin(radians(self.direction + 90))

        self.position = self.x, self.y

    def detectHit(self, asteroids: list[Asteroid]):
        if not len(asteroids) == 0:
            for asteroid in asteroids:
                if tools.isCollided(self.surface.get_rect(center = self.position), asteroid.surface.get_rect(center = asteroid.position)):
                    gs.SCORE += 1
                    asteroids.remove(asteroid)
                    return True
        
        return False

def gravitational_field(sources, x, y):
    fields = [tuple(source.gravity * coord for coord in (source.x - x, source.y - y)) for source in sources]
    return tuple(map(sum, zip(*fields)))

class Spaceship(GameObject):
    def __init__(self, position: Tuple[int, int], speed: int):
        super().__init__(0, position, pg.image.load(os.path.join("content", "assets", "sprites", "spaceship.png")), speed)
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.angular_vel = gs.SPACESHIP_ANGULAR_VEL
        self.isInvincible = False
    
    def rotate(self, angle: float):
        self.rotation_angle += angle * self.angular_vel

    def shoot(self, bullets: list[Bullet]):
        bullet = Bullet(self.rotation_angle, self.position, gs.BULLET_MAX_SPEED)
        bullets.append(bullet)

    def deathToAsteroids(self, blackholes: list[Blackhole]):
        blackhole = Blackhole(self.rotation_angle, self.position, 10)
        blackholes.append(blackhole)

    def updatePos(self):
        if self.x < 0:
            self.x = gs.SCREEN_WIDTH + self.x
        elif self.x > gs.SCREEN_WIDTH:
            self.x = self.x - gs.SCREEN_WIDTH
        
        if self.y < 0:
            self.y = gs.SCREEN_HEIGHT + self.y
        elif self.y > gs.SCREEN_HEIGHT:
            self.y = self.y - gs.SCREEN_HEIGHT

spaceship = Spaceship((gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 2), gs.SPACESHIP_SPEED)
clock = pg.time.Clock()

# shoot cooldown
bullets: list[Bullet] = []
shoot_cooldown = gs.BULLET_MAX_COOLDOWN

# blackhole cooldown
blackholes: list[Blackhole] = []
blackhole_cooldown = 0

# asteroid generation cooldown
asteroids: list[Asteroid] = []
asteroid_cooldown = gs.ASTEROID_MAX_COOLDOWN

def update():
    global spaceship, clock, bullets, shoot_cooldown, blackholes, blackhole_cooldown, asteroids, asteroid_cooldown

    # for shoot and skill cooldown
    clock.tick()
    millisec = clock.get_time()

    # update cooldowns
    shoot_cooldown += millisec
    blackhole_cooldown += millisec
    asteroid_cooldown += millisec

    if blackhole_cooldown > gs.BLACKHOLE_MAX_COOLDOWN:
        gs.BLACKHOLE_READY = True
    else:
        gs.BLACKHOLE_LEFT_COOLDOWN -= millisec

    if gs.GAME_OVER:
        gameOverText = TextBox(gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 3, "SPACESHIP LOST IN SPACE", gs.FONT_FAMILY, gs.TITLE_FONT_SIZE, gs.TITLE_COLOR)
        scoreText = TextBox(gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 2, "FINAL SCORE: " + str(gs.SCORE), gs.FONT_FAMILY, gs.TITLE_FONT_SIZE, gs.SKY_BLUE)

        while True:
            tools.updateTxtBoxes([gameOverText, scoreText])

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_TAB:
                        pg.quit()
                        quit()

            pg.display.update()
            gs.CLOCK.tick(gs.FPS)

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
        if shoot_cooldown > gs.BULLET_MAX_COOLDOWN:
            shoot_cooldown = 0
            spaceship.shoot(bullets)

    if keyevent[pg.K_f]:
        if blackhole_cooldown > gs.BLACKHOLE_MAX_COOLDOWN:
            blackhole_cooldown = 0
            gs.BLACKHOLE_LEFT_COOLDOWN = gs.BLACKHOLE_MAX_COOLDOWN
            gs.BLACKHOLE_READY = False
            spaceship.deathToAsteroids(blackholes)
            spaceship.isInvincible = True           

    if keyevent[pg.K_UP] or keyevent[pg.K_w]:
        spaceship.move(1)

    if keyevent[pg.K_DOWN] or keyevent[pg.K_s]:
        spaceship.move(-1)

    if asteroid_cooldown > gs.ASTEROID_MAX_COOLDOWN:
        asteroid_cooldown = 0

        asteroid_x = 0
        asteroid_y = 0

        # random asteroid spawn point
        spawn_option = random.randint(0, 1)

        if spawn_option == 0:
            # randomly spawn from either sides
            asteroid_x = random.randint(0, 1) * gs.SCREEN_WIDTH
            asteroid_y = random.randint(0, gs.SCREEN_HEIGHT)
        elif spawn_option == 1:
            # randomly spawn from top or bottom
            asteroid_x = random.randint(0, gs.SCREEN_WIDTH)
            asteroid_y = random.randint(0, 1) * gs.SCREEN_HEIGHT

        asteroid = Asteroid(random.randint(0, 360), (asteroid_x, asteroid_y), random.randint(10, gs.ASTEROID_MAX_SPEED), random.randint(-gs.ASTEROID_MAX_SPEED, gs.ASTEROID_MAX_SPEED), (spaceship.x, spaceship.y), random.uniform(0.5, gs.ASTEROID_MAX_SCALE_FACTOR))
        asteroids.append(asteroid)

    for asteroid in asteroids:
        if asteroid.x > gs.SCREEN_WIDTH or asteroid.x < 0 or asteroid.y < 0 or asteroid.y > gs.SCREEN_HEIGHT or asteroid.detectHit(spaceship):
            asteroids.remove(asteroid)
        else:
            asteroid.rotate(1)
            asteroid.asteroid_fly()

            if not len(blackholes) == 0:
                asteroid.updatePosition(millisec, (0, 0), blackholes)

            asteroid.render()

    for bullet in bullets:
        if bullet.x > gs.SCREEN_WIDTH or bullet.x < 0 or bullet.y < 0 or bullet.y > gs.SCREEN_HEIGHT or bullet.detectHit(asteroids):
            bullets.remove(bullet)
        else:
            bullet.move(1)
            bullet.render()

    for blackhole in blackholes:
        if blackhole.x > gs.SCREEN_WIDTH or blackhole.x < 0 or blackhole.y < 0 or blackhole.y > gs.SCREEN_HEIGHT:
            blackholes.remove(blackhole)
            spaceship.isInvincible = False
        else:
            blackhole.rotate(1)
            blackhole.blackhole_fly()
            blackhole.detectHit(asteroids)
            blackhole.render()

    spaceship.updatePos()
    spaceship.render()
    
    hud.update()