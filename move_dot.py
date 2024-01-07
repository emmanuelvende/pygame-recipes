import pygame

BG_COLOR = 16, 8, 24
W, H = 800, 600
RED = 248, 16, 16


def draw_it(surface, pos):
    pygame.draw.circle(surface, RED, pos, 10)


pygame.init()
pygame.display.set_caption("template")
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pos = pygame.mouse.get_pos()
    draw_it(screen, pos)

    pygame.display.flip()
