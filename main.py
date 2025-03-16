#For user input and handling gamestate

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION=8
SQ_SIZE=HEIGHT//DIMENSION
MAX_FPS=15 #for animations
IMAGES={}

#loading images once
def loadImages():
    pieces=['bR','bN','bB','bQ','bK','bP','wR','wN','wB','wQ','wK','wP']
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
    

#main code- user input and updating graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    # print(gs.board)
    loadImages()
    sqSelected = ()       # track of last click of user (tuple: (row,col))
    playerClicks = []     # track of player clicks (two tuples)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()         #coordinates of mouse click
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = ()          
                    playerClicks = []
                else:   
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move=ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    # print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks=[sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade=True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen,gs, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs, sqSelected):
    drawBoard(screen, sqSelected)               #draw the board
    drawPieces(screen,gs.board)     #draw the pieces on the board

def drawBoard(screen, sqSelected):
    colors=[p.Color(240,217,181,1),p.Color(181,136,99,1)]       #square colors
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c)%2)]
            if (r,c) == sqSelected:
                color = p.Color(130,151,105,1)
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))         #piece on board

if __name__ == "__main__":
    main()