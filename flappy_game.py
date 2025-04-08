import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.joins("assets", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.joins("assets", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.joins("assets", "bird3.png"))),
]
PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.joins("assets", "pipe.png"))
)
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.joins("assets", "base.png"))
)
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.joins("assets", "bg.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
