# TCC Project
# Gustavo Figueiredo Serra NUSP 9794013

import chess
import pygame
import math
import time
import engine

# chess.PAWN: chess.PieceType= 1
# chess.KNIGHT: chess.PieceType= 2
# chess.BISHOP: chess.PieceType= 3
# chess.ROOK: chess.PieceType= 4
# chess.QUEEN: chess.PieceType= 5
# chess.KING: chess.PieceType= 6


def chess_GUI(mode, agent = engine.engine, depth = 4, agent_color = 0):
    
    # source: https://blog.devgenius.io/simple-interactive-chess-gui-in-python-c6d6569f7b6c
    
    #initialise display
    X = 800
    Y = 800
    scrn = pygame.display.set_mode((X, Y))
    pygame.init()

    #basic colours
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    YELLOW = (204, 204, 0)
    BLUE = (50, 255, 255)
    BLACK = (0, 0, 0)

    #initialise chess board
    BOARD = chess.Board()

    #load piece images
    pieces = {'p': pygame.image.load('resources/b_pawn.png').convert_alpha(),
              'n': pygame.image.load('resources/b_knight.png').convert_alpha(),
              'b': pygame.image.load('resources/b_bishop.png').convert_alpha(),
              'r': pygame.image.load('resources/b_rook.png').convert_alpha(),
              'q': pygame.image.load('resources/b_queen.png').convert_alpha(),
              'k': pygame.image.load('resources/b_king.png').convert_alpha(),
              'P': pygame.image.load('resources/w_pawn.png').convert_alpha(),
              'N': pygame.image.load('resources/w_knight.png').convert_alpha(),
              'B': pygame.image.load('resources/w_bishop.png').convert_alpha(),
              'R': pygame.image.load('resources/w_rook.png').convert_alpha(),
              'Q': pygame.image.load('resources/w_queen.png').convert_alpha(),
              'K': pygame.image.load('resources/w_king.png').convert_alpha(),

              }

    background = pygame.image.load("resources/board.png").convert()

    def update(scrn,board):
        '''
        updates the screen basis the board class
        '''

        for i in range(64):
            piece = board.piece_at(i)
            if piece == None:
                pass
            else:
                scrn.blit(pieces[str(piece)],((i%8)*90,630-(i//8)*90))

        for i in range(7):
            i=i+1
            pygame.draw.line(scrn,WHITE,(0,i*90),(720,i*90))
            pygame.draw.line(scrn,WHITE,(i*90,0),(i*90,720))

        pygame.display.flip()
    
    #board background
    scrn.blit(background, ( 0,0 ))
    #name window
    pygame.display.set_caption('Chess')
    
    if mode == "player vs player":

        index_moves = []

        status = True
        while (status):
            #update screen
            update(scrn,BOARD)

            for event in pygame.event.get():

                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    status = False

                # if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #remove previous highlights
                    scrn.blit(background, ( 0,0 ))
                    #get position of mouse
                    pos = pygame.mouse.get_pos()

                    #find which square was clicked and index of it
                    square = (math.floor(pos[0]/90),math.floor(pos[1]/90))
                    index = (7-square[1])*8+(square[0])

                    # if we are moving a piece
                    if index in index_moves: 

                        move = moves[index_moves.index(index)]

                        BOARD.push(move)

                        #reset index and moves
                        index=None
                        index_moves = []


                    # show possible moves
                    else:
                        #check the square that is clicked
                        piece = BOARD.piece_at(index)
                        #if empty pass
                        if piece == None:

                            pass
                        else:

                            #figure out what moves this piece can make
                            all_moves = list(BOARD.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:

                                    moves.append(m)

                                    t = m.to_square

                                    TX1 = 90*(t%8)
                                    TY1 = 90*(7-t//8)


                                    #highlight squares it can move to
                                    pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,90,90),5)

                            index_moves = [a.to_square for a in moves]

        # deactivates the pygame library
            if BOARD.outcome() != None:
                print(BOARD.outcome())
                status = False
                print(BOARD)
        pygame.quit()

    if mode == "player vs engine":

        index_moves = []

        status = True
        while (status):
            #update screen
            update(scrn,BOARD)


            if BOARD.turn==agent_color:
                BOARD.push(agent(BOARD,depth))
                scrn.blit(background, ( 0,0 ))

            else:

                for event in pygame.event.get():

                    # if event object type is QUIT
                    # then quitting the pygame
                    # and program both.
                    if event.type == pygame.QUIT:
                        status = False

                    # if mouse clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #reset previous screen from clicks
                        scrn.blit(background, ( 0,0 ))
                        #get position of mouse
                        pos = pygame.mouse.get_pos()

                        #find which square was clicked and index of it
                        square = (math.floor(pos[0]/90),math.floor(pos[1]/90))
                        index = (7-square[1])*8+(square[0])

                        # if we have already highlighted moves and are making a move
                        if index in index_moves: 

                            move = moves[index_moves.index(index)]
                            #print(BOARD)
                            #print(move)
                            BOARD.push(move)
                            index=None
                            index_moves = []

                        # show possible moves
                        else:

                            piece = BOARD.piece_at(index)

                            if piece == None:

                                pass
                            else:

                                all_moves = list(BOARD.legal_moves)
                                moves = []
                                for m in all_moves:
                                    if m.from_square == index:

                                        moves.append(m)

                                        t = m.to_square

                                        TX1 = 90*(t%8)
                                        TY1 = 90*(7-t//8)


                                        pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,90,90),5)
                                #print(moves)
                                index_moves = [a.to_square for a in moves]

        # deactivates the pygame library
            if BOARD.outcome() != None:
                print(BOARD.outcome())
                status = False
                print(BOARD)
        pygame.quit()

    if mode == "engine vs engine":
              
        agent1 = agent2 = agent

        #make background black
        scrn.fill(BLACK)
        #name window
        pygame.display.set_caption('Chess')

        #variable to be used later

        status = True
        while (status):
            #update screen
            update(scrn,BOARD)

            if BOARD.turn==agent_color:
                BOARD.push(agent1(BOARD,depth))

            else:
                BOARD.push(agent2(BOARD,depth))

            scrn.fill(BLACK)

            for event in pygame.event.get():

                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    status = False

        # deactivates the pygame library
            if BOARD.outcome() != None:
                print(BOARD.outcome())
                status = False
                print(BOARD)

        time.sleep(5)

        pygame.quit()
        
# mode_num = int(input("What is the game mode?\n1- player vs. engine\n2- engine vs. engine\n3- player vs. player\n"))

# if mode_num == 1:
#     mode = "player vs engine"
#     color = int(input("Will you play with black or white? (0 = white, 1 = black)  "))
#     depth = int(input("What is the engine's search depth? (recommended: 4)  "))
#     chess_GUI(mode, engine.engine, depth, color)
    
# if mode_num == 2:
#     mode = "engine vs engine"
#     depth = int(input("What is the engine's search depth? (recommended: 4)  "))
#     chess_GUI(mode, engine.engine, depth)
    
# if mode_num == 3:
#     mode = "player vs player"
#     chess_GUI(mode)
    
