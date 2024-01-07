import pygame
import PIL.Image

BG_COLOR = 16, 8, 24
WHITE = 248, 104, 128


pygame.init()

WH = 1024, 768  # pygame.display.list_modes()[0]


pygame.display.set_caption("super background")
screen = pygame.display.set_mode(WH)  # , flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()


background = PIL.Image.open("bg_1344x896.png")
background = background.resize(WH)
background = pygame.image.frombytes(
    background.tobytes(), background.size, background.mode
)

font = pygame.font.Font("Bahianita-Regular.ttf", 48)
texts = "Press F11 or F to toggle fullscreen", "Press ESC or Q to Quit"
texts = tuple(map(lambda text: font.render(text, False, WHITE, BG_COLOR), texts))
for text in texts:
    text.set_colorkey(BG_COLOR)


def render_texts(surface, texts, pos):
    x, y = pos
    for text in texts:
        surface.blit(text, (x, y))
        dy = text.get_size()[1]
        dy += dy // 5
        y += dy


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            if event.key in (pygame.K_f, pygame.K_F11):
                if screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode(WH)
                else:
                    pygame.display.set_mode(WH, flags=pygame.FULLSCREEN)
    screen.blit(background, (0, 0))
    render_texts(screen, texts, (100, 100))

    pygame.display.flip()
