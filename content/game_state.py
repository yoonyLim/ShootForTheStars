import os
import pygame as pg

## SCREEN ##
SCREEN_WIDTH = 720
SCREEN_HEIGHT = pg.display.set_mode().get_size()[1] - 100
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

## BACKGROUND ##
BG = pg.image.load(os.path.join("content", "assets", "bg", "space.jpg"))
BG.set_alpha(100)
BG = pg.transform.scale(BG, (SCREEN_HEIGHT, SCREEN_WIDTH))
BG = pg.transform.rotate(BG, 90)

## SCENES ##
CURRENT_SCENE_INDEX = 0

## MAIN MENU ##
MAIN_MENU_CURRENT_OPTION_INDEX = 0

## INPUT ##
MOUSE_POS = pg.mouse.get_pos()

## COLORS ##

#                R    G    B
GRAY         = (100, 100, 100)
CHARCOAL     = (50,   50,  50)
NAVYBLUE     = ( 60,  60, 100)
WHITE        = (255, 255, 255)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
FOREST_GREEN = ( 31, 162,  35)
BLUE         = (  0,   0, 255)
SKY_BLUE     = ( 39, 145, 251)
YELLOW       = (255, 255,   0)
ORANGE       = (255, 128,   0)
PURPLE       = (255,   0, 255)
CYAN         = (  0, 255, 255)
BLACK        = (  0,   0,   0)
NEAR_BLACK   = ( 19,  15,  48)
COMBLUE      = (233, 232, 255)
GOLD         = (255, 215,   0)

BG_COLOR = BLACK
TITLE_COLOR = GOLD
BUTTON_DEFAULT_COLOR = WHITE
BUTTON_HOVERED_COLOR = RED
BUTTON_SELECTED_COLOR = SKY_BLUE
TEXTBOX_COLOR = GRAY

## FONTS ##
FONT_FAMILY = "arial"
FONT_SIZE = 25
TITLE_FONT_SIZE = 60
BUTTON_FONT_SIZE = 40
TEXTBOX_FONT_SIZE = 32

## GAME CONDITION ##
GAME_CLOSE = False
GAME_OVER = False

## GAME SPEED ##
CLOCK = pg.time.Clock()
FPS = 30