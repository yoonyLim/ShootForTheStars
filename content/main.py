import pygame as pg
import content.game_state as gs

def main():
    pg.init()

    pg.display.set_caption("Shoot for the Stars")

    while not gs.GAME_CLOSE:
        gs.SCREEN.fill(gs.BG_COLOR)
        pg.display.update()
        gs.CLOCK.tick(gs.FPS)

    pg.quit()
    quit()