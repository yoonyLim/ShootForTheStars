import os
import pygame as pg
import content.game_state as gs
from content.assets.ui.textbox import TextBox
from content.utilities import tools

class PlayerHUD():
    def __init__(self):
        self.sprite = pg.image.load(os.path.join("content", "assets", "sprites", "heart.png"))
        self.start_position = (30, 30)
        self.lives = gs.SPACESHIP_LIVES
        self.surface = pg.Surface(self.sprite.get_size(), pg.SRCALPHA)

    def render(self):
        for i in range(gs.SPACESHIP_LIVES):
            gs.SCREEN.blit(self.surface, (self.start_position[0] + i * self.sprite.get_width(), 30))
            self.surface.blit(self.sprite, (0, 0))

        scoreText = TextBox(30, 100, "FINAL SCORE: " + str(gs.SCORE), gs.FONT_FAMILY, gs.BUTTON_FONT_SIZE, gs.GOLD, "topleft")
        blackholeReadyText = TextBox(gs.SCREEN_WIDTH / 2, 100, "BLACKHOLE READY TO USE! [F]", gs.FONT_FAMILY, gs.BUTTON_FONT_SIZE, gs.GOLD)
        blackholeLeftCooldownText = TextBox(gs.SCREEN_WIDTH / 2, 100, str(gs.BLACKHOLE_LEFT_COOLDOWN // 1000 + 1) + " SECs LEFT FOR BLACKHOLE", gs.FONT_FAMILY, gs.BUTTON_FONT_SIZE, gs.GOLD)

        tools.updateTxtBoxes([scoreText])

        if gs.BLACKHOLE_READY:
            tools.updateTxtBoxes([blackholeReadyText])
        else:
            tools.updateTxtBoxes([blackholeLeftCooldownText])


playerHUD = PlayerHUD()

def update():
    global palyerHUD

    playerHUD.render()