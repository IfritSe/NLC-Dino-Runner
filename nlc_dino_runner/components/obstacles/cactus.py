import random

from nlc_dino_runner.components.obstacles.Obstacle import Osbtacles


class Cactus(Osbtacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300