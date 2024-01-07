import pygame

BG_COLOR = 16, 8, 24
W, H = 800, 600

pygame.init()
pygame.display.set_caption("template")
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("hello world")

    pygame.display.flip()
