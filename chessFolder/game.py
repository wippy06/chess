import pygame
from .constants import BLUE, SQUARE_SIZE, WEIGHT0
from .board import Board

class Game:
    def __init__(self,win):
        self.win = win
        self.selected = None
        self.board = Board()
        self.valid_moves = []

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()      

    def winner(self):
        return self.board.winner()

    def select(self, square, row, col):
        #if something is selected try to move unless selection is invalid
        if self.selected:
            result = self._move(square)
            if not result:
                self.selected=None
                self.select(square, row, col)
           
        piece = self.board.is_piece(row,col)
        #add turn == colour condition
        if piece[0] == True and self.board.get_turn() == piece[1]:
            self.selected = square
            self.valid_moves = self.board.get_piece_valid_moves(square)
            return True
        
        return False

    def _move(self,square):
        move = self.board.get_move(square, self.valid_moves)
        if self.selected and move in self.valid_moves:
            self.board.move(move)
            self.valid_moves = []
        else:
            return False      
        return True

    def draw_valid_moves(self, moves):
        #draw from get legal moves function from chess
        if moves != None and moves != []:
            for move in moves:
                row = 8 - int(str(move)[3])
                col = ord(str(move)[2])-97
                pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def get_board(self):
        return self.board

    def ai_move(self,board):
        if self.board.board != board.board:
            self.board = board
            return True
        else:
            return False


    