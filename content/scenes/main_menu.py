import pygame as pg
import content.game_state as gs
from content.assets.ui.textbox import TextBox
from content.assets.ui.button import Button
from content.utilities import tools

def update():
    gs.MOUSE_POS = pg.mouse.get_pos()

    # initialize title
    TITLE = TextBox(gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 4, "SHOOT FOR THE STARS", gs.FONT_FAMILY, gs.TITLE_FONT_SIZE, gs.TITLE_COLOR)

    # initialize buttons
    PLAY_BTN = Button(gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 2, "PLAY", gs.FONT_FAMILY, gs.BUTTON_FONT_SIZE, gs.BUTTON_DEFAULT_COLOR, 0)
    QUIT_BTN = Button(gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 2 + tools.getTxtRectSize("PLAY", gs.FONT_FAMILY, gs.BUTTON_FONT_SIZE)[1] * 2, "QUIT", gs.FONT_FAMILY, gs.BUTTON_FONT_SIZE, gs.BUTTON_DEFAULT_COLOR, 1)
    LIST_BTNS = [PLAY_BTN, QUIT_BTN]

    # get input
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                gs.GAME_CLOSE = True
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                gs.MAIN_MENU_CURRENT_OPTION_INDEX = (gs.MAIN_MENU_CURRENT_OPTION_INDEX + 1) % len(LIST_BTNS)
            elif event.key == pg.K_UP or event.key == pg.K_w:
                gs.MAIN_MENU_CURRENT_OPTION_INDEX = (gs.MAIN_MENU_CURRENT_OPTION_INDEX + len(LIST_BTNS) - 1) % len(LIST_BTNS)
            elif event.key == pg.K_RETURN:
                gs.CURRENT_SCENE_INDEX = gs.MAIN_MENU_CURRENT_OPTION_INDEX + 1
                gs.MAIN_MENU_CURRENT_OPTION_INDEX = 0
        elif event.type == pg.MOUSEBUTTONDOWN:
            if PLAY_BTN.checkForInput(gs.MOUSE_POS):
                gs.CURRENT_SCENE_INDEX = 1
                gs.MAIN_MENU_CURRENT_OPTION_INDEX = 0
            elif QUIT_BTN.checkForInput(gs.MOUSE_POS):
                gs.CURRENT_SCENE_INDEX = 2
                gs.MAIN_MENU_CURRENT_OPTION_INDEX = 0
        
        if gs.CURRENT_SCENE_INDEX == 0:
            gs.FIRST_GAME_LOOP = True

    tools.updateTxtBoxes([TITLE])
    tools.updateBtns(LIST_BTNS, gs.MAIN_MENU_CURRENT_OPTION_INDEX, gs.BUTTON_DEFAULT_COLOR, gs.BUTTON_SELECTED_COLOR)