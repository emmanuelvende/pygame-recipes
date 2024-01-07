import math

import pygame


def scr2phy(xy, surface):
    """
    Screen to physical coordinates conversion (put Y direction to up)

    Use this func when geometry with oriented angles is involved (like rotation matrixes).
    This func "flips" the Y axis to standard (as opposed to pygame's) coordinates reference.

    If xy is `tuple` or `list` then conversion is applied to all elements.

    Input type is preserved and can be (x,y) or [x,y] or Vector2(x,y)
    """

    def _scr2phy(xy, surface):
        T = type(xy)
        if T in (list, tuple, pygame.math.Vector2):
            Y = surface.get_height()
            return T(xy[0], Y - xy[1])
        else:
            raise NotImplementedError(f"Unrecognized coordinate type: '{T}'")

    T = type(xy)
    if T in (list, tuple):
        return T(map(lambda z: _scr2phy(z, surface), xy))
    else:
        return _scr2phy(xy, surface)


def phy2scr(xy, surface):
    """
    Physical to screen coordinates conversion.
    """
    return scr2phy(xy, surface)


def rad2deg(rad):
    return 180 * rad / math.pi


def deg2rad(deg):
    return math.pi * deg / 180
