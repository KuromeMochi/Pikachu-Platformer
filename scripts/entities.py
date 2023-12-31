import pygame

class PhysicsEntity:
    def __init__(self, game, entity_type, position, size):
        """
        Constructor
        :param game: self of Game class i.e. the current reference of the instance of the game we are on right now, used to access the asset dictionary mainly.
        :param entity_type: the nature of the asset e.g. is it player, block etc - string.
        :param position: the initial or current position of the asset - tuple / list will be converted to list
        :param size: the dimensions of the object in pixels as a tuple
        """
        self.game = game
        self.type = entity_type
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

    def generate_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def update(self, tilemap, movement = (0, 0)):
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.position[0] += frame_movement[0]
        entity_rect = self.generate_rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.position[0] = entity_rect.x

        self.position[1] += frame_movement[1]
        entity_rect = self.generate_rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.position[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1) # terminal velocity

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0


    def render(self, surface, offset = (0, 0)):
        surface.blit(self.game.assets["player"], (self.position[0] - offset[0], self.position[1] - offset[1]))
