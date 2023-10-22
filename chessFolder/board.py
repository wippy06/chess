import pygame
import chess
from .constants import BROWN, ROWS, BEIGE, SQUARE_SIZE, AI, BLACK, WEIGHT0
from .eval_constants import*

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
        for row in range (ROWS):
            #row%2 determines if first square is missed out or not
            for col in range (row % 2, ROWS, 2):
                pygame.draw.rect(win, BEIGE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self,move):
        self.board.push_san("{}".format(move))
        self.board2D = self.convert_to_2d()

    def draw(self,win):
        self.draw_squares(win)

        for x in [*self.pieceListWhite, *self.pieceListBlack]:
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
        print(self.evaluate(WEIGHT0))
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
        for row in range(len(self.board2D)):
            for col in range(len(self.board2D[row])):
                if self.board2D[row][col] == type:
                    list_of_cords.append([row,col])
        return list_of_cords

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

        pawnAttack = self.p_attack_black()-self.p_attack_white()

        pieceSquareTable = 0
        for x in self.pieceListBlack:
            pieceSquareTable += self.piece_square_table(x)
        for x in self.pieceListWhite:
            pieceSquareTable -= self.piece_square_table(x)

        pieceValue = 0
        for x in self.pieceListBlack:
            if x == "k":
                continue
            pieceValue += self.piece_value(x)


        for x in self.pieceListWhite:
            if x == "K":
                continue
            pieceValue -= self.piece_value(x)
        
        result = 0
        if self.winner() == "white wins":
            result = -999999999999999999999999999
        elif self.winner() == "black wins":
            result = 999999999999999999999999999
        elif self.winner() == "draw":
            if pieceValue*weight[0] + pieceSquareTable*weight[1] + pawnAttack*weight[2] > 0:
                result = -300
            else:
                result = 300

        return pieceValue*weight[0] + pieceSquareTable*weight[1] + pawnAttack*weight[2] + result

    def piece_square_table(self, type):

        pieces = self.get_numPieces(type)

        if type == "R":
            type =  rookEvalWhite   
        elif type == "N":
            type =  knightEval
        elif type == "B":
            type =  bishopEvalWhite
        elif type == "Q":
            type =  queenEval
        elif type == "K":
            type =  kingEvalWhite
        elif type == "P":
            type =  pawnEvalWhite
        elif type == "r":
            type =  rookEvalBlack
        elif type == "n":
            type =  knightEval
        elif type == "b":
            type =  bishopEvalBlack
        elif type == "q":
            type =  queenEval
        elif type == "k":
            type =  kingEvalBlack
        elif type == "p":
            type = pawnEvalBlack
        elif type == "k_end":
            type =  kingEvalEndGameBlack
        else:
            type =  kingEvalEndGameWhite
        
        value = 0
        for x in pieces:
            value += type[x[0]][x[1]]

        return value
    
    def piece_value(self, type):

        pieces = self.get_numPieces(type)

        if type == "R" or type == "r":
            type =  rookValue
        elif type == "N" or type == "n":
            type =  knightValue
        elif type == "B" or type == "b":
            type =  bishopValue
        elif type == "Q" or type == "q":
            type =  queenValue
        else:
            type = pawnValue
        
        return len(pieces)*type

    def p_attack_black(self):
        attacked = self.get_numPieces("P")
        value = 0
        catch = False
        for x in attacked:
            x = [x[0]-1, x[1]+1]
            if x[1]==8:
                x[1] = x[1]-2
            if x in self.get_numPieces("r"):
                value -= 250
            if x in self.get_numPieces("q"):
                value -= 450
            if x in self.get_numPieces("b"):
                value -= 160
            if x in self.get_numPieces("n"):
                value -= 150
            if catch:
                continue
            x = [x[0], x[1]-2]    
            if x[1]==-1:
                x[1] = 1       
            if x in self.get_numPieces("r"):
                value -= 250
            if x in self.get_numPieces("q"):
                value -= 450
            if x in self.get_numPieces("b"):
                value -= 160
            if x in self.get_numPieces("n"):
                value -= 150


        return value
    
    def p_attack_white(self):
        attacked = self.get_numPieces("p")
        value = 0
        catch = False
        for x in attacked:
            x = [x[0]+1, x[1]+1]
            if x[1]==8:
                x[1] = x[1]-2
                catch == True
            if x in self.get_numPieces("R"):
                value -= 250
            if x in self.get_numPieces("Q"):
                value -= 450
            if x in self.get_numPieces("B"):
                value -= 160
            if x in self.get_numPieces("N"):
                value -= 150
            if catch:
                continue
            x = [x[0], x[1]-2]
            if x[1]==-1:
                x[1] = 1
            if x in self.get_numPieces("R"):
                value -= 250
            if x in self.get_numPieces("Q"):
                value -= 450
            if x in self.get_numPieces("B"):
                value -= 160
            if x in self.get_numPieces("N"):
                value -= 150

        return value

            