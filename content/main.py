import pygame as pg
import content.game_state as gs
import content.scenes.main_menu as main_menu_scene
import content.scenes.play_screen as play_scene
import content.scenes.quit as quit_scene

def main():
    pg.init()

    pg.display.set_caption("Shoot for the Stars")

    LIST_SCENES = [main_menu_scene, play_scene, quit_scene]

    while not gs.GAME_CLOSE:
        gs.SCREEN.fill(gs.BG_COLOR)
        gs.SCREEN.blit(gs.BG, (0, 0))

        LIST_SCENES[gs.CURRENT_SCENE_INDEX].update()

        pg.display.update()
        gs.CLOCK.tick(gs.FPS)

    pg.quit()
    quit()