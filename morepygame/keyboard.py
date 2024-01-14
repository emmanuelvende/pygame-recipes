import pygame
from pygame.math import Vector2 as Vec


def get_moving_amount(
    key_up=pygame.K_UP,
    key_down=pygame.K_DOWN,
    key_left=pygame.K_LEFT,
    key_right=pygame.K_RIGHT,
    delta_x=5,
    delta_y=5,
):
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[key_up]:
        dy = -delta_y
    if keys[key_down]:
        dy = delta_y
    if keys[key_left]:
        dx = -delta_x
    if keys[key_right]:
        dx = delta_x
    return Vec(dx, dy)
