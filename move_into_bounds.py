import pygame
import morepygame
import morepygame.keyboard
from pygame import *
from pygame.math import Vector2 as Vec

BG_COLOR = 16, 8, 24
W, H = 800, 600
COLOR_KEY = 17, 17, 17

pygame.init()
pygame.display.set_caption("move into bounds")
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

ground_rect = pygame.Rect((40, 40), (520, 520))
inner_rect = pygame.Rect((50, 50), (500, 500))

player = morepygame.Entity((50, 50))
player.apply_image("hero.png", colorkey=COLOR_KEY)
player.pos = 100, 200

forbidden_rect = pygame.Rect((300, 280), (100, 70))

running = True
while running:
    screen.fill(BG_COLOR)

    pygame.draw.rect(screen, (0, 255, 255), ground_rect, width=10)
    pygame.draw.rect(screen, (255, 0, 255), inner_rect, width=1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    dxdy = morepygame.keyboard.get_moving_amount()
    if dxdy:
        player.pos += dxdy

    pygame.draw.rect(screen, (255, 0, 255), forbidden_rect, width=1)

    player.stay_into(inner_rect, morepygame.Offset(-10, 0, 10, 20))
    # player.stay_into(inner_rect)
    player.stay_out_of(forbidden_rect)

    player.display_on_surface(screen)
    pygame.draw.rect(screen, (255, 0, 0), player.get_rect(), 1)

    pygame.display.flip()

    clock.tick(60)
