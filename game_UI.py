import pygame
import sys

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE
TICK = 1
CROSS = -1
EMPTY = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
C1 = (255, 0, 0)
C2 = (0, 0, 255)


def draw_chess_board(screen):
    screen.fill(WHITE)
    for x in [HEIGHT/3,HEIGHT*2/3]:
        pygame.draw.line(screen, BLACK, (x, 0), (x, WIDTH), 2)
    for y in [WIDTH/3,WIDTH*2/3]:
        pygame.draw.line(screen, BLACK, (0, y), (HEIGHT, y), 2)

def draw_cross(screen, MAP):
    for row in range(3):
        for col in range(3):
            if MAP[row][col]:
                x = row * SQUARE_SIZE + SQUARE_SIZE // 2
                y = col * SQUARE_SIZE + SQUARE_SIZE // 2
                if MAP[row][col] == 1:
                    pygame.draw.circle(screen, C1, (y, x), SQUARE_SIZE // 5)
                else:
                    pygame.draw.circle(screen, C2, (y, x), SQUARE_SIZE // 5)

def get_mouse_cell(position):
    return [position[1] // SQUARE_SIZE, position[0] // SQUARE_SIZE]

def check(MAP):
    for player in [TICK,CROSS]:
        if (any([all([MAP[x][y] == player for y in range(3)]) for x in range(3)]) 
            or any([all([MAP[x][y] == player for x in range(3)]) for y in range(3)])):
            return player
        if all([MAP[x][x] == player for x in range(3)]) or all([MAP[x][2-x] == player for x in range(3)]):
            return player
    if all([MAP[x][y] != 0 for x in range(3) for y in range(3)]):
        return 0    # 平局
    return None


def game_UI():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cross Chess Board")

    clock = pygame.time.Clock()

    put = list()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                axis = get_mouse_cell(event.pos)
                if axis not in put:
                    put.append(axis)

        draw_chess_board(screen)
        for axis in put:
            print(axis)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

def main():
    game_UI()
    
if __name__ == "__main__":
    main()
