import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 450, 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PySaga')
clock = pygame.time.Clock()


def display_text():
    font = pygame.font.Font(None, 36)
    text = font.render('PySaga', True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_text()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
