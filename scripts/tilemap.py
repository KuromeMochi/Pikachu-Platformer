import pygame

TILE_NEARBY_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # will use this to find the 9 tiles around the player
PHYSICS_TILES = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tile_size = 16):
        """ Constructor
        Param:
        game: self of Game class i.e. the current reference of the instance of the game we are on right now, used to access the asset dictionary mainly.
        tile_size: the size of the tile in pixels (square shaped)
        """
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {}
        self.offgrid_tiles = []

        for i in range(10): # assigns key value pairs to the tile map dictionary - value is a smaller dictionary with tile information
            self.tile_map[str(3+i) + ";10"] = {"type": "grass", "variant": 1, "pos": (3 + i, 10)}
            self.tile_map["10;" + str(5+i)] = {"type": "stone", "variant": 1, "pos": (10, 5 + i)}

    def tiles_around(self, position):
        tiles = []
        tile_location = (int(position[0] // self.tile_size), int(position[1] // self.tile_size))
        for offset in TILE_NEARBY_OFFSETS: # can now generate all the tiles around that pixel
            check_location = str(tile_location[0] + offset[0]) + ";" + str(tile_location[1] + offset[1])
            if check_location in self.tile_map:
                tiles.append(self.tile_map[check_location])
        return tiles

    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(int(tile["pos"][0] * self.tile_size), int(tile["pos"][1] * self.tile_size), self.tile_size, self.tile_size))
        return rects

    def render(self, surface, offset = (0, 0)):
        # off-grid rendering
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]],
                         (tile["pos"] - offset[0], tile["pos"][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                location = str(x) + ";" + str(y)
                if location in self.tile_map:
                    tile = self.tile_map[location]
                    surface.blit(self.game.assets[tile["type"]][tile["variant"]], (
                    tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]))

        # on-grid rendering
        for location in self.tile_map:
            tile = self.tile_map[location]
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]))
