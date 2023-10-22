import pygame
from chess.constants import WIDTH,HEIGHT, SQUARE_SIZE
from chess.game import Game


FPS = 60

#set display size and capiton
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

def get_row_col_from_mouse(pos):
    x,y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row,col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

 
    while run:
        clock.tick(FPS)
        
        if game.winner()!=None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            
            #checks if game is shut down
            if event.type == pygame.QUIT:
                run = False
            
            #checks is mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        #draws the board        
        game.update()

    pygame.quit()

#runs the main function
main()