import pygame as pg
## SCREEN ##
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
TITLE_COLOR = GREEN
BUTTON_DEFAULT_COLOR = WHITE
BUTTON_HOVERED_COLOR = RED
BUTTON_SELECTED_COLOR = GREEN
TEXTBOX_COLOR = GRAY

## GAME CONDITION ##
GAME_CLOSE = False

## GAME SPEED ##
CLOCK = pg.time.Clock()
FPS = 30