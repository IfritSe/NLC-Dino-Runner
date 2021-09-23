import pygame
import random

from nlc_dino_runner.components.obstacles.cactus import Cactus
from nlc_dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS


class ObstaclesManager:

    def __init__(self):
        self.obstacles_list = []

    def update(self, game):
        cactus_list = [1, 2]
        print(cactus_list)
        if len(self.obstacles_list) == 0:
            cactus = random.choice(cactus_list)
            if cactus == 1:
                self.obstacles_list.append(Cactus(SMALL_CACTUS))
            elif cactus == 2:
                self.obstacles_list.append(Cactus(LARGE_CACTUS))

        for obstacle in self.obstacles_list:
            obstacle.update(game.game_speed, self.obstacles_list)
            if game.player.throwing_hammer:
                if game.player.hammer_throwed.rect.colliderect(obstacle.rect):
                    self.obstacles_list.remove(obstacle)

            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.shield:
                    self.obstacles_list.remove(obstacle)
                else:
                    if game.hearts_manager.hearts_counter > 1:
                        game.hearts_manager.hearts_counter -= 1
                        game.player.dino_rect.colliderect(obstacle.rect)
                        self.obstacles_list.remove(obstacle)
                    else:
                        pygame.time.delay(10)
                        game.playing = False
                        game.death_count += 1
                        game.game_speed = 20
                        break

    def draw(self, screen):
        for obstacle in self.obstacles_list:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles_list = []