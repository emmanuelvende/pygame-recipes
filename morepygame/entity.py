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
        return self._pos_vec

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
        Return a `pygame.Rect` indicating 
        """
        if self.surface:
            w, h = self.surface.get_width(), self.surface.get_height()
            lefttop = self._display_pos
            return pygame.Rect(lefttop, (w, h))
        else:
            return pygame.Rect(self._pos_vec, (0, 0))

    def stays_into_bounds(
        self,
        bounding_rect,
        left_offset=0,
        right_offset=0,
        top_offset=0,
        bottom_offset=0,
    ):
        """
        `_offset` values are the allowed offsets out of bounds.

        Example: if `top_offset == 10` then the entity is allowed to enter 
        10px at the top of the bounding rect.

        A negative offset value indicates a distance to stay away from
        the corresponding bounding edge.
        """
        me_rect = self.get_rect()
        my_offset_top = me_rect.top - bounding_rect.top
        my_offset_bottom = bounding_rect.bottom - me_rect.bottom
        my_offset_left = me_rect.left - bounding_rect.left
        my_offset_right = bounding_rect.right - me_rect.right

        dx, dy = 0, 0
        if my_offset_top + top_offset < 0:
            dy = abs(my_offset_top + top_offset)
        elif my_offset_bottom + bottom_offset < 0:
            dy = -abs(my_offset_bottom + bottom_offset)
        if my_offset_left + left_offset < 0:
            dx = abs(my_offset_left + left_offset)
        elif my_offset_right + right_offset < 0:
            dx = -abs(my_offset_right + right_offset)
        if (dx, dy) != (0, 0):
            self.pos += Vec(dx, dy)

    def stay_out_of_bounds(self, bounding_rect):
        pass


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
