import pygame
import morepygame

BG_COLOR = 16, 8, 24
W, H = 800, 600
COLOR_KEY = 17, 17, 17
RED = 248, 16, 16
YELLOW = 228, 228, 16


pygame.init()
pygame.display.set_caption("soccer")
screen = pygame.display.set_mode((W, H))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

circle_surf = pygame.Surface((200, 200))
circle_surf.fill(BG_COLOR)
pygame.draw.circle(circle_surf, RED, (100, 100), 50)
ball = morepygame.Entity()
ball.apply_surface(circle_surf, colorkey=BG_COLOR)
ball.pos = screen.get_rect().center

player = morepygame.Entity()
player.apply_image("hero.png", colorkey=COLOR_KEY)

entities = player, ball

running = True
dt = 0
while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                running = False

    player.pos = pygame.mouse.get_pos()

    for entity in entities:
        entity.display_on_surface(screen)

    collision_pos, collision_normal = player.collide(ball, compute_normal=True)
    if collision_pos:
        pygame.draw.circle(screen, YELLOW, collision_pos, 30, 3)
        pygame.draw.circle(screen, YELLOW, collision_pos, 5)
    if collision_normal:
        normal_vec = pygame.math.Vector2(collision_normal)
        collision_arrow_vec = normal_vec + collision_pos
        morepygame.draw_arrow(screen, collision_pos, collision_arrow_vec, 3, YELLOW)

    pygame.display.flip()

    dt = clock.tick(60)

    ball.move(dt)
