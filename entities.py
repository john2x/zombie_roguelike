# TODO: destroy method, remove all references
# TODO: monsters
# TODO: player stats
# TODO: monster stats

from bitstring import BitString
from constants import *

def create_feature(x, y, t):
    if not t in FEATURE_TYPES:
        print 'Invalid feature ' + t
        return None

    if t == '+' or t == "'":
        if t == '+':
            opened = False
        else:
            opened = True
        feature = Door(x, y, opened)
    elif t == 'T':
        feature = Tree(x, y)
    return feature

# BASE CLASSES
class Entity(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.t = ''
        self.tile = None
        self.properties = BitString('0b00')
        self.color = None
        self.parent = None

    def update_tile(self):
        if self.tile:
            self.tile.properties[PASSABLE] = self.properties[PASSABLE]
            self.tile.properties[BLOCK_SIGHT] = self.properties[BLOCK_SIGHT]

    def destroy(self):
        try:
            x, y = self.x, self.y
            self.parent.remove_child(self)
            return x, y
        except:
            print 'Destroy method failed. '

    def __repr__(self):
        return self.t

class Feature(Entity):
    def __init__(self, x, y, t):
        self.t = '+'

class Item(Entity):
    # pickable, destructible, container, 
    pass

class Being(Entity):
    def __init__(self, x, y, name):
        Entity.__init__(self, x, y)
        self.name = name
        self.properties[PASSABLE] = 0
        self.ap = 1
        self.hp = 100
        self.energy = 100

    def move(self, direction):
        if self.parent:
            if direction == UP:
                x = self.x
                y = self.y - 1
            elif direction == UP_RIGHT:
                x = self.x + 1
                y = self.y - 1
            elif direction == RIGHT:
                x = self.x + 1
                y = self.y
            elif direction == DOWN_RIGHT:
                x = self.x + 1
                y = self.y + 1
            elif direction == DOWN:
                x = self.x
                y = self.y + 1
            elif direction == DOWN_LEFT:
                x = self.x - 1
                y = self.y + 1
            elif direction == LEFT:
                x = self.x - 1
                y = self.y
            elif direction == UP_LEFT:
                x = self.x - 1
                y = self.y - 1
            else:
                print 'Invalid move direction. '
                return

            target_tile = self.parent.mapobj.get_tile(x, y)
            if not target_tile:
                return
            if target_tile.properties[PASSABLE]:
                self.tile.remove_child(self)
                target_tile.add_child(self)
                self.x = x
                self.y = y
                self.ap -= .5
            else:
                #TODO: if a move failed, do not take a turn
                print 'not passable'

class Overlay(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y)

# BEINGS
class Player(Being):
    def __init__(self, x, y, name):
        Being.__init__(self, x, y, name)
        self.t = '@'
        self.weapon = 'fist'

    def attack(self, target):
        # check if in range
        pass

class Monster(Being):
    def __init__(self, x, y, namet):
        Being.__init__(self, x, y, name)
        self.t = 'z'
# FEATURES
class Door(Entity):
    def __init__(self, x, y, opened):
        Entity.__init__(self, x, y)
        self.opened = opened
        if opened:
            self.t = "'"
            self.properties[PASSABLE] = 1
            self.properties[BLOCK_SIGHT] = 0
        else:
            self.t = '+'
            self.properties[PASSABLE] = 0
            self.properties[BLOCK_SIGHT] = 1
    def open(self):
        self.opened = True
        self.t = "'"
        self.properties[PASSABLE] = 1
        self.properties[BLOCK_SIGHT] = 0
        self.update_tile()
    def close(self):
        self.opened = False
        self.t = "+"
        self.properties[PASSABLE] = 0
        self.properties[BLOCK_SIGHT] = 1
        self.update_tile()

class Cursor(Overlay):
    def __init__(self, x, y):
        Overlay.__init__(self, x, y)
        self.t = '0'

    def move(self, direction):
        if self.parent:
            if direction == UP:
                x = self.x
                y = self.y - 1
            elif direction == UP_RIGHT:
                x = self.x + 1
                y = self.y - 1
            elif direction == RIGHT:
                x = self.x + 1
                y = self.y
            elif direction == DOWN_RIGHT:
                x = self.x + 1
                y = self.y + 1
            elif direction == DOWN:
                x = self.x
                y = self.y + 1
            elif direction == DOWN_LEFT:
                x = self.x - 1
                y = self.y + 1
            elif direction == LEFT:
                x = self.x - 1
                y = self.y
            elif direction == UP_LEFT:
                x = self.x - 1
                y = self.y - 1
            else:
                print 'Invalid move direction. '
                return

            area = self.parent.area

            #if ((x >= area['start_x'] and x < area['end_x'])
            #and (y >= area['start_y'] and y < area['end_y'])):
            if (x in range(area['start_x'], area['end_x']) and
                y in range(area['start_y'], area['end_y'])):
                self.x = x
                self.y = y
    
