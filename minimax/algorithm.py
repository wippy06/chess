from copy import deepcopy
from chessFolder.constants import PLAYER, AI

def minimax(position, depth, max_player, alpha, beta, weight):
    #position is an object
    #depth is an int to show how far to go
    #max_player checks if ai wants to maximise sore or minimise score

    if depth == 0 or position.winner() != None:
        return position.evaluate(weight), position
    
    if max_player:
        maxEval = float("-inf")
        best_move = None
        for move in get_all_moves(position):
            evaluation = minimax(move, depth-1, False, alpha, beta, weight)[0]
            maxEval = max(maxEval,evaluation)

            if maxEval == evaluation:
                best_move = move

            alpha = max( alpha, maxEval)
            if beta <= alpha:
                break

        return maxEval, best_move
    
    else:
        minEval = float("inf")
        best_move = None
        for move in get_all_moves(position):
            evaluation = minimax(move, depth-1, True, alpha, beta, weight)[0]
            minEval = min(minEval,evaluation)

            if minEval == evaluation:
                best_move = move
            
            beta = min( beta, minEval)
            if beta <= alpha:
                break

        return minEval, best_move

def simulate_move(move, board):
    board.move(move)

    return board

def get_all_moves(board):
    moves = []

    valid_moves = board.get_all_valid_moves()
    for move in valid_moves:
        temp_board = deepcopy(board)
        new_board = simulate_move(move, temp_board)
        moves.append(new_board)

    return moves


