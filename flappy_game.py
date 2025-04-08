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
