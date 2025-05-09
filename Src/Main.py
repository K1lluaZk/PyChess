import pygame
import os
import random
import copy
import sys

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
    image = pygame.image.load(os.path.join("src/pieces", piece + ".png"))
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
def MovesforBlackspawn(tablero, fila, columna):
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


#Function to get the valid moves for the piece wr
def MovesforWhitesrook(tablero, fila, columna):
    moves = []

    # move up (fila - 1)
    for i in range(fila - 1, -1, -1):  
        if tablero[i][columna] == '':  
            moves.append((i, columna))
        elif tablero[i][columna].startswith('b'):  
            moves.append((i, columna))
            break  
        else: 
            break
        
    # Move down (fila + 1)
    for i in range(fila + 1, 8):  
        if tablero[i][columna] == '':  
            moves.append((i, columna))
        elif tablero[i][columna].startswith('b'): 
            moves.append((i, columna))
            break  
        else:  
            break

    # Move to the right (columna - 1)
    for j in range(columna - 1, -1, -1):  
        if tablero[fila][j] == '':  
            moves.append((fila, j))
        elif tablero[fila][j].startswith('b'):  
            moves.append((fila, j))
            break  
        else:  
            break

      # Move to the right (columna + 1)
    for j in range(columna + 1, 8):  
        if tablero[fila][j] == '':  
            moves.append((fila, j))
        elif tablero[fila][j].startswith('b'):  
            moves.append((fila, j))
            break  
        else:  
            break

    return moves


#Function to get the valid moves for the piece br
def MovesforBlacksrook(tablero, fila, columna):
    moves = []

    # Move up (fila - 1)
    for i in range(fila - 1, -1, -1):  
        if tablero[i][columna] == '':  
            moves.append((i, columna))
        elif tablero[i][columna].startswith('w'):  
            moves.append((i, columna))
            break  
        else:  
            break
        
    # Move down (fila + 1)
    for i in range(fila + 1, 8):  
        if tablero[i][columna] == '':  
            moves.append((i, columna))
        elif tablero[i][columna].startswith('w'):  
            moves.append((i, columna))
            break  
        else:  
            break

    # Move to the right (columna - 1)
    for j in range(columna - 1, -1, -1):  
        if tablero[fila][j] == '':  
            moves.append((fila, j))
        elif tablero[fila][j].startswith('w'):  
            moves.append((fila, j))
            break  
        else: 
            break

      # Move to the left (columna + 1)
    for j in range(columna + 1, 8): 
        if tablero[fila][j] == '':  
            moves.append((fila, j))
        elif tablero[fila][j].startswith('w'):  
            moves.append((fila, j))
            break  
        else:  
            break

    return moves

#Function to get the valid moves for the piece wn
def MovesforWhiteshorse(tablero, fila, columna):
    moves = []
    
    # Moves valids for the horse
    valid_moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]
    
    for move in valid_moves:
        new_row = fila + move[0]
        new_col = columna + move[1]
        
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            casilla = tablero[new_row][new_col]
            
            if casilla == '' or casilla.startswith('b'):
                moves.append((new_row, new_col))
    
    return moves

#Function to get the valid moves for the piece bn
def MovesforBlackshorse(tablero, fila, columna):
    moves = []
    
    # Moves valids for the horse
    valid_moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]
    
    for move in valid_moves:
        new_row = fila + move[0]
        new_col = columna + move[1]
        
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            casilla = tablero[new_row][new_col]
            
            if casilla == '' or casilla.startswith('w'):
                moves.append((new_row, new_col))
    
    return moves


#Function to get the valid moves for the piece wb
def MovesforWhitesbishop(tablero, fila, columna):
    moves = []
    
    # Moves valids (Diagonal directions)
    valid_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  

    for dir in valid_moves:
        new_row= fila + dir[0]
        new_col = columna + dir[1]

        while 0 <= new_row < 8 and 0 <= new_col < 8:
            casilla = tablero[new_row][new_col]

            if casilla == '':
                moves.append((new_row, new_col))
            elif casilla.startswith('b'):  
                moves.append((new_row, new_col))
                break  
            else:  
                break  

            new_row += dir[0]
            new_col += dir[1]

    return moves


#Function to get the valid moves for the piece bb
def MovesforBlacksbishop(tablero, fila, columna):
    moves = []
    
    # Moves valids (Diagonal directions)
    valid_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  

    for dir in valid_moves:
        new_row= fila + dir[0]
        new_col = columna + dir[1]

        while 0 <= new_row < 8 and 0 <= new_col < 8:
            casilla = tablero[new_row][new_col]

            if casilla == '':
                moves.append((new_row, new_col))
            elif casilla.startswith('w'):  
                moves.append((new_row, new_col))
                break  
            else:  
                break  

            new_row += dir[0]
            new_col += dir[1]

    return moves

