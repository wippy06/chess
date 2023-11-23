from copy import deepcopy

def minimax(position, max_depth, weight, transpositionTable, captureCatch):
    best_move = None
    for depth in range(1, max_depth + 1):
        bestEval, alpha, beta = float("-inf"), float("-inf"), float("inf")
        moves = get_all_moves(position)
        for move in moves:
            if ("x" in str(position.board.san(move)) or "+" in str(position.board.san(move))) and depth == 1 and not captureCatch:
                depth += 1
                captureCatch = True

            position.move(move)
            evaluation = minimax_alpha_beta(position, depth - 1, weight, alpha, beta, transpositionTable, captureCatch, False)
            position.unmove()

            if evaluation > bestEval:
                bestEval = evaluation
                best_move = move

    position.move("{}".format(best_move))
    newPos = deepcopy(position)
    position.unmove()

    return newPos

def minimax_alpha_beta(position, depth, weight, alpha, beta, transpositionTable, captureCatch, maxPlayer):
    positionKey = hash(str(position.board))

    if positionKey in transpositionTable:
        return transpositionTable[positionKey]

    if depth == 0 or position.winner() is not None:
        return position.evaluate(weight)

    if maxPlayer:
        bestEval = float("-inf")
        moves = get_all_moves(position)
        for move in moves:
            position.move(move)
            evaluation = minimax_alpha_beta(position, depth - 1, weight, alpha, beta, transpositionTable, captureCatch, False)
            position.unmove()

            bestEval = max(bestEval, evaluation)
            alpha = max(alpha, bestEval)
            if beta <= alpha:
                break
        return bestEval
    else:
        bestEval = float("inf")
        moves = get_all_moves(position)
        for move in moves:
            position.move(move)
            evaluation = minimax_alpha_beta(position, depth - 1, weight, alpha, beta, transpositionTable, captureCatch, True)
            position.unmove()

            bestEval = min(bestEval, evaluation)
            beta = min(beta, bestEval)
            if beta <= alpha:
                break
        return bestEval

def get_all_moves(board):
    moveRate = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

    valid_moves = board.get_all_valid_moves()

    for move in valid_moves:
        if board.board.is_checkmate():
            moveRate[0].append(move)
        elif move.promotion:
            moveRate[1].append(move)
        elif board.board.gives_check(move):
            moveRate[2].append(move)
        elif board.board.is_capture(move):
            moveRate[3].append(move)
        elif board.board.is_castling(move):
            moveRate[4].append(move)
        else:
            moveRate[5].append(move)

    moves = sum((moveRate[i] for i in range(6)), [])

    return moves
