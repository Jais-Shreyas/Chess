import pygame as pg
import ChessEngine
Images = {}
Width = Height = 512
Dimensions = 8
SQ_SIZE = Height // Dimensions
Max_FPS = 15

def loadImages():
  pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
  for piece in pieces:
    Images[piece] = pg.transform.scale(pg.image.load("./Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    
def main():
  pg.init()
  screen = pg.display.set_mode((Width, Height))
  pg.display.set_caption("Chess")
  clock = pg.time.Clock()
  screen.fill(pg.Color("white"))
  gs = ChessEngine.GameState()
  loadImages()
  validMoves = gs.getValidMoves()   # this is an expensive operation
  moveMade = False    # to check if a player makes a move
  running = True
  sqSelected = ()    # tracks the last clicked cell
  playerClicks = []  # keep tracks of player clicks (two tuples: [(r, c), (r, c)])
  
  while running:
    for e in pg.event.get():
      if e.type == pg.QUIT:
        running = False
      elif e.type == pg.MOUSEBUTTONDOWN:
        col, row = pg.mouse.get_pos()
        col, row = col//SQ_SIZE, row//SQ_SIZE
        if sqSelected == (row, col):  # deselect the square
          sqSelected = ()
          playerClicks = []
        else:
          sqSelected = (row, col)
          playerClicks.append(sqSelected)
        if len(playerClicks) == 2:    # make a move
          move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
          print(move.getChessNotation())
          if move in validMoves:    # in lecture 3, it was done.
            gs.makeMove(move)
            moveMade = True
          sqSelected = ()
          playerClicks = []
      elif e.type == pg.KEYDOWN:
        if e.key == pg.K_z:
          gs.Undo()
          moveMade = True
    if moveMade:
      validMoves = gs.getValidMoves()
      moveMade = False
    drawGameState(screen, gs)
    clock.tick(Max_FPS)
  pg.quit()
  
def drawGameState(screen, gs):
  drawBoard(screen)
  drawPieces(screen, gs.board)

def drawBoard(screen):
  colors = [pg.Color("white"), pg.Color("gray")]
  for r in range(Dimensions):
    for c in range(Dimensions):
      color = colors[((r+c) % 2)]
      pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
  pg.display.flip()
  
def drawPieces(screen, board):
  for r in range(Dimensions):
    for c in range(Dimensions):
      piece = board[r][c]
      if piece != "--":
        screen.blit(Images[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
  pg.display.flip()
  
if __name__ == "__main__":
  main()