#Function to get the valid moves for the piece wq
def MovesforWhitesqueen(tablero, fila, columna):
    moves = []
    moves += MovesforWhitesbishop(tablero, fila, columna)
    moves += MovesforWhitesrook(tablero, fila, columna)
    return moves

#Function to get the valid moves for the piece bq
def MovesforBlacksqueen(tablero, fila, columna):
    moves = []
    moves += MovesforBlacksbishop(tablero, fila, columna)
    moves += MovesforBlacksrook(tablero, fila, columna)
    return moves


#Function to get the valid moves for the piece wk
def MovesforWhitesking(tablero, fila, columna):
    moves = []
    valid_moves = [
        (-1, 0), (1, 0),  
        (0, -1), (0, 1),   
        (-1, -1), (-1, 1), 
        (1, -1), (1, 1)    
    ]

    for dir in valid_moves:
        new_row = fila + dir[0]
        new_col = columna + dir[1]

        if 0 <= new_row < 8 and 0 <= new_col < 8:
            casilla = tablero[new_row][new_col]

            if casilla == '' or casilla.startswith('b'):
                moves.append((new_row, new_col))
    return moves

#Function to get the valid moves for the piece bk
def MovesforBlacksking(tablero, fila, columna):
    moves = []
    valid_moves = [
        (-1, 0), (1, 0),  
        (0, -1), (0, 1),   
        (-1, -1), (-1, 1), 
        (1, -1), (1, 1)    
    ]

    for dir in valid_moves:
        new_row = fila + dir[0]
        new_col = columna + dir[1]

        if 0 <= new_row < 8 and 0 <= new_col < 8:
            casilla = tablero[new_row][new_col]

            if casilla == '' or casilla.startswith('w'):
                moves.append((new_row, new_col))
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
    for row, col in moves:
        win.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))



#Ia moves a black piece
def ia_mover_pieza_negra(tablero):
    piezas_movibles = []

    for fila in range(8):
        for columna in range(8):
            pieza = tablero[fila][columna]
            if pieza.startswith('b'):
                if pieza == 'bp':
                    moves = MovesforBlackspawn(tablero, fila, columna)
                elif pieza == 'br':
                    moves = MovesforBlacksrook(tablero, fila, columna)
                elif pieza == 'bn':
                    moves = MovesforBlackshorse(tablero, fila, columna)
                elif pieza == 'bb':
                    moves = MovesforBlacksbishop(tablero, fila, columna)
                elif pieza == 'bq':
                    moves = MovesforBlacksqueen(tablero, fila, columna)
                elif pieza == 'bk':
                    moves = MovesforBlacksking(tablero, fila, columna)
                else:
                    moves = []

                if moves:
                    piezas_movibles.append(((fila, columna), moves))

    if piezas_movibles:
        origen, posibles = random.choice(piezas_movibles)
        destino = random.choice(posibles)

        ofila, ocol = origen
        dfila, dcol = destino

        tablero[dfila][dcol] = tablero[ofila][ocol]
        tablero[ofila][ocol] = ''




#Function to verify if a player has won
def verifywinner(tablero):
    kingwhite = False
    kingblack = False

    for fila in tablero:
        for pieza in fila:
            if pieza == 'wk':
                kingwhite = True
            elif pieza == 'bk':
                kingblack = True

    if not kingwhite:
        return 'Black' 
    elif not kingblack:
        return 'White'  
    else:
        return None  
    

#Function to check if the king is in check
def enjaque(board, color):
    if color == 'w':
        rey = 'wk'
        enemigo = 'b'
    else:
        rey = 'bk'
        enemigo = 'w'

    rey_pos = None

    
    for row in range(8):
        for col in range(8):
            if board[row][col] == rey:
                rey_pos = (row, col)
                break
        if rey_pos:  
            break

    if rey_pos is None:
       return True   

    for row in range(8):
        for col in range(8):
            pieza = board[row][col]
            if pieza.startswith(enemigo):
                moves = getmoves(board, row, col, pieza)
                if rey_pos in moves:
                    return True

    return False


