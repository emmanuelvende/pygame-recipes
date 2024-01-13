import pygame


class Entity:
    def __init__(self, pos=(0, 0), speed=(0, 0)):
        self.surface = None
        self.speed = speed
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
        self.pos = tuple(self.pos[i] + self.speed[i] * dt for i in range(len(self.pos)))

    def collide(self, other, compute_normal=False):
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
                return collision_pos, (dx, dy)
            else:
                return None, None
        else:
            return collision_pos
