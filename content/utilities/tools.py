import pygame as pg
import content.game_state as gs
from typing import Tuple
from content.assets.ui.textbox import TextBox
from content.assets.ui.button import Button

def setScreen(width, height):
    gs.SCREEN_WIDTH, gs.SCREEN_HEIGHT = width, height
    gs.SCREEN = pg.display.set_mode((width, height), 0, 0)

def getTxtRectSize(text: str, font_family: str, font_size: int):
    return pg.font.Font.size(pg.font.SysFont(font_family, font_size), text)

def updateTxtBoxes(txtboxes: list[TextBox]):
    for txtbox in txtboxes:
        txtbox.update()

def updateBtns(buttons: list[Button], idx: int, default_color: Tuple[int, int, int], selected_color: Tuple[int, int, int]):
    for button in buttons:
        if button.index == idx:
            button.setColor(selected_color)
        else:
            button.setColor(default_color)
        button.update()