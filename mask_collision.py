import pygame

import morepygame

BG_COLOR = 16, 8, 24
BG_COLOR_ALT = 128, 96, 24
W, H = 800, 600
RED = 248, 16, 16
YELLOW = 228, 228, 16
COLOR_KEY = 17, 17, 17


def substract_pos(pos_a, pos_b):
    return tuple(pos_a[i] - pos_b[i] for i in range(len(pos_a)))


def add_pos(pos_a, pos_b):
    return tuple(pos_a[i] + pos_b[i] for i in range(len(pos_a)))


def collision_normal(mask, other, offset):
    x, y = offset
    dx = mask.overlap_area(other, (x + 1, y)) - mask.overlap_area(other, (x - 1, y))
    dy = mask.overlap_area(other, (x, y + 1)) - mask.overlap_area(other, (x, y - 1))
    return dx, dy


pygame.init()
pygame.display.set_caption("template")
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

pygame.mouse.set_visible(0)


hero_surf = pygame.image.load("img1.png")
hero_surf.set_colorkey(COLOR_KEY)
hero_mask = pygame.mask.from_surface(hero_surf)

circle_surf = pygame.Surface((200, 200))
circle_surf.fill(BG_COLOR)
pygame.draw.circle(circle_surf, RED, (100, 100), 50)
circle_surf.set_colorkey(BG_COLOR)
circle_mask = pygame.mask.from_surface(circle_surf)

bg_color = BG_COLOR
running = True
while running:
    screen.fill(bg_color)

    circle_pos = 100, 100

    screen.blit(circle_surf, circle_pos)

    hero_pos = pygame.mouse.get_pos()
    screen.blit(hero_surf, hero_pos)

    screen.blit(circle_mask.to_surface(), (0, 400))
    screen.blit(hero_mask.to_surface(), (250, 400))

    offset = tuple(hero_pos[i] - circle_pos[i] for i in range(len(hero_pos)))
    overlap_mask = circle_mask.overlap_mask(hero_mask, offset)

    screen.blit(overlap_mask.to_surface(), (400, 400))

    overlap_pos = circle_mask.overlap(hero_mask, offset)

    if overlap_pos:
        collision_pos = add_pos(circle_pos, overlap_pos)
        pygame.draw.circle(screen, YELLOW, collision_pos, 30, 3)
        pygame.draw.circle(screen, YELLOW, collision_pos, 5)
        bg_color = BG_COLOR_ALT

        normal = collision_normal(circle_mask, hero_mask, offset)
        normal_vec = pygame.math.Vector2(normal)
        collision_arrow_vec = normal_vec + collision_pos
        morepygame.draw_arrow(screen, collision_pos, collision_arrow_vec, 3, YELLOW)
    else:
        bg_color = BG_COLOR

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                show_masks = not show_masks

    pygame.display.flip()
