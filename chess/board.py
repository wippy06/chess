import pygame
import chess
from .constants import BROWN, ROWS, BEIGE, SQUARE_SIZE, COLS, BLACK, WHITE

class Board:
    def __init__(self):
        self.board = chess.Board()
        self.board2D = self.convert_to_2d()

        self.draw()
    
    def convert_to_2d(self):
        board_str = str(self.board).replace(" ","").replace("\n","")
        board_1D = [board_str[i:i+8] for i in range(0, len(board_str), 8)]
        board_2D = []
        for x in board_1D:
            board_2D.append([x[i:i+1] for i in range(0, len(x), 1)])
        return board_2D

    def draw_squares(self,win):
        #background colour
        win.fill(BROWN)
        #adding Beige squares in checker board pattern
        for row in range (ROWS):
            #row%2 determines if first square is missed out or not
            for col in range (row % 2, ROWS, 2):
                pygame.draw.rect(win, BEIGE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self,move):
        self.board.push_san("{}".format(move))
        self.board2D = self.convert_to_2d()

    def draw(self,win):
        self.draw_squares(win)
        # get chess board
        # create if and elif stuff
        #draw board
        pass     

    def winner(self):
        if self.board.result():
            if self.board.is_checkmate():
                if self.board.result() == "1-0":
                    return "white wins"
                else:
                    return "black wins"
            else:
                return "draw"
        else:
            return None
        

    def get_all_valid_moves(self):
        moves = []
        for x in range(len(list(self.board.legal_moves))):
            moves.append(list(self.board.legal_moves)[x])

        #returns list of moves, use index to choose move
        return moves
    
    def get_piece_valid_moves(self, square):
        #only takes co-ordinate for square
        allMoves = self.get_all_valid_moves()
        moves = []
        for x in allMoves:
            if str(x)[0] == square[0] and str(x)[1] == square[1]:
                moves.append(x)
        return moves

    
    def get_numPieces(self, type):
        #type is piece representation eg "p" for black pawn
        list_of_cords = []
        for x in range(len(self.board2D)):
            for y in range(len(self.board2D[x])):
                if self.board2D[x][y] == type:
                    list_of_cords.append((x,y))
        print(list_of_cords)