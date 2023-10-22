import pygame
from .constants import WHITE, BLACK, BLUE, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self,win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.valid_moves = None

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, square, row, col):
        #if something is selected try to move unless selection is invalid
        if self.selected:
            result = self._move(square,row,col)
            if not result:
                self.selected=None
                self.select(square)
           
        piece = self.board.is_piece(row,col)
        #add turn == colour condition
        if piece[0] and self.board.get_turn == piece[1]:
            self.selected = square
            self.valid_moves = self.board.get_piece_valid_moves(square)
            return True
        
        return False

    def _move(self,square,row,col):
        move = self.board.get_move(square, self.valid_moves)
        if self.selected and move in self.valid_moves:
            self.board.move(move)
        else:
            return False      
        return True

    def draw_valid_moves(self, moves):
        #draw from get legal moves function from chess
        for move in moves:
            row = 8 - move[3]
            col = ord(move[2])-97
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)


    