from chessFolder.eval_constants import*

def evaluate(weight, board):
    pawnAttack = p_attack_black(board)-p_attack_white(board)

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
        result = -999999999
        resultMult = 1
    elif board.winner() == "black wins":
        result =  999999999
        resultMult = 1
    elif board.winner() == "draw":
        resultMult = 0

    return (pieceValue*weight[0] + pieceSquareTable*weight[1] + pawnAttack*weight[2] + result)*resultMult

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
    elif type == "K" and board.get_num_all_pieces() > 4:
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
    elif type == "k" and board.get_num_all_pieces() > 4:
        type =  kingEvalBlack
    elif type == "p":
        type = pawnEvalBlack
    elif type == "k" and board.get_num_all_pieces() <= 4:
        type =  kingEvalEndGameBlack
    elif type == "K" and board.get_num_all_pieces() <= 4:
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

        