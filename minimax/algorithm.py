from copy import deepcopy

def minimax(position, depth, weight, maxPlayer, alpha, beta, transpositionTable, captureCatch):

    positionKey = hash(str(position.board))

    if positionKey in transpositionTable:
        return transpositionTable[positionKey]

    if depth == 0 or position.winner() != None:
        return position

    newPos = deepcopy(position)

    bestPos = None

    if maxPlayer:
        bestEval = float("-inf")
        moves = get_all_moves(newPos)
        for move in moves:

            #if last move was capture or check look ahead another move
            if ("x" in str(newPos.board.san(move)) or "+" in str(newPos.board.san(move))) and depth == 1 and captureCatch == False:
                depth += 1
                captureCatch = True

            newPos.move("{}".format(move))
            evaluation = minimax(newPos, depth-1, weight, False, alpha, beta, transpositionTable, captureCatch).evaluate(weight)
            bestEval = max(bestEval, evaluation)
            if bestEval == evaluation:
                bestPos = move
            newPos.unmove()

            alpha = max(alpha, bestEval)
            if beta <= alpha:
                break

            
    else:
        bestEval = float("inf")
        moves = get_all_moves(newPos)
        for move in moves:

            #if last move was capture or check look ahead another move
            if ("x" in str(newPos.board.san(move)) or "+" in str(newPos.board.san(move))) and depth == 1 and captureCatch == False:
                depth += 1
                captureCatch = True

            newPos.move("{}".format(move))
            evaluation = minimax(newPos, depth-1, weight, True, alpha, beta, transpositionTable, captureCatch).evaluate(weight)
            bestEval = min(bestEval, evaluation)
            if bestEval == evaluation:
                bestPos = move
            newPos.unmove()

            beta = min(beta, bestEval)
            if beta <= alpha:
                break 

    newPos.move("{}".format(bestPos))

    transpositionTable[positionKey] = newPos
    
    return newPos

def get_all_moves(board):
    moves = []
    moveRate0 = []
    moveRate1 = []
    moveRate2 = []
    moveRate3 = []
    moveRate4 = []
    moveRate5 = []

    valid_moves = board.get_all_valid_moves()
    for move in valid_moves:

        if board.board.is_checkmate():
            moveRate0.append(move)
        elif move.promotion:
            moveRate1.append(move)
        elif board.board.gives_check(move):
            moveRate2.append(move)
        elif board.board.is_capture(move):
            moveRate3.append(move)
        elif board.board.is_castling(move):
            moveRate4.append(move)
        else:
            moveRate5.append(move)
    moves = [*moveRate0, *moveRate1, *moveRate2, *moveRate3, *moveRate4, *moveRate5]

    return moves
