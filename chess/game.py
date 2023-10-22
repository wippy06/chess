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
        self.turn = WHITE
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self,row,col):
        #if something is selected try to move unless selection is invalid
        pass

    def draw_valid_moves(self, moves):
        #draw from get legal moves function from chess
        #pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
        pass

    def change_turn(self):
        self.valid_moves={}
        #swaps turns
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    