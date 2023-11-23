from .eval_constants import*

def evaluate(weight, board):
    # Gather all pieces regardless of color
    all_pieces = board.pieceListBlack + board.pieceListWhite

    # Initialize variables
    pieceSquareTable = 0
    pieceValue = 0
    resultMult = 1

    # Calculate piece square tables and piece values
    for piece in all_pieces:
        if piece.isupper():
            pieceSquareTable -= piece_square_table(board, piece)
            pieceValue -= piece_value(board, piece)
        else:
            pieceSquareTable += piece_square_table(board, piece)
            pieceValue += piece_value(board, piece)

    # Calculate pawn attack and piece protection
    pawnAttack = p_attack_black(board) - p_attack_white(board)
    pieceProtect = piece_protect(board)

    # Determine result
    result = 0
    winner = board.winner()
    if winner == "white wins":
        result = -9999999999999999999
    elif winner == "black wins":
        result = 9999999999999999999
    elif winner == "draw":
        resultMult = 0

    # Calculate the final evaluation score based on the weighted factors
    return (pieceValue * weight[0] + pieceSquareTable * weight[1] + pawnAttack * weight[2] + pieceProtect * weight[3] + result) * resultMult

def piece_square_table(board, piece_type):
    if (piece_type == "k" or piece_type == "K") and board.get_num_all_pieces() <= endgame:
        piece_type.join("1")
        
    pieces = board.get_numPieces(piece_type)
    value = sum(piece_evaluations[piece_type][x[0]][x[1]] for x in pieces)

    return value

def piece_value(board, piece_type):
    pieces = board.get_numPieces(piece_type)
    return len(pieces) * piece_values.get(piece_type, pawnValue)

def p_attack_black(board):
    pieces = board.get_numPieces("P")
    attacked_positions = set(tuple(piece) for piece in pieces)
    value = 0

    rook_pieces = board.get_numPieces("r")
    rook_positions = set(tuple(piece) for piece in rook_pieces)

    queen_pieces = board.get_numPieces("q")
    queen_positions = set(tuple(piece) for piece in queen_pieces)

    bishop_pieces = board.get_numPieces("b")
    bishop_positions = set(tuple(piece) for piece in bishop_pieces)

    knight_pieces = board.get_numPieces("n")
    knight_positions = set(tuple(piece) for piece in knight_pieces)

    for x,y in attacked_positions:
        left_attack = (x - 1, y + 1)
        right_attack = (x - 1, y - 1)

        if right_attack[1] == -1:
            right_attack = (right_attack[0], 1)

        if right_attack in rook_positions:
            value -= 250
        if right_attack in queen_positions:
            value -= 450
        if right_attack in bishop_positions:
            value -= 160
        if right_attack in knight_positions:
            value -= 150

        if left_attack[1] == 8:
            left_attack = (left_attack[0], left_attack[1] - 2)

        if left_attack in rook_positions:
            value -= 250
        if left_attack in queen_positions:
            value -= 450
        if left_attack in bishop_positions:
            value -= 160
        if left_attack in knight_positions:
            value -= 150

    return value if board.get_turn() else 0

def p_attack_white(board):
    pieces = board.get_numPieces("p")
    attacked_positions = set(tuple(piece) for piece in pieces)
    value = 0

    rook_pieces = board.get_numPieces("R")
    rook_positions = set(tuple(piece) for piece in rook_pieces)

    queen_pieces = board.get_numPieces("Q")
    queen_positions = set(tuple(piece) for piece in queen_pieces)

    bishop_pieces = board.get_numPieces("B")
    bishop_positions = set(tuple(piece) for piece in bishop_pieces)

    knight_pieces = board.get_numPieces("N")
    knight_positions = set(tuple(piece) for piece in knight_pieces)

    for x in attacked_positions:
        left_attack = (x[0] + 1, x[1] + 1)
        right_attack = (x[0] + 1, x[1] - 1)

        if right_attack[1] == -1:
            right_attack = (right_attack[0], 1)

        if right_attack in rook_positions:
            value -= 250
        if right_attack in queen_positions:
            value -= 450
        if right_attack in bishop_positions:
            value -= 160
        if right_attack in knight_positions:
            value -= 150

        if left_attack[1] == 8:
            left_attack = (left_attack[0], left_attack[1] - 2)

        if left_attack in rook_positions:
            value -= 250
        if left_attack in queen_positions:
            value -= 450
        if left_attack in bishop_positions:
            value -= 160
        if left_attack in knight_positions:
            value -= 150

    return value if board.get_turn() else 0

def piece_protect(board):
    moves = board.get_all_valid_moves()

    moveDestinations = set()

    piecesWhite = []
    piecesBlack = []

    whiteScore = 0
    blackScore = 0

    for x in board.pieceListWhite:
        piecesWhite.extend(board.get_numPieces(x))
    for x in board.pieceListBlack:
        piecesBlack.extend(board.get_numPieces(x))

    if moves:
        moveDestinations = set((8 - int(str(move)[3]), ord(str(move)[2]) - 97) for move in moves)

    for piece in piecesWhite:
        if tuple(piece) not in moveDestinations:
            whiteScore += 1

    for piece in piecesBlack:
        if tuple(piece) not in moveDestinations:
            blackScore += 1

    return -(blackScore - whiteScore) * 10