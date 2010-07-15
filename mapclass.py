import entities
from bitstring import BitString
from constants import *

# b = BitString('0b0000')
# print(b[0])
# b[0] = 1 

class Map(object):
    def __init__(self, layout):
        self.w = 0
        self.h = 0
        self.z = 0
        self.layout = layout
        self.tiles = self.read(layout)

    def read(self, data):
        """ Reads from a string layout to convert to tiles """
        rows = data.split('\n')
        for row in rows:
            if '' in rows:
                rows.remove('')
        self.w = len(rows[0])
        self.h = len(rows)
        tiles = [[0 for x in range(self.w)] for y in range(self.h)]
        for y, row in enumerate(rows):
            for x, col in enumerate(row):
                properties = BitString('0b1000')

                # add a feature in the tile
                if col in FEATURE_TYPES:
                    if col == '+' or col == "'":
                        if col == '+':
                            opened = False
                        else:
                            opened = True
                        child = entities.Door(x, y, opened)

                # add a creature in the tile
                elif col in CREATURE_TYPES:
                    pass
                    child = None

                # specify the terrain type
                elif col in TERRAIN_TYPES:
                    if col == '#':
                        properties[PASSABLE] = 0
                        properties[BLOCK_SIGHT] = 1
                    elif col == '~':
                        properties[PASSABLE] = 0
                    child = None

                else:
                    print 'Invalid tile type. ' + col
                    return None

                tiles[y][x] = Tile(x, y, col)
                tiles[y][x].set_properties(properties)

                if child:
                    tiles[y][x].t = '.'
                    tiles[y][x].add_child(child)
                    
        return tiles


    def get_tile(self, x, y):
        try:
            return self.tiles[y][x]
        except:
            print 'Tile does not exist on ', x , ':', y
            return None

    def get_adjacent_tiles(self, tile):
        try:
            adjacent_tiles = []
            adjacent_tiles.append(self.tiles[tile.y - 1][tile.x - 1])
            adjacent_tiles.append(self.tiles[tile.y - 1][tile.x])
            adjacent_tiles.append(self.tiles[tile.y - 1][tile.x + 1])
            adjacent_tiles.append(self.tiles[tile.y][tile.x - 1])
            adjacent_tiles.append(self.tiles[tile.y][tile.x + 1])
            adjacent_tiles.append(self.tiles[tile.y + 1][tile.x - 1])
            adjacent_tiles.append(self.tiles[tile.y + 1][tile.x])
            adjacent_tiles.append(self.tiles[tile.y + 1][tile.x + 1])
            return adjacent_tiles
        except:
            print 'Error retrieving adjacent tiles. '
            return None

    def print_map(self):
        for row in self.tiles:
            for col in row:
                print col.t,
            print

    def __str__(self):
        return self.layout
    

class Tile(object):
    #properties
    #passable, illuminated, explored, blocks sight
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        self.color = None
        self.properties = BitString('0b1000')
        self.children = [] # list of monsters or items on the tile
        self.feature = None

    def add_child(self, entity):
        # can only add a child when there is no feature already occupying
        # and only when the tile is passable
        if ((not self.feature and self.properties[PASSABLE]) 
            or isinstance(entity, entities.Cursor)):

            if isinstance(entity, entities.Feature):
                self.feature = entity
            else:
                self.children.append(entity)
            entity.tile = self
            entity.update_tile()
        else:
            print 'Cannot add child in tile ' , entity.x, ":", entity.y

    def remove_child(self, entity):
        try:
            if isinstance(entity, entities.Feature):
                self.feature = None
                # TODO: update properties 
            else:
                self.children.remove(entity)
                self.properties[PASSABLE] = 1
                for child in self.children:
                    child.update_tile()
            entity.tile = None
        except:
            print 'No child ' + entity + ' in tile ' , x, " : ", y

    def set_properties(self, properties):
        if isinstance(properties, BitString):
            self.properties = properties

    def __str__(self):
        if not self.children:
            return self.t
        else:
            return self.children[len(self.children) - 1].t

