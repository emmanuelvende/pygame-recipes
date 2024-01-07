import math

import pygame
from pygame.math import Vector2 as Vec

from morepygame.utils import *


def _compute_left_right(surface, start, end, head_length=None, head_angle_rad=None):
    if start == end:
        return start, start

    start, end = scr2phy((start, end), surface)
    length = (Vec(end) - Vec(start)).length()
    a = head_length if head_length else length / 5
    arrow_body_vec = Vec(end[0] - start[0], end[1] - start[1])
    pointe = -arrow_body_vec.normalize() * a
    head_angle_rad = rad2deg(head_angle_rad) if head_angle_rad else 30
    left_vec = pointe.rotate(-head_angle_rad)
    right_vec = pointe.rotate(head_angle_rad)
    left = end + left_vec
    right = end + right_vec
    left, right = phy2scr((left, right), surface)
    return left, right


def _draw_body_left_right(
    surface, color, start, end, head_length, head_angle_rad, width
):
    left, right = _compute_left_right(surface, start, end, head_length, head_angle_rad)
    pygame.draw.line(surface, color, start, end, width=width)
    pygame.draw.line(surface, color, end, left, width=width)
    pygame.draw.line(surface, color, end, right, width=width)


def draw_arrow_by_angle_rad(
    surface, start, length, width, angle, color, head_length=None, head_angle_rad=None
):
    """
    All coordinates are pygame screen coordinates. Angles are counted counter clockwise.
    """
    start = scr2phy(start, surface)
    end = Vec(start) + length * Vec(math.cos(angle), math.sin(angle))
    start, end = scr2phy((start, end), surface)

    _draw_body_left_right(
        surface, color, start, end, head_length, head_angle_rad, width
    )


def draw_arrow(
    surface, start, end, width, color, head_length=None, head_angle_rad=None
):
    """
    All coordinates are pygame screen coordinates. Angles are counted counter clockwise.
    """
    _draw_body_left_right(
        surface, color, start, end, head_length, head_angle_rad, width
    )
