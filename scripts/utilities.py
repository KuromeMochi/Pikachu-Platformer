import pygame
import os

IMAGE_PATH = "data/images/"

def load_image(path):
    image = pygame.image.load(IMAGE_PATH + path).convert() # use convert to convert the representation of image for pygame, better for rendering
    image.set_colorkey((0, 0, 0))
    return image

def load_images(path):
    images = []
    for image_name in sorted(os.listdir(IMAGE_PATH + path)):
        images.append(load_image(path + "/" + image_name))
    return images

class Animation:
    def __init__(self, animate_images, image_duration = 5, loop = True):
        """
        Adds animation
        :param animate_images: a list of images we want to animate e.g. all the images relating to a character
        :param image_duration: how long each image will last for - each frame same duration, can set up a system with math etc.
        :param loop: will loop through animation, set to True by default as we want it to be animated all the time.
        """
        self.animate_images = animate_images
        self.image_duration = image_duration
        self.loop = loop
        self.done = False
        self.frame = 0 # frame of the game

    def copy(self):
        return Animation(self.animate_images, self.image_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.animate_images)) # forces to loop after reaching end
        else:
            self.frame = min(self.frame + 1, self.image_duration * len(self.animate_images) - 1)


    def image(self):

        return self.animate_images[int(self.frame / self.image_duration)]


