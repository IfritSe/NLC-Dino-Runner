import pygame

from nlc_dino_runner.components.powerups.hammer import Hammer, HammerThrowed
from nlc_dino_runner.components.text_utils import get_centered_message
from pygame.sprite import Sprite
from nlc_dino_runner.utils.constants import \
    RUNNING, \
    DUCKING, \
    JUMPING, \
    RUNNING_SHIELD, \
    DUCKING_SHIELD, \
    JUMPING_SHIELD, \
    RUNNING_HAMMER, \
    JUMPING_HAMMER, \
    DUCKING_HAMMER, \
    SHIELD_TYPE, \
    HAMMER_TYPE, \
    DEFAULT_TYPE


class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 280
    Y_POS_DUCK = 320
    JUMP_VEL = 18

    def __init__(self):
        self.run_img = {DEFAULT_TYPE: RUNNING,
                        SHIELD_TYPE: RUNNING_SHIELD,
                        HAMMER_TYPE: RUNNING_HAMMER
                        }
        self.jump_img = {DEFAULT_TYPE: JUMPING,
                         SHIELD_TYPE: JUMPING_SHIELD,
                         HAMMER_TYPE: JUMPING_HAMMER
                        }
        self.duck_img = {DEFAULT_TYPE: DUCKING,
                         SHIELD_TYPE: DUCKING_SHIELD,
                         HAMMER_TYPE: DUCKING_HAMMER
                        }
        self.type = DEFAULT_TYPE
        self.image = self.run_img[self.type][0]

        self.shield = False
        self.shield_time_up = 0
        self.show_text = False

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL

        self.hammer = False
        self.throwing_hammer = False
        self.hammers_remain = 3
        self.hammer_throwed = HammerThrowed(self.dino_rect.y)

    def update(self, user_input):
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()

        if user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False
        elif user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_duck = False
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

        if self.step_index >= 10:
            self.step_index = 0

        if user_input[pygame.K_SPACE] and self.hammer and not self.throwing_hammer:
            self.hammer_throwed = HammerThrowed(self.dino_rect.y)
            self.throwing_hammer = True

    def run(self):
        self.image = self.run_img[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img[self.type]
        if self.jump:
            self.dino_rect.y -= self.jump_vel
            self.jump_vel -= 1

        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def check_invincibility(self, screen):
        if self.shield:
            time_to_show = round((self.shield_time_up - pygame.time.get_ticks())/1000, 1)
            if time_to_show < 0:
                self.shield = False
                if self.type == SHIELD_TYPE:
                    self.type = DEFAULT_TYPE
            else:
                if self.show_text:
                    text, text_rect = get_centered_message("Shield enabled for: " + str(time_to_show),
                                                           width=550,
                                                           height=100,
                                                           )
                    screen.blit(text, text_rect)

    def check_hammer(self, screen):
        if self.hammer:
            text, text_rect = get_centered_message("Hammers left: " + str(self.hammers_remain - 1),
                                                           width=550,
                                                           height=100,
                                                           )
            screen.blit(text, text_rect)

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))