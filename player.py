import pygame
from pygame.constants import *

WH = 1024, 768

BG_COLOR = 16, 8, 24
PLAYER_BG_COLOR = 250, 250, 250

pygame.init()
screen = pygame.display.set_mode(WH)

bg_color = BG_COLOR

player = pygame.image.load("basket-ball-player.png")
player.set_colorkey(PLAYER_BG_COLOR)

running = True
while running:
    screen.fill(bg_color)

    pos = pygame.mouse.get_pos()
    screen.blit(player, pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (K_q, K_ESCAPE):
                running = False

    pygame.display.flip()
