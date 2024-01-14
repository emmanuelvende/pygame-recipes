import pygame
import morepygame
from pygame import *
from pygame.math import Vector2 as Vec

BG_COLOR = 16, 8, 24
W, H = 800, 600
COLOR_KEY = 17, 17, 17

pygame.init()
pygame.display.set_caption("move into bounds")
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


player = morepygame.Entity((50, 50))
player.apply_image("hero.png", colorkey=COLOR_KEY)
player.pos = 100, 100

print("helo")

running = True
while running:
    screen.fill(BG_COLOR)

    ground_rect = pygame.Rect((10, 10), (500, 500))
    pygame.draw.rect(screen, (255, 255, 255), ground_rect, width=1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    keys_pressed = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys_pressed[K_LEFT]:
        dx = -1
    if keys_pressed[K_RIGHT]:
        dx = 1
    if keys_pressed[K_UP]:
        dy = -1
    if keys_pressed[K_DOWN]:
        dy = 1

    pos = Vec(player.pos)
    pos += Vec(dx, dy)
    player.pos = pos

    player.stays_into_bounds(ground_rect)

    player.display_on_surface(screen)
    rect = pygame.Rect(
        player._display_pos,
        (player.surface.get_rect().width, player.surface.get_rect().height),
    )
    pygame.draw.rect(screen, (255, 0, 0),rect, 1)

    pygame.display.flip()
