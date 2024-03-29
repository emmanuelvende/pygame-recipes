import pygame
from pygame.math import Vector2 as Vec


class Entity:
    def __init__(self, pos=(0, 0), speed=(0, 0)):
        """
        `speed` : can be either 2-items tuple or `pygame.math.Vector2d`
        """
        self.surface = None
        self.speed_vec = Vec(speed)
        self.pos = Vec(pos)

    @property
    def pos(self):
        return self._pos_vec.copy()  # return a copy because if returning the reference
        # then one can change the actual vector through this reference!

    @pos.setter
    def pos(self, newpos):
        self._pos_vec = Vec(newpos)
        if self.surface:
            center = self.surface.get_rect().center
        else:
            center = self._pos_vec

        self._display_pos = tuple(
            self.pos[i] - center[i] for i in range(len(self._pos_vec))
        )

    def get_rect(self):
        """
        Return a `pygame.Rect` indicating where the `self.surface` is displayed.
        If `self.surface` is `None` then a 0-width, 0-height rect positionned at the
        entity pos is returned.
        """
        if self.surface:
            w, h = self.surface.get_width(), self.surface.get_height()
            lefttop = self._display_pos
            return pygame.Rect(lefttop, (w, h))
        else:
            return pygame.Rect(self._pos_vec, (0, 0))

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
