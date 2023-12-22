import pygame
import math


YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ALPHA_0 = 0
F = 60
W = math.pi * 2 / 10  # 1 round per 10 seconds


def apply_rotation(theta, u):
    return (
        math.cos(theta) * u[0] - math.sin(theta) * u[1],
        math.sin(theta) * u[0] + math.cos(theta) * u[1],
    )


def draw_arrow(screen, alpha):
    start = screen.get_rect().center
    length = 100
    a = 20
    beta = 30 * math.pi / 180
    end = start[0] + math.cos(alpha) * length, start[1] - math.sin(alpha) * length
    left = end[0] - a * math.cos(beta), end[1] - a * math.sin(beta)
    right = end[0] - a * math.cos(beta), end[1] + a * math.sin(beta)

    left_vector = end[0] - left[0], end[1] - left[1]
    left_vector = apply_rotation(math.pi - alpha, left_vector)

    right_vector = end[0] - right[0], end[1] - right[1]
    right_vector = apply_rotation(math.pi - alpha, right_vector)

    pygame.draw.line(screen, YELLOW, start, end, width=2)
    pygame.draw.line(
        screen, YELLOW, end, (end[0] + left_vector[0], end[1] + left_vector[1]), width=2
    )
    pygame.draw.line(
        screen,
        YELLOW,
        end,
        (end[0] + right_vector[0], end[1] + right_vector[1]),
        width=2,
    )


def display_time(screen, font, msec):
    text_surf = font.render(f"{msec/1000:.2f} sec", True, WHITE)
    screen.blit(text_surf, (10, 10))


def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.font.init()
    the_font = pygame.font.SysFont("Arial", 20)

    clock = pygame.time.Clock()

    alpha = ALPHA_0
    msec = 0

    running = True
    while running:
        screen.fill((8, 16, 16))
        draw_arrow(screen, alpha)

        display_time(screen, the_font, msec)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

        alpha += W / F

        msec += clock.tick(F)
    pygame.quit()


main()
