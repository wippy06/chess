#size constants
WIDTH, HEIGHT = 800,800
ROWS = 8
SQUARE_SIZE = WIDTH//ROWS

#RGB colour constants
    #pieces
WHITE = True
BLACK = False
    #potential movement
BLUE = (0,0,255)
    #checker board
BEIGE = (252,227,173)
BROWN = (107, 34, 0)

#AI
AI_ON = True
AI_VS_AI = False
AI = BLACK
PLAYER = WHITE
DEPTH = 3

    #weights to calculate eval, 0 is AI, 1 is Player AI
        #[pieceValue, pieceSquareTable, pawnAttack, castlingRight] 
WEIGHT0 = [5, 1, 1, 1]
WEIGHT1 = [5, 1, 1, 1]