import pygame
import os


pygame.init()

#Set up the display
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

#Set up colors
WHITE = (232, 235, 239)
BLACK = (125, 135, 150)
HIGHLIGHT = (0, 255, 0, 100) 

#Create the display window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyChess")


#Load chess pieces images
pieces = {}
for piece in ['wp', 'bp', 'wr', 'br', 'wn', 'bn', 'wb', 'bb', 'wq', 'bq', 'wk', 'bk']:
    image = pygame.image.load(os.path.join("pieces", piece + ".png"))
    pieces[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))



#Initialize the chessboard with pieces
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

#Function to get the valid moves for the piece wp
def MovesforWhitespawn(tablero, fila, columna):
    moves = []

    #Move forward if free
    if fila > 0 and tablero[fila - 1][columna] == '':
        moves.append((fila - 1, columna))

        #Move two if it's in the start row
        if fila == 6 and tablero[fila - 2][columna] == '':
            moves.append((fila - 2, columna))

    #Eating on the left diagonal
    if fila > 0 and columna > 0 and tablero[fila - 1][columna - 1].startswith('b'):
        moves.append((fila - 1, columna - 1))

    #Eat diagonally right
    if fila > 0 and columna < 7 and tablero[fila - 1][columna + 1].startswith('b'):
        moves.append((fila - 1, columna + 1))

    return moves

#Function to get the valid moves for the piece bp
def MovesforBlackpawn(tablero, fila, columna):
    moves = []

    #Move forward if free
    if fila < 7 and tablero[fila + 1][columna] == '':
        moves.append((fila + 1, columna))

        #Move two if it's in the start row
        if fila == 1 and tablero[fila + 2][columna] == '':
            moves.append((fila + 2, columna))

    #Eating on the left diagonal
    if fila < 7 and columna < 7 and tablero[fila + 1][columna + 1].startswith('w'):
        moves.append((fila + 1, columna + 1))

    #Eat diagonally right
    if fila < 7 and columna > 0 and tablero[fila + 1][columna - 1].startswith('w'):
        moves.append((fila + 1, columna - 1))

    return moves


#Draw the chessboard
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))




#Draw pieces on the board
def draw_pieces(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != '':
                win.blit(pieces[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))
 
 
 
#Draw valid moves                
def draw_valid_moves(win, moves):
    surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    surface.fill(HIGHLIGHT)
    for move in moves:
        row, col = move
        win.blit(surface, (col*SQUARE_SIZE, row*SQUARE_SIZE))               
                



#Main logic of the game
def main():
    selected = None
    valid_moves = []
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        draw_board(WIN)
        draw_valid_moves(WIN, valid_moves)
        draw_pieces(WIN, board)
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

                    if (row, col) in valid_moves:
                        board[row][col] = piece
                        board[prev_row][prev_col] = ''
                    
                    selected = None
                    valid_moves = []

                elif board[row][col] != '':
                    piece = board[row][col]
                    if piece == 'wp':
                        selected = (row, col)
                        valid_moves = MovesforWhitespawn(board, row, col)

                    if piece == 'bp':
                        selected = (row, col)
                        valid_moves = MovesforBlackpawn(board, row, col)

    pygame.quit()

if __name__ == "__main__":
    main()
