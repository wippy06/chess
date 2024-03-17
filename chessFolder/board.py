import pygame
import chess
from .constants import BROWN, BEIGE, SQUARE_SIZE
from minimax.evaluate import evaluate

class Board:
    def __init__(self):
        self.board = chess.Board()
        self.board2D = self.convert_to_2d()
        self.pieceListWhite = ["R","N","B","Q","K","P"]
        self.pieceListBlack = ["r","n","b","q","k","p"]
    
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
        for row in range (8):
            #row%2 determines if first square is missed out or not
            for col in range (row % 2, 8, 2):
                pygame.draw.rect(win, BEIGE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self,move):
        self.board.push_san("{}".format(move))
        self.board2D = self.convert_to_2d()

    def unmove(self):
        self.board.pop()
        self.board2D = self.convert_to_2d()

    def draw(self,win):
        self.draw_squares(win)

        pieceItems = []
        pieceItems[0:0] = self.pieceListWhite
        pieceItems[0:0] = self.pieceListBlack

        for x in pieceItems:
            if x.isupper():
                y="_"
            else:
                y=""
            directory = "chessFolder/assets/{}{}.png".format(y,x)
            for piece in self.get_numPieces(x):
                row,col = piece
                win.blit(pygame.transform.scale(pygame.image.load(directory),(80,80)), (col*SQUARE_SIZE+10,row*SQUARE_SIZE+10))   

    def winner(self):
        if self.board.result() != "*":
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
        for row in range(8):
            for col in range(8):
                if self.board2D[row][col] == type:
                    list_of_cords.append([row,col])
        return list_of_cords
    
    def get_num_all_pieces(self):
        num = 0
        for row in range(8):
            for col in range(8):
                if self.board2D[row][col] != "." or self.board2D[row][col] != "p" or self.board2D[row][col] != "P" or self.board2D[row][col] != "k" or self.board2D[row][col] != "K":
                    num+=1
        return num

    def is_piece(self, row,col):
        isPiece = False
        colour = False
        if self.board2D[row][col] != ".":
            isPiece = True
            if self.board2D[row][col].islower():
                colour = False
            else:
                colour = True

        #returns if there is a piece and what colour that piece is
        return [isPiece, colour]

    def get_turn(self):
        #true is white
        #false is black
        return self.board.turn
    
    def get_move(self, square, valid_moves):
        #only takes co-ordinate for square
        move = None
        for x in valid_moves:
            if str(x)[2] == square[0] and str(x)[3] == square[1]:
                move = x
                break
        return move
    
    def evaluate(self, weight):
        return evaluate(weight, self)
            