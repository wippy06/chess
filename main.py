import pygame
from chessFolder.constants import WIDTH,HEIGHT, SQUARE_SIZE, ROWS, PLAYER, AI, AI_ON, AI_VS_AI, DEPTH, LEARN
from chessFolder.game import Game
from minimax.algorithm import minimax, get_all_moves
import time
import random

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

def playGame(weight0, weight1):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    plyCount = 0

    game.update()

    transposisitonTableWhite = {}
    transposisitonTableBlack = {}

    clock.tick(FPS)

    while run:

        if game.board.get_turn() == AI and AI_ON and game.winner() == None:
            time_start = time.perf_counter()
            new_board = minimax(game.get_board(), DEPTH, weight0, True, float("-inf"), float("+inf"), transposisitonTableBlack, False)
            time_end = time.perf_counter()
            print(time_end-time_start, new_board.board.peek())

            plyCount+=1

            game.ai_move(new_board)
            game.update()

        if game.board.get_turn() == PLAYER and AI_VS_AI and AI_ON and game.winner() == None:
            time_start = time.perf_counter()
            new_board = minimax(game.get_board(), DEPTH, weight1, False, float("-inf"), float("+inf"), transposisitonTableWhite, False)          
            time_end = time.perf_counter()
            print(time_end - time_start, new_board.board.peek())

            plyCount+=1

            game.ai_move(new_board)
            game.update()
        
        if game.winner()!=None:
            print(game.winner())
            print(game.board.board)
            run = False
            return [game.winner(), plyCount]

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                print(get_all_moves(game.get_board()))
            

            #checks if game is shut down
            if event.type == pygame.QUIT:
                run = False
                return "end"
            
            #checks is mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                square = get_square_from_row_col(row,col)
                game.select(square, row, col)
                game.update()   
        
    pygame.quit()

def main():
    run = True
    change = 2
    weight0 = []
    weight1 = []
    game_count = 0

    open('chessResults.txt', 'w').close()
    train_start = time.perf_counter()

    while run == True:
        file = open("chessResults.txt", "a")
        if change == 2:
            weight0 = [random.randint(1,100),random.randint(1,100)]
            weight1 = [random.randint(1,100),random.randint(1,100)]
        elif change == 1:
            weight1 = [random.randint(1,100),random.randint(1,100)]
        else:
            weight0 = [random.randint(1,100),random.randint(1,100)]

        time_start = time.perf_counter()
        result = playGame(weight0, weight1)
        time_end = time.perf_counter()
        time_diff = round(time_end-time_start) 

        if result=="end":
            train_end = time.perf_counter()
            train_time = round(train_end-train_start) 
            file.write("end.{}.{}".format(train_time, game_count))
            run = False
        elif result[0] == "black wins":
            game_count +=1
            change = 0
        elif result[0] == "white wins":
            game_count +=1
            change = 1
        else:
            game_count +=1
            change = 2

        if run ==True:
            resultString = "{}.{}.{}.{}.{}\n".format(result[0], weight0, weight1, time_diff, result[1])
            file.write(resultString)
        file.close()    
    print("end.{}.{}".format(train_time, game_count))       

if LEARN == True:
    main()
else:
    playGame([6,7], [6,7])