import pygame
import sys

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_chess_board(screen):
    screen.fill(WHITE)
    for x in [HEIGHT/3,HEIGHT*2/3]:
        pygame.draw.line(screen, BLACK, (x, 0), (x, WIDTH), 2)
    for y in [WIDTH/3,WIDTH*2/3]:
        pygame.draw.line(screen, BLACK, (0, y), (HEIGHT, y), 2)

def draw_cross(screen, row, col):
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2

    pygame.draw.line(screen, BLACK, (x - SQUARE_SIZE // 2, y), (x + SQUARE_SIZE // 2, y), 2)
    pygame.draw.line(screen, BLACK, (x, y - SQUARE_SIZE // 2), (x, y + SQUARE_SIZE // 2), 2)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cross Chess Board")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_chess_board(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
