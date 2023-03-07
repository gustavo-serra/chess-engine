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
        "Q": 900,
        "R": 500,
        "B": 300,
        "N": 300,
        "P": 100,
        "k": -20000,
        "q": -900,
        "r": -500,
        "b": -300,
        "n": -300,
        "p": -100
    }

    for piece in board.piece_map().values():
        position_eval += piece_values[piece.symbol()]
    
    return position_eval

#def pawn_eval_files(board):
#                
#        white_pawns = board.pieces(1,1)
#        black_pawns = board.pieces(1,0)
#        
#        pawn_files_white = [p%8 for p in white_pawns]
#        pawn_files_black = [p%8 for p in black_pawns]
#        
#        # white doubled pawns
#        pawn_eval += -0.5*(len(pawn_files_white)-len(set(pawn_files_white)))
#
#        # black doubled pawns
#        pawn_eval += 0.5*(len(pawn_files_white)-len(set(pawn_files_white)))
#
#        # white isolated pawns
#        files_set = set(sorted(pawn_files_white))
#        spaces = sorted(set([-1,0,1,2,3,4,5,6,7,8]) - files_set)
#        diffs = [t - s for s, t in zip(spaces, spaces[1:])]
#        pawn_eval += sum([-0.25 for d in diffs if d == 2])
#
#        # black isolated pawns
#        files_set = set(sorted(pawn_files_black))
#        spaces = sorted(set([-1,0,1,2,3,4,5,6,7,8]) - files_set)
#        diffs = [t - s for s, t in zip(spaces, spaces[1:])]
#        pawn_eval += sum([0.25 for d in diffs if d == 2])
#
#        # passed pawns
#        passed_pawns = 0
#        isolated_pawns = 0
#        backwards_pawns = 0
#        doubled_pawns = 0
#        semiopen_files = []
#        for pawn in white_pawns:           
#            file = pawn%8
#            rank = pawn//8
#            doubled = False
#            passer = True
#            isolated = True
#            backwards = True
#            semi_open = True
#            for f in [file-1, file, file+1]:
#                if f >=0 && f < 8:
#                    for r in range(1,7):
#                        
#                        # doubled, isolated and backwards pawns
#                        if r*8 + f in white_pawns:
#                            if f = file:
#                                doubled = True
#                            else:
#                                isolated = False
#                                if r <= rank:
#                                    backwards = False # include better backwards rule? + blocked pawns
#                            
#                        # passed pawns
#                        if (r > rank) && (r*8 + f in black_pawns):
#                            passer = False
#                        
#                        # semi open file
#                        if (f = file) && (r*8 + f in black_pawns):
#                            semi_open = False
#                            
#            if semi_open: semi_open_files += [file]
#            passed_pawns += passer
#            isolated_pawns += isolated
#
#        # backwards pawn ?
#    
#    return position_eval


#def king_safety_eval(board):

#def center_control_eval(board):

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
    
    return pawn_eval, doubled_pawns, passed_pawns, isolated_pawns, backwards_pawns#, semi_open_files_white, semi_open_files_black, open_files 


def mobility_eval(board):
    
    if board.turn == chess.WHITE:
        temp_board = board.copy()
        temp_board.push(chess.Move.null())
        return 10*(board.legal_moves.count()-temp_board.legal_moves.count())
    
    if board.turn == chess.BLACK:
        temp_board = board.copy()
        temp_board.push(chess.Move.null())
        return -10*(board.legal_moves.count()-temp_board.legal_moves.count())


def evaluate(board):
        
    #semi_open_files_white, semi_open_files_black, open_files
        
    return material_eval(board) + pawn_eval(board)[0] + mobility_eval(board)


#def search(board, depth):
#    
#    if depth == 0:
#        return evaluate(board)
#    
#    if board.is_checkmate():
#        return math.inf
#    
#    if board.is_stalemate():
#        return 0
#    
#    legal_moves = list(board.legal_moves)
#    
#    best_eval = -math.inf
#    
#    for move in legal_moves:
#        board.push(move)
#        evaluation = -search(board, depth - 1)
#        best_eval = max(best_eval, evaluation)
#        board.pop()

def order_moves(board):

    piece_values = {
        "K": 20000,
        "Q": 900,
        "R": 500,
        "B": 300,
        "N": 300,
        "P": 100,
        "k": -20000,
        "q": -900,
        "r": -500,
        "b": -300,
        "n": -300,
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

    #for move in board.legal_moves:
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
                #print(ply_from_root, move, evaluation,principal_variation)
            
            alpha = evaluation
    
    return alpha


def engine(board, depth):
    
    global best_move
    
    with chess.polyglot.open_reader("/data/data/chess-engine/assets/openings/Human.bin") as reader:
        
#        print(board)
#        
#        print(reader)
#        
#        print(reader.get(board))
#        
#        for move in reader.find_all(chess.Board()):
#            print(move)
#
#        print(reader.choice(board).move)

        try: 
            return reader.choice(board).move
        except:
            best_move = chess.Move.null()

            evaluation = search_alphabeta_pruning(board, depth)

            print(best_move)

            return best_move
