# TODO: change render method to not be dependant on the player DONE

from tile_properties import *
from utils import get_area_around_entity
from entities import Player, Feature, Item, Being, Overlay

class Stage(object):
    def __init__(self, mapobj, view_w=None, view_h=None):
        self.mapobj = mapobj
        if view_w and view_h:
            self.view_area = (view_w, view_h)
        else:
            self.view_area = (mapobj.w, mapobj.h)
        self.features = []
        self.items = []
        self.beings = []
        self.overlays = []
        self.player = None
        self.area = None

    def add_overlay(self, overlay):
        if isinstance(overlay, Overlay):
            self.overlays.append(overlay)
            overlay.parent = self

    def remove_overlay(self, overlay):
        if isinstance(overlay, Overlay):
            try:
                self.overlays.remove(overlay)
                overlay.parent = None
            except:
                print 'Overlay not found. '

    def add_child(self, entity):
        if isinstance(entity, Feature):
            self.features.append(entity)
        elif isinstance(entity, Item):
            self.items.append(entity)
        elif isinstance(entity, Being):
            self.beings.append(entity)
            if isinstance(entity, Player):
                self.player = entity
        self.mapobj.get_tile(entity.x, entity.y).add_child(entity)
        entity.parent = self

    def remove_child(self, entity):
        try:
            if isinstance(entity, Feature):
                self.features.remove(entity)
            elif isinstance(entity, Item):
                self.items.remove(entity)
            elif isinstance(entity, Being):
                self.beings.remove(entity)
                if isinstance(entity, Player):
                    self.player = None

            self.mapobj.get_tile(entity.x, entity.y).remove_child(entity)
            entity.parent = None
        except:
            print 'Child not found. '

    def get_child(self, entity):
        if (entity in self.features or entity in self.items or 
        entity in self.beings):
            return entity
        else:
            return None

    #TODO: refactor this to reposition an element around
    def move_child(self, child, x, y):
        if (child in self.features or child in self.items
        or child in self.beings):
            target_tile = self.mapobj.get_tile(x, y)
            if not target_tile:
                return
            if target_tile.properties[PASSABLE]:
                child.tile.remove_child(child)
                target_tile.add_child(child)
                child.x = x
                child.y = y

    def new_turn(self):
        for being in self.beings:
            being.ap = 1

    def check_turn(self):
        # player always has the first actions
        if self.player.ap > 0:
            return self.player
        for being in self.beings:
            if being.ap > 0:
                # turn has not ended
                return being
        return None

    def examine_tile(self, tile):
        pass

    def render(self, area, display, fontsheet):
        output = []
        #self.area = get_area_around_entity(self.player,
        #                              self.view_area[0], self.view_area[1],
        #                              self.mapobj.w, self.mapobj.h)
        self.area = area

        for row in self.mapobj.tiles[self.area['start_y']:self.area['end_y']]:
            output.append(row[self.area['start_x']:self.area['end_x']])

        # draw world 
        for y, row in enumerate(output):
            for x, tile in enumerate(row):
                char = fontsheet.get_char(ord(tile.__str__()))
                display.blit(char,
                             (x * fontsheet.char_w, y * fontsheet.char_h)
                            )
        # draw overlays
        if self.overlays:
            for overlay in self.overlays:
                x = overlay.x
                y = overlay.y
                if (x in range(self.area['start_x'], self.area['end_x']) and
                y in range(self.area['start_y'], self.area['end_x'])):
                    x = x - self.area['start_x']
                    y = y - self.area['start_y']
                    char = fontsheet.get_char(ord(overlay.t))
                    display.blit(char,
                                 (x * fontsheet.char_w, y * fontsheet.char_h)
                                )



    def t_print(self):
        output = []
        start_y = self.player.y - self.view_area[1] / 2
        end_y = self.player.y + self.view_area[1] / 2
        start_x = self.player.x - self.view_area[0] / 2
        end_x = self.player.x + self.view_area[0] / 2

        if start_y < 0:
            start_y = 0
            end_y = self.view_area[1]
        elif end_y >= self.mapobj.h:
            start_y = self.mapobj.h - self.view_area[1]
            end_y = self.mapobj.h
        if start_x < 0:
            start_x = 0
            end_x = self.view_area[0]
        elif end_x >= self.mapobj.w:
            start_x = self.mapobj.w - self.view_area[0]
            end_x = self.mapobj.w

        for row in self.mapobj.tiles[start_y:end_y]:
            output.append(row[start_x:end_x])
        for row in output:
            for tile in row:
                print tile,
            print
