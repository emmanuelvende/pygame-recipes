import pygame
import morepygame
import morepygame.keyboard
from pygame.math import Vector2 as Vec


def display_collision_on_surface(surface, entity, other):
    YELLOW = 228, 228, 16
    collision_pos, normal_vec = entity.collide(other, compute_normal=True)
    if collision_pos:
        pygame.draw.circle(surface, YELLOW, collision_pos, 30, 3)
        pygame.draw.circle(surface, YELLOW, collision_pos, 5)
    if normal_vec:
        collision_arrow_vec = normal_vec + collision_pos
        morepygame.draw_arrow(surface, collision_pos, collision_arrow_vec, 3, YELLOW)


def manage_bouncing(entity, other):
    _, normal_vec = entity.collide(other, compute_normal=True)
    if normal_vec:
        entity.speed_vec.reflect_ip(normal_vec)


BG_COLOR = 16, 8, 24
W, H = 800, 600
COLOR_KEY = 17, 17, 17
BALL_COLOR = 128, 222, 248
WHITE = 242, 242, 232
OFFSET = 50
GROUND_COLOR = 8, 64, 16


pygame.init()
pygame.display.set_caption("soccer")
screen = pygame.display.set_mode((W, H))

pygame.mouse.set_visible(False)
clock = pygame.time.Clock()


radius = 30
ball_surf = pygame.Surface((2 * radius, 2 * radius))
ball_surf.fill(BG_COLOR)
pygame.draw.circle(ball_surf, BALL_COLOR, ball_surf.get_rect().center, radius)
ball = morepygame.Entity(speed=(0.5, 0.25))
ball.apply_surface(ball_surf, colorkey=BG_COLOR)
ball.pos = screen.get_rect().center

player = morepygame.Entity()
player.apply_image("hero.png", colorkey=COLOR_KEY)
player.pos = 200, 200

LINE_WIDTH = 10
ground_surf = pygame.Surface((W - 2 * OFFSET, H - 2 * OFFSET))
ground_surf.fill(BG_COLOR)
pygame.draw.rect(ground_surf, WHITE, ground_surf.get_rect(), width=LINE_WIDTH)
ground = morepygame.Entity()
ground.apply_surface(ground_surf, colorkey=BG_COLOR)
ground.pos = screen.get_rect().center

ground_rect = ground.get_rect()

OFFSETS = 4 * (-LINE_WIDTH,)
INNER_OFFSET = morepygame.Offset(*OFFSETS)

entities = ground, player, ball

running = True
paused = False
display_collisions = False
dt = 0
while running:
    screen.fill(GROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                running = False
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_d:
                display_collisions = not display_collisions

    dxdy = morepygame.keyboard.get_moving_amount()
    if dxdy:
        player.pos += dxdy

    player.stays_into_bounds(ground_rect, INNER_OFFSET)

    for entity in entities:
        entity.display_on_surface(screen)

    if display_collisions:
        display_collision_on_surface(screen, player, ball)
        display_collision_on_surface(screen, ball, ground)
        display_collision_on_surface(screen, player, ground)

    manage_bouncing(ball, ground)
    manage_bouncing(ball, player)

    ball.stays_into_bounds(ground_rect, INNER_OFFSET)

    pygame.display.flip()

    dt = clock.tick(60)

    if not paused:
        ball.move(dt)
