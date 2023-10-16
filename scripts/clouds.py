import pygame
import random

class Cloud:
    def __init__(self, position, image, speed, depth):
        """ Constructor
        Param:
        position: a list (can be tuple when passed in) containing the coordinates of the object
        image: the image of the asset as a list of loading images from the pygame load function (clouds)
        speed: the speed of the cloud at which the image will be moving along the screen.
        depth: the positioning of the cloud in terms of how close it is to the viewer - for parallax
        """
        self.position = list(position)
        self.image = image
        self.speed = speed
        self.depth = depth

    def update(self):
        self.position[0] += self.speed

    def render(self, surface, offset = (0, 0)):
        render_position = (self.position[0] - offset[0] * self.depth, self.position[1] - offset[1] * self.depth) # parallax effect
        # add 1st self.image.get_width() for padding so the cloud respawns when it is fully off-screen, 2nd one for avoiding render issues at (0, 0), wrapping
        surface.blit(self.image, (render_position[0] % (surface.get_width() + self.image.get_width()) - self.image.get_width(), render_position[1] % (surface.get_height() + self.image.get_height()) - self.image.get_height()))

class Clouds:
    """ Handle the multiple versions of clouds (images)"""
    def __init__(self, cloud_images, count = 16):
        self.clouds = []

        for i in range(count): # * 99999 due to modulo, the clouds will always loop to somewhere on screen
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))

        self.clouds.sort(key = lambda x: x.depth) # sorting all clouds, key argument determines how you sort things, in this case take the object by its depth  - clouds closest to the camera will be pushed to the front for rendering

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset = (0, 0)):
        for cloud in self.clouds:
            cloud.render(surface, offset=offset)