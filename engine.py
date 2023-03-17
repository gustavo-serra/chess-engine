# TCC Project
# Gustavo Figueiredo Serra NUSP 9794013

import chess
import chess.polyglot
import pygame
import math
import time

# chess.PAWN: chess.PieceType= 1
# chess.KNIGHT: chess.PieceType= 2
# chess.BISHOP: chess.PieceType= 3
# chess.ROOK: chess.PieceType= 4
# chess.QUEEN: chess.PieceType= 5
# chess.KING: chess.PieceType= 6


def material_eval(board):
    position_eval = 0
    
    piece_values = {
        "K": 20000,
        "Q": 950,
        "R": 563,
        "B": 333,
        "N": 305,
        "P": 100,
        "k": -20000,
        "q": -950,
        "r": -563,
        "b": -333,
        "n": -305,
        "p": -100
    }

    for piece in board.piece_map().values():
        position_eval += piece_values[piece.symbol()]
    
    return position_eval

def get_piece_square_value(board):
    """
    This function returns the positional value of each piece on the board.
    """
    piece_square_value_opening = {
        chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0,
                     20, 25, 35, 50, 50, 35, 25, 20,
                     6, 12, 25, 40, 40, 25, 12, 6,
                     0, 3, 17, 27, 27, 10, 3, 0,
                     -3, -5, 10, 20, 20, 0, 0, -10,
                     -10, -5, 5, 15, 15, 0, 10, -5,
                     -10, -5, 5, 10, 10, 10, 15, -5,
                     0, 0, 0, 0, 0, 0, 0, 0],   

        chess.KNIGHT: [-50, -40, -30, -30, -30, -30, -40, -50,
                        -40, -20, 0, 0, 0, 0, -20, -40,
                        -30, 0, 10, 15, 15, 20, 0, -30,
                        -30, 5, 15, 20, 20, 15, 5, -30,
                        -30, 0, 15, 20, 20, 15, 0, -30,
                        -30, 5, 10, 15, 15, 10, 5, -30,
                        -40, -20, 0, 5, 5, 0, -20, -40,
                        -50, -40, -30, -30, -30, -30, -40, -50],

        chess.BISHOP: [-20, -10, -10, -10, -10, -10, -10, -20,
                        -10, 0, 0, 0, 0, 0, 0, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -10, 5, 5, 10, 10, 5, 5, -10,
                        -10, 0, 10, 10, 10, 0, 0, -10,
                        -10, 10, 5, 5, 5, 5, 10, -10,
                        -10, 20, 5, 10, 10, 5, 20, -10,
                        -20, -10, -10, -10, -10, -10, -10, -20],

    chess.ROOK: [20, 20, 30, 40, 40, 30, 20, 20,
                 20, 30, 40, 50, 50, 40, 30, 20,
                 10, 20, 30, 40, 40, 30, 20, 10,
                 -5, 10, 20, 30, 30, 20, 10, -5,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 -15, 0, 0, 0, 0, 0, 0, -15,
                 -30, -20, 5, 20, 20, 10, -20, -30],

    chess.QUEEN: [-20, 0, 10, 15, 40, 40, 40, 40,
                    -10, 0, 0, 0, 0, 30, 30, 30,
                    -10, 0, 5, 5, 5, 30, 30, 30,
                    -5, 0, 5, 5, 5, 15, 0, -5,
                    0, 0, 5, 5, 5, 5, 0, -5,
                    -10, 5, 5, 5, 5, 5, 0, -10,
                    -10, 0, 15, 0, 10, 0, 0, -10,
                    -20, -10, -10, 10, -5, -10, -10, -20],

    chess.KING: [-30, -40, -40, -50, -50, -40, -40, -30,
                    -30, -40, -40, -50, -50, -40, -40, -30,
                    -30, -40, -40, -50, -50, -40, -40, -30,
                    -30, -40, -40, -50, -50, -40, -40, -30,
                    -20, -30, -30, -40, -40, -30, -30, -20,
                    -10, -20, -20, -20, -20, -20, -20, -10,
                    5, 10, -5, -50, -50, -20, 20, 20,
                    -10, 30, 10, -50, -10, -30, 30, 20]}
    
    piece_square_value_endgame = {
        chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0,
                     55, 35, 25, 15, 15, 25, 35, 55,
                     45, 29, 16, 5, 5, 16, 29, 45,
                     33, 17, 7, 0, 0, 7, 17, 33,
                     25, 10, 0, -5, -5, 0, 10, 25,
                     20, 5, -5, -10, -10, -5, 5, 20,
                     20, 5, -5, -10, -10, -5, 5, 20,
                     0, 0, 0, 0, 0, 0, 0, 0],

        chess.KNIGHT: [-50, -40, -30, -30, -30, -30, -40, -50,
                        -40, -20, 0, 0, 0, 0, -20, -40,
                        -30, 0, 10, 15, 15, 10, 0, -30,
                        -30, 5, 15, 20, 20, 15, 5, -30,
                        -30, 0, 15, 20, 20, 15, 0, -30,
                        -30, 5, 10, 15, 15, 10, 5, -30,
                        -40, -20, 0, 5, 5, 0, -20, -40,
                        -50, -40, -30, -30, -30, -30, -40, -50],

        chess.BISHOP: [-20, -10, -10, -10, -10, -10, -10, -20,
                        -10, 0, 0, 0, 0, 0, 0, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -10, 5, 10, 15, 15, 10, 5, -10,
                        -10, 0, 10, 15, 15, 10, 0, -10,
                        -10, 10, 5, 15, 15, 5, 10, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -20, -10, -10, -10, -10, -10, -10, -20],

    chess.ROOK: [15, 10, 10, 10, 10, 10, 10, 0,
                 15, 15, 15, 15, 10, 10, 10, 5,
                 10, 10, 10, 5, 5, 5, 5, 5,
                 5, 5, 10, 5, 0, 0, 5, 5,
                 5, 5, 5, 5, 0, 0, 0, 5,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 0, 0, 0, 5, 5, 0, 0, 0],

    chess.QUEEN: [-10, 20, 20, 30, 30, 20, 10, 20,
                  -20, 20, 30, 40, 50, 30, 30, 0,
                  -20, 0, 5, 40, 40, 40, 0, 10,
                  5, 20, 25, 40, 40, 40, 50, 30,
                  0, 30, 25, 50,30, 30, 40, 20,
                  -10, 5, 15, 5, 5, 15, 10, 0,
                  -10, 0, 5, 0, 0, 0, 0, -10,
                  -20, -10, -10, -5, -5, -10, -10, -20],

    chess.KING: [-50, -40, -20, -20, -10, 10, 5, -20,
                 -10, 20, 15, 15, 15, 40, 20, 10,
                 10, 15, 25, 15, 20, 40, 40, 10,
                 -5, 0, 25, 25, 25, 30, 25, 10,
                 -20, 0, 20, 25, 25, 25, 10, 5,
                 -10, 0, 10, 20, 25, 15, 5, -10,
                 -30, -10, 5, 15, 15, 5, -5, -20,
                 -50, -30, -20, -10, -30, -15, -25, -45]}

    phase_dict = {chess.PAWN : 0,
    chess.KNIGHT : 1,
    chess.BISHOP : 1,
    chess.ROOK : 2,
    chess.QUEEN : 4}
    TotalPhase = phase_dict[chess.PAWN]*16 + phase_dict[chess.KNIGHT]*4 + phase_dict[chess.BISHOP]*4 + phase_dict[chess.ROOK]*4 + phase_dict[chess.QUEEN]*2

    phase = TotalPhase
    opening = 0
    endgame = 0
    
    for piece_type in range(1,6):
        phase -= phase_dict[piece_type]*len(board.pieces(piece_type,chess.BLACK))
        for square in board.pieces(piece_type,chess.BLACK):
            opening -= piece_square_value_opening[piece_type][square]
            endgame -= piece_square_value_endgame[piece_type][square]
        phase -= phase_dict[piece_type]*len(board.pieces(piece_type,chess.WHITE))
        for square in board.pieces(piece_type,chess.WHITE):
            opening += piece_square_value_opening[piece_type][(7-square//8)*8 + square%8]
            endgame += piece_square_value_endgame[piece_type][(7-square//8)*8 + square%8]

    phase = (phase * 256 + (TotalPhase / 2)) / TotalPhase
    
    #print(phase, opening, endgame)
    
    piece_eval = ((opening * (256 - phase)) + (endgame * phase)) / 256
    
    return piece_eval

def pawn_eval(board):
                
    white_pawns = board.pieces(1,1)
    black_pawns = board.pieces(1,0)

    # mid-game only?
    #pawn_files_white = [p%8 for p in white_pawns]
    #pawn_files_black = [p%8 for p in black_pawns]
    #semi_open_files_white = set(sorted(pawn_files_black)) - set(sorted(pawn_files_white))
    #semi_open_files_black = set(sorted(pawn_files_white)) - set(sorted(pawn_files_black))
    #open_files = set([0,1,2,3,4,5,6,7]) - set(sorted(pawn_files_white)) - set(sorted(pawn_files_black))

    passed_pawns = []
    isolated_pawns = []
    backwards_pawns = []
    doubled_pawns = []
    for pawn in white_pawns:           
        file = pawn%8
        rank = pawn//8
        doubled = False
        passer = True
        isolated = True
        backwards = True
        semi_open = True
        for f in [file-1, file, file+1]:
            if f >=0 and f < 8:
                for r in range(1,7):
                    square = r*8 + f

                    # passed pawn
                    if (r > rank) and (square in black_pawns):
                        passer = False

                    # doubled, isolated and backwards pawn
                    if (square != pawn) and (square in white_pawns):
                        if f == file:
                            if r > rank:
                                doubled = True 
                                passer = False #doubled passed pawn doesn´t count
                        else:
                            isolated = False
                            if r <= rank:
                                backwards = False # include better backwards rule? + blocked pawns

                    #need to include protection, pawn chains

        if doubled: doubled_pawns += [pawn]
        if passer: passed_pawns += [pawn]
        if isolated: isolated_pawns += [pawn]
        if backwards: backwards_pawns += [pawn]

    pawn_eval = 50*len(passed_pawns) - 25*len(doubled_pawns) - 5*len(backwards_pawns) - 25*len(isolated_pawns)
    
    return pawn_eval #, doubled_pawns, passed_pawns, isolated_pawns, backwards_pawns, semi_open_files_white, semi_open_files_black, open_files 


def mobility_eval(board):
    
    if board.turn == chess.WHITE:
        temp_board = board.copy()
        temp_board.push(chess.Move.null())
        return 5*(board.legal_moves.count()-temp_board.legal_moves.count())
    
    if board.turn == chess.BLACK:
        temp_board = board.copy()
        temp_board.push(chess.Move.null())
        return -5*(board.legal_moves.count()-temp_board.legal_moves.count())


def evaluate(board):
        
    return material_eval(board) + piece_eval(board) + mobility_eval(board)# + pawn_eval(board)

def order_moves(board):

    piece_values = {
        "K": 20000,
        "Q": 950,
        "R": 563,
        "B": 333,
        "N": 305,
        "P": 100,
        "k": -20000,
        "q": -950,
        "r": -563,
        "b": -333,
        "n": -305,
        "p": -100
    }
    
    dict_move_scores = dict()
    
    for move in board.legal_moves:
        
        move_score = 0
        capturing_piece = board.piece_at(move.from_square)
        captured_piece = board.piece_at(move.from_square)
        last_moved_piece = board.piece_at(board.peek().to_square)

        if captured_piece != None:
            move_score += piece_values[captured_piece.symbol()] - piece_values[capturing_piece.symbol()]
            
        if board.gives_check(move):
            move_score += piece_values[capturing_piece.symbol()]
            
        if move.promotion != None:
            move_score += piece_values[chess.Piece(move.promotion,board.turn).symbol()]
            
        dict_move_scores[move] = move_score
    
    return dict(sorted(dict_move_scores.items(), key=lambda item: item[1])).keys()

def search_alphabeta_pruning(board, depth, ply_from_root=0, alpha=-math.inf, beta=math.inf):
    
    global best_move
    
    if board.turn == chess.WHITE:
        color_bool = 1
    
    if board.turn == chess.BLACK:
        color_bool = -1
    
    if depth == 0:
        return color_bool*evaluate(board)
    
    if board.is_checkmate():
        return (-1000000 + ply_from_root)
    
    if board.is_stalemate():
        return 0

    for move in order_moves(board):
        board.push(move)
        evaluation = -search_alphabeta_pruning(board, depth - 1, ply_from_root + 1, -beta, -alpha)
        board.pop()
        if evaluation >= beta:
            return beta
        if evaluation > alpha:
            #principal_variation = list(board.move_stack)[-ply_from_root:]
            if ply_from_root == 0:
                best_move = move
            
            alpha = evaluation
    
    return alpha


def engine(board, depth):
    
    global best_move
    
    with chess.polyglot.open_reader("/data/data/chess-engine/assets/openings/baron30.bin") as reader:

        try: 
            return reader.choice(board).move
        except:
            best_move = chess.Move.null()

            evaluation = search_alphabeta_pruning(board, depth)

            return best_move
