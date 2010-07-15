# TODO: turns not working right. change the main loop DONE?
# TODO: overlay objects on the map, they are not part of the game, just visual
#           i.e., cursors, notifications, etc DONE
# TODO: implement opening/closing doors

import pygame
import sys
import os
import pdb
from pygame.locals import *
from entities import Player, Cursor
from mapclass import Map
from stage import Stage
from fontsheet import Fontsheet
from maptest import data
from constants import *
from utils import get_area_around_entity

TILE_WIDTH = 16
TILE_HEIGHT = 16
MAP_WIDTH = 0
MAP_HEIGHT = 0
VIEW_SIZE = 16

STATES = ['MOVEMENT', 'OPENING', 'SHOOTING']
STATE_MOVEMENT = 0
STATE_OPENING = 1
STATE_SHOOTING = 2
STATE_TARGETTING = 3
state = STATE_MOVEMENT

testmap = data

pygame.init()

p = Player(3,3,'John')
m = Map(testmap)
cursor = None
MAP_WIDTH = m.w
MAP_HEIGHT = m.h

stage = Stage(m, TILE_WIDTH, TILE_HEIGHT)
stage.add_child(p)

fontsheet = Fontsheet(os.path.join("tiles", "consolas_unicode_16x16.png"), TILE_WIDTH, TILE_HEIGHT)

if __name__ == '__main__':
    screen = pygame.display.set_mode((400,400))
    screen.fill(pygame.Color(255, 255, 255, 0))
    area = get_area_around_entity(p, VIEW_SIZE, VIEW_SIZE, MAP_WIDTH, MAP_HEIGHT)
    stage.render(area, screen, fontsheet)
    pygame.display.update()
    while 1:
        #for e in pygame.event.get():
        stage.new_turn()
        while stage.check_turn():
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_t:
                    state = STATE_TARGETTING
                    print 'Entering targetting state. '
                elif e.key == pygame.K_ESCAPE:
                    if state <> STATE_MOVEMENT:
                        state = STATE_MOVEMENT
                        print 'Entering movement state. '
                        try:
                            stage.remove_overlay(cursor)
                            cursor = None
                        except:
                            print 'No cursor created. '

                if state == STATE_MOVEMENT:
                    if e.key == pygame.K_LEFT:
                        p.move(LEFT)
                    elif e.key == pygame.K_RIGHT:
                        p.move(RIGHT)
                    elif e.key == pygame.K_DOWN:
                        p.move(DOWN)
                    elif e.key == pygame.K_UP:
                        p.move(UP)
                    elif e.key == pygame.K_o:
                        adjacent_tiles = stage.mapobj.get_adjacent_tiles(p.tile)
                    elif e.key == pygame.K_d:
                        coords = p.destroy()
                        print coords
                elif state == STATE_TARGETTING:
                    # create cursor object
                    if not cursor:
                        cursor = Cursor(p.x, p.y)
                        stage.add_overlay(cursor)
                        print 'Cusror created.'
                    if e.key == pygame.K_LEFT:
                        cursor.move(LEFT)
                    elif e.key == pygame.K_RIGHT:
                        cursor.move(RIGHT)
                    elif e.key == pygame.K_DOWN:
                        cursor.move(DOWN)
                    elif e.key == pygame.K_UP:
                        cursor.move(UP)

            screen.fill(pygame.Color(255, 255, 255, 0))
            area = get_area_around_entity(p, VIEW_SIZE, VIEW_SIZE, MAP_WIDTH, MAP_HEIGHT)
            stage.render(area, screen, fontsheet)
            pygame.display.update()
            #pdb.set_trace()
        print 'Turn ended. '
        #stage.t_print()
        # trigger new turn

