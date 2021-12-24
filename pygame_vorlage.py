import pygame, sys, random
from pygame.locals import *

pygame.init()
size = width, height = 500, 400
screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        screen.fill([255, 255, 255])
        pygame.display.flip()
