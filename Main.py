import pygame
import os

pygame.init()


WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS


WHITE = (232, 235, 239)
BLACK = (125, 135, 150)
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyChess")



board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp'] * 8,
    [''] * 8,
    [''] * 8,
    [''] * 8,
    [''] * 8,
    ['wp'] * 8,
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
]


def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



def main():
    selected = None
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        draw_board(WIN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                if selected:
                    prev_row, prev_col = selected
                    piece = board[prev_row][prev_col]
                    board[prev_row][prev_col] = ''
                    board[row][col] = piece
                    selected = None
                elif board[row][col] != '':
                    selected = (row, col)

    pygame.quit()

if __name__ == "__main__":
    main()
