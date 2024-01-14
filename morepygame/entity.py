import pygame
from pygame.math import Vector2 as Vec


class Offset:
    def __init__(self, left=0, right=0, top=0, bottom=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def __str__(self):
        return f"L: {self.left}, R: {self.right}, T: {self.top}, B: {self.bottom}"


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

    def stay_into(self, bounding_rect, allowed_offset=Offset()):
        """
        `_offset` values are the allowed offsets out of bounds.

        Example: if `top_offset == 10` then the entity is allowed to enter
        10px at the top of the bounding rect.

        A negative offset value indicates a distance to stay away from
        the corresponding bounding edge.


        """
        me_rect = self.get_rect()
        my_offset = Offset()
        my_offset.top = me_rect.top - bounding_rect.top
        my_offset.bottom = bounding_rect.bottom - me_rect.bottom
        my_offset.left = me_rect.left - bounding_rect.left
        my_offset.right = bounding_rect.right - me_rect.right
        self._shift_inside_according_to_offsets(my_offset, allowed_offset)

    def _shift_inside_according_to_offsets(self, my_offset, allowed_offset):
        dx, dy = 0, 0
        if my_offset.top + allowed_offset.top < 0:
            dy = abs(my_offset.top + allowed_offset.top)
        elif my_offset.bottom + allowed_offset.bottom < 0:
            dy = -abs(my_offset.bottom + allowed_offset.bottom)
        if my_offset.left + allowed_offset.left < 0:
            dx = abs(my_offset.left + allowed_offset.left)
        elif my_offset.right + allowed_offset.right < 0:
            dx = -abs(my_offset.right + allowed_offset.right)
        if (dx, dy) != (0, 0):
            self.pos += Vec(dx, dy)

    def stay_out_of(self, bounding_rect, allowed_offset=Offset()):
        me_rect = self.get_rect()
        my_offset = Offset()
        my_offset.top = me_rect.top - bounding_rect.bottom
        my_offset.bottom = bounding_rect.top - me_rect.bottom
        my_offset.left = me_rect.left - bounding_rect.right
        my_offset.right = bounding_rect.left - me_rect.right
        print(" " * 80, end="\r")
        print(my_offset, end="\r")
        # self._shift_outside_according_to_offsets(my_offset, allowed_offset)

    def _shift_outside_according_to_offsets(self, my_offset, allowed_offset):
        dx, dy = 0, 0
        if my_offset.top + allowed_offset.top < 0:
            dy = abs(my_offset.top + allowed_offset.top)
        if my_offset.bottom + allowed_offset.bottom < 0:
            dy = -abs(my_offset.top + allowed_offset.top)
        if my_offset.left + allowed_offset.left < 0:
            dx = abs(my_offset.left + allowed_offset.left)
        if my_offset.right + allowed_offset.right < 0:
            dx = -abs(my_offset.right + allowed_offset.right)
        if (dx, dy) != (0, 0):
            self.pos += Vec(dx, dy)

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
