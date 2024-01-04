from .eval_constants import*

def evaluate(weight, board):
    pawnAttack = p_attack_black(board)-p_attack_white(board)

    pieceProtect = piece_protect(board)

    pieceSquareTable = 0
    for x in board.pieceListBlack:
        pieceSquareTable += piece_square_table(board,x)
    for x in board.pieceListWhite:
        pieceSquareTable -= piece_square_table(board,x)

    pieceValue = 0
    for x in board.pieceListBlack:
        if x == "k":
            continue
        pieceValue += piece_value(board,x)

    for x in board.pieceListWhite:
        if x == "K":
            continue
        pieceValue -= piece_value(board,x)
    
    result = 0
    resultMult = 1
    if board.winner() == "white wins":
        return(float("-inf"))
    elif board.winner() == "black wins":
        return(float("inf"))
    elif board.winner() == "draw":
        return 0

    return (pieceValue*weight[0] + pieceSquareTable*weight[1] + pawnAttack*weight[2] + pieceProtect*weight[3] + result)*resultMult

def piece_square_table(board, type):

    pieces = board.get_numPieces(type)

    if type == "R":
        type =  rookEvalWhite   
    elif type == "N":
        type =  knightEval
    elif type == "B":
        type =  bishopEvalWhite
    elif type == "Q":
        type =  queenEval
    elif type == "K" and board.get_num_all_pieces() > endgame:
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
    elif type == "k" and board.get_num_all_pieces() > endgame:
        type =  kingEvalBlack
    elif type == "p":
        type = pawnEvalBlack
    elif type == "k" and board.get_num_all_pieces() <= endgame:
        type =  kingEvalEndGameBlack
    elif type == "K" and board.get_num_all_pieces() <= endgame:
        type =  kingEvalEndGameWhite
    
    value = 0
    for x in pieces:
        value += type[x[0]][x[1]]

    return value

def piece_value(board, type):

    pieces = board.get_numPieces(type)

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

def p_attack_black(board):
    attacked = board.get_numPieces("P")
    value = 0
    catch = False

    for x in attacked:
        x = [x[0]-1, x[1]+1]
        if x[1]==8:
            x[1] = x[1]-2
            catch == True
        if x in board.get_numPieces("r"):
            value -= 250
        if x in board.get_numPieces("q"):
            value -= 450
        if x in board.get_numPieces("b"):
            value -= 160
        if x in board.get_numPieces("n"):
            value -= 150
        if catch:
            continue
        x = [x[0], x[1]-2]    
        if x[1]==-1:
            x[1] = 1       
        if x in board.get_numPieces("r"):
            value -= 250
        if x in board.get_numPieces("q"):
            value -= 450
        if x in board.get_numPieces("b"):
            value -= 160
        if x in board.get_numPieces("n"):
            value -= 150
    
    if board.get_turn():
        return value
    else:
        return 0

def p_attack_white(board):
    attacked = board.get_numPieces("p")
    value = 0
    catch = False
    for x in attacked:
        x = [x[0]+1, x[1]+1]
        if x[1]==8:
            x[1] = x[1]-2
            catch == True
        if x in board.get_numPieces("R"):
            value -= 250
        if x in board.get_numPieces("Q"):
            value -= 450
        if x in board.get_numPieces("B"):
            value -= 160
        if x in board.get_numPieces("N"):
            value -= 150
        if catch:
            continue
        x = [x[0], x[1]-2]
        if x[1]==-1:
            x[1] = 1
        if x in board.get_numPieces("R"):
            value -= 250
        if x in board.get_numPieces("Q"):
            value -= 450
        if x in board.get_numPieces("B"):
            value -= 160
        if x in board.get_numPieces("N"):
            value -= 150

    if board.get_turn():
        return 0
    else:
        return value

def piece_protect(board):
    moves = board.get_all_valid_moves()

    moveDestinations = []

    piecesWhite = []
    piecesBlack = []

    whiteScore = 0
    blackScore = 0

    for x in board.pieceListWhite:
        piecesWhite = piecesWhite + board.get_numPieces(x)
    for x in board.pieceListBlack:
        piecesBlack = piecesBlack + board.get_numPieces(x)

    if moves != None and moves != []:
        for move in moves:
            row = 8 - int(str(move)[3])
            col = ord(str(move)[2])-97
            moveDestinations.append([row,col])

    for piece in piecesWhite:
        if piece not in moveDestinations:
            whiteScore += 1

    for piece in piecesBlack:
        if piece not in moveDestinations:
            blackScore += 1

    #print(-(blackScore-whiteScore))

    return (blackScore-whiteScore)*50
