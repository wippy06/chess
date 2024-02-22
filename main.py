import pygame
from chessFolder.constants import WIDTH,HEIGHT, SQUARE_SIZE, ROWS, PLAYER, AI, AI_ON, AI_VS_AI, DEPTH, WEIGHT0, WEIGHT1
from chessFolder.game import Game
from minimax.algorithm import minimax, get_all_moves
import time

FPS = 60

letters = ["a","b","c","d","e","f","g","h"]

#set display size and capiton
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

def get_row_col_from_mouse(pos):
    x,y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row,col

def get_square_from_row_col(row,col):
    row = ROWS - row
    col = letters[col]

    square = "{}{}".format(col,row)

    return square

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    game.update()

    transposisitonTableWhite = {}
    transposisitonTableBlack = {}

    clock.tick(FPS)

    while run:

        if game.board.get_turn() == AI and AI_ON and game.winner() == None:
            time_start = time.perf_counter()
            new_board = minimax(game.get_board(), DEPTH, WEIGHT0, True, float("-inf"), float("+inf"), transposisitonTableBlack, False)
            time_end = time.perf_counter()
            print(time_end-time_start)

            game.ai_move(new_board)
            game.update()

        if game.board.get_turn() == PLAYER and AI_VS_AI and AI_ON and game.winner() == None:
            time_start = time.perf_counter()
            new_board = minimax(game.get_board(), DEPTH, WEIGHT1, False, float("-inf"), float("+inf"), transposisitonTableWhite, False)          
            time_end = time.perf_counter()
            print(time_end - time_start)

            game.ai_move(new_board)
            game.update()
        
        if game.winner()!=None:
            print(game.winner())
            run = False

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                print(get_all_moves(game.get_board()))
            

            #checks if game is shut down
            if event.type == pygame.QUIT:
                run = False
            
            #checks is mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                square = get_square_from_row_col(row,col)
                game.select(square, row, col)
                game.update()   
        
    pygame.quit()

#runs the main function
main()