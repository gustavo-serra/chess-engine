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

global depth
global engine

# source: https://blog.devgenius.io/simple-interactive-chess-gui-in-python-c6d6569f7b6c

def play(events):

    global WHITE, GREY, YELLOW, BLUE, BLACK, board, background, index_moves, moves

    for event in events:
        
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
                #print(board)
                #print(move)
                board.push(move)
                index=None
                index_moves = []

            # show possible moves
            else:

                piece = board.piece_at(index)

                if piece == None:
                    pass

                else:

                    all_moves = list(board.legal_moves)
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

def update():
    '''
    updates the screen basis the board class
    '''

    global scrn, WHITE, pieces, board

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

def init():
    
    global scrn, status, WHITE, GREY, YELLOW, BLUE, BLACK, pieces, board, agent, agent_color, index_moves, background, depth
    
    # initialise display
    X = 800
    Y = 800
    scrn = pygame.display.set_mode((X, Y))
    pygame.init()

    status = True

    #basic colours
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    YELLOW = (204, 204, 0)
    BLUE = (50, 255, 255)
    BLACK = (0, 0, 0)

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
              'K': pygame.image.load('resources/w_king.png').convert_alpha()
              }

    background = pygame.image.load("resources/board.png").convert()
    
    #board background
    scrn.blit(background, ( 0,0 ))
    
    #name window
    pygame.display.set_caption('Chess')
    
    #initialise chess board and agent to play
    board = chess.Board()
    agent = engine.engine
    agent_color = 0
    depth = 5
    
    #used later
    index_moves = []

    update()

async def main():

    global scrn, status, WHITE, GREY, YELLOW, BLUE, BLACK, pieces, board, agent, agent_color, index_moves, background, depth
    
    init()
    
    while (status):
        #update screen

        if board.turn==agent_color:
            board.push(agent(board,depth))
            scrn.blit(background, ( 0,0 ))

        else:
            play(pygame.event.get())

        update()

        if board.outcome() != None:
            status = False

        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