def getmoves(board, row, col, piece):
    if piece == 'wp':
        return MovesforWhitespawn(board, row, col)
    if piece == 'bp':
        return MovesforBlackspawn(board, row, col)
    if piece == 'wr':
        return MovesforWhitesrook(board, row, col)
    if piece == 'br':
        return MovesforBlacksrook(board, row, col)
    if piece == 'wn':
        return MovesforWhiteshorse(board, row, col)
    if piece == 'bn':
        return MovesforBlackshorse(board, row, col)
    if piece == 'wb':
        return MovesforWhitesbishop(board, row, col)
    if piece == 'bb':
        return MovesforBlacksbishop(board, row, col)
    if piece == 'wq':
        return MovesforWhitesqueen(board, row, col)
    if piece == 'bq':
        return MovesforBlacksqueen(board, row, col)
    if piece == 'wk':
        return MovesforWhitesking(board, row, col)
    if piece == 'bk':
        return MovesforBlacksking(board, row, col)
    return []


def enjaquemate(board, color):
    if not enjaque(board, color):
        return False

    for row in range(8):
        for col in range(8):
            pieza = board[row][col]
            if pieza.startswith(color):
                moves = getmoves(board, row, col, pieza)

                for move in moves:
                    temp_board = copy.deepcopy(board)
                    new_row, new_col = move
                    temp_board[new_row][new_col] = pieza
                    temp_board[row][col] = ''

                    if not enjaque(temp_board, color):
                        return False  

    return True  


#Promote the pawn to queen when it reaches the last row
def promocionar_peon(tablero, fila, columna):
    pieza = tablero[fila][columna]
    if pieza == 'wp' and fila == 0:
        tablero[fila][columna] = 'wq' 
    elif pieza == 'bp' and fila == 7:
        tablero[fila][columna] = 'bq'  

#Function to display the victory screen
def mostrar_pantalla_victoria(ganador):
   
    WIN.fill((0, 0, 0)) 

    fuente = pygame.font.SysFont('Arial', 60)
    mensaje = f"¡{ganador} gana!"
    texto = fuente.render(mensaje, True, (255, 255, 255))  

    rect_texto = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(texto, rect_texto)

    pygame.display.update()

    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

#Main logic of the game
def main():

    turn = 'w'  
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
                        
                        if piece.startswith(turn):  
                            board[row][col] = piece
                            board[prev_row][prev_col] = ''

                            if turn == 'w':
                               turn = 'b'
                                   
                               if enjaquemate(board, 'b'):
                                  mostrar_pantalla_victoria('Blanco')
                                  run = False
                                  break
        
                               ia_mover_pieza_negra(board)
                               
                               if enjaquemate(board, 'w'):
                                  mostrar_pantalla_victoria('Negro')
                                  run = False
                                  break
                              
                               turn = 'w'
                              
                              
                    
                    selected = None
                    valid_moves = []

                elif board[row][col] != '':
                    piece = board[row][col]
                    
                    if (turn == 'w' and piece.startswith('w')) or (turn == 'b' and piece.startswith('b')):
                        selected = (row, col)
                    
                    if piece == 'wp':
                        selected = (row, col)
                        valid_moves = MovesforWhitespawn(board, row, col)
                        promocionar_peon(board, row, col)
                        
                    if piece == 'bp':
                        selected = (row, col)
                        valid_moves = MovesforBlackspawn(board, row, col)
                        promocionar_peon(board, row, col)
                        
                    if piece == 'wr':
                        selected = (row, col)
                        valid_moves = MovesforWhitesrook(board, row, col)
                        
                    if piece == 'br':
                        selected = (row, col)
                        valid_moves = MovesforBlacksrook(board, row, col)    
                    
                    if piece == 'wn':
                        selected = (row, col)
                        valid_moves = MovesforWhiteshorse(board, row, col)
                        
                    if piece == 'bn':
                        selected = (row, col)
                        valid_moves = MovesforBlackshorse(board, row, col)               
                        
                    if piece == 'wb':
                        selected = (row, col)
                        valid_moves = MovesforWhitesbishop(board, row, col) 
                        
                    if piece == 'bb':
                        selected = (row, col)
                        valid_moves = MovesforBlacksbishop(board, row, col)               
                    
                    if piece == 'wq':
                        selected = (row, col)
                        valid_moves = MovesforWhitesqueen(board, row, col)               
                    
                    if piece == 'bq':
                        selected = (row, col)
                        valid_moves = MovesforBlacksqueen(board, row, col)  
                    
                    if piece == 'wk':
                        selected = (row, col)
                        valid_moves = MovesforWhitesking(board, row, col) 
                    
                    if piece == 'bk':
                        selected = (row, col)
                        valid_moves = MovesforBlacksking(board, row, col)     
                                 

    pygame.quit()

if __name__ == "__main__":
    main()
