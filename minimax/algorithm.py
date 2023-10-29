from copy import deepcopy

def minimax(position, depth, max_player, alpha, beta, weight):
    #position is an object
    #depth is an int to show how far to go
    #max_player checks if ai wants to maximise sore or minimise score

    if position.board.is_check()and depth == 0:
        depth += 1

    if depth == 0 or position.winner() != None:
        return position.evaluate(weight), position
    
    if max_player:
        maxEval = float("-inf")
        best_move = None
        for move in get_all_moves(position, max_player):
            evaluation = minimax(move, depth-1, False, alpha, beta, weight)[0]
            maxEval = max(maxEval,evaluation)
                         
            if maxEval == evaluation:
                best_move = move

            alpha = max( alpha, maxEval)
            if beta <= alpha:
                #pass
                break

        return maxEval, best_move
    
    else:
        minEval = float("inf")
        best_move = None
        for move in get_all_moves(position, max_player):
            evaluation = minimax(move, depth-1, True, alpha, beta, weight)[0]
            minEval = min(minEval,evaluation)

            if minEval == evaluation:
                best_move = move  
            
            beta = min( beta, minEval)
            if beta <= alpha:
                #pass
                break    

        return minEval, best_move

def simulate_move(move, board):
    board.move(move)

    return board

def get_all_moves(board, max_player):
    moves = []
    moveRate1 = []
    moveRate2 = []
    moveRate3 = []
    moveRate4 = []
    moveRate5 = []

    valid_moves = board.get_all_valid_moves()
    for move in valid_moves:
        temp_board = deepcopy(board)
        new_board = simulate_move(move, temp_board)

        if move.promotion:
            moveRate1.append(new_board)
        elif board.board.is_castling(move):
            moveRate2.append(new_board)
        elif board.board.gives_check(move):
            moveRate3.append(new_board)
        elif board.board.is_capture(move):
            moveRate4.append(new_board)
        else:
            moveRate5.append(new_board)
    moves = [*moveRate1, *moveRate2, *moveRate3, *moveRate4, *moveRate5]

    return moves

'''
#does not work also super slow

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


def minimax(position, depth, weight):

    if depth == 0 or position.winner() != None:
        return position

    bestPos = None
    bestEval = float("-inf")

    moves = get_all_moves(position)
    for move in moves:
        position.board.push_san("{}".format(move))
        evaluation = -1 * (minimax(position, depth-1, weight).evaluate(weight))
        bestEval = max(bestEval, evaluation)
        if bestEval == evaluation:
            bestPos = deepcopy(position)
        position.board.pop()

    return bestPos
'''
