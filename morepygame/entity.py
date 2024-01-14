import pygame
from pygame.math import Vector2 as Vec


class Entity:
    def __init__(self, pos=(0, 0), speed=(0, 0)):
        """
        `speed` : can be either 2-items tuple or `pygame.math.Vector2d`
        """
        self.surface = None
        self.speed_vec = Vec(speed)
        self.pos = pos

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pp):
        self._pos = pp
        if self.surface:
            center = self.surface.get_rect().center
        else:
            center = self._pos

        self._display_pos = tuple(
            self.pos[i] - center[i] for i in range(len(self._pos))
        )

    def stays_into_bounds(self, bounding_rect, x_offset=0, y_offset=0):
        """
        x_offset and y_offset shall be positive
        """
        if x_offset < 0 or y_offset < 0:
            raise ArithmeticError("x_offset and y_offset cannot be negative")
        if self.surface:
            w, h = self.surface.get_width(), self.surface.get_height()
            lefttop = self._display_pos
            me_rect = pygame.Rect(lefttop, (w, h))
        else:
            me_rect = pygame.Rect(self._pos, (0, 0))
        offset_top = me_rect.top - bounding_rect.top
        offset_bottom = bounding_rect.bottom - me_rect.bottom
        offset_left = me_rect.left - bounding_rect.left
        offset_right = bounding_rect.right - me_rect.right

        dx, dy = 0, 0
        if offset_top + y_offset < 0:
            dy = abs(offset_top + y_offset)
        elif offset_bottom + y_offset < 0:
            dy = -abs(offset_bottom + y_offset)
        if offset_left + x_offset < 0:
            dx = abs(offset_left + x_offset)
        elif offset_right + x_offset < 0:
            dx = -abs(offset_right + x_offset)
        if (dx,dy) != (0,0):
            pos_v = Vec(self.pos)
            pos_v += Vec(dx, dy)
            self.pos = pos_v[0], pos_v[1]

    def apply_image(self, img_filepath, colorkey=None):
        self.apply_surface(pygame.image.load(img_filepath), colorkey)

    def apply_surface(self, surface, colorkey=None):
        self.surface = surface
        self.surface.set_colorkey(colorkey)
        self.mask = pygame.mask.from_surface(self.surface)

    def display_on_surface(self, surface):
        surface.blit(self.surface, self._display_pos)

    def display_mask_on_surface(self, surface):
        surface.blit(self.mask.to_surface(), self._display_pos)

    def move(self, dt):
        self.pos = tuple(
            self.pos[i] + self.speed_vec[i] * dt for i in range(len(self.pos))
        )

    def collide(self, other, compute_normal=False):
        """
        If `compute_normal == True`, returns `collision_pos, collision_vec`
        else return `collision_pos`.
        Either `collision_pos` or `collision_vec` can be `None`
        """
        offset = tuple(
            other._display_pos[i] - self._display_pos[i]
            for i in range(len(self._display_pos))
        )
        overlap_pos = self.mask.overlap(other.mask, offset)
        collision_pos = (
            tuple(
                overlap_pos[i] + self._display_pos[i]
                for i in range(len(self._display_pos))
            )
            if overlap_pos
            else None
        )
        if compute_normal:
            if collision_pos:
                x, y = offset
                dx = self.mask.overlap_area(
                    other.mask, (x + 1, y)
                ) - self.mask.overlap_area(other.mask, (x - 1, y))
                dy = self.mask.overlap_area(
                    other.mask, (x, y + 1)
                ) - self.mask.overlap_area(other.mask, (x, y - 1))
                return collision_pos, Vec(dx, dy)
            else:
                return None, None
        else:
            return collision_pos
