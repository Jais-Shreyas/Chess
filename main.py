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
  # print(gs.board)
  running = True
  while running:
    for e in pg.event.get():
      if e.type == pg.QUIT:
        running = False
      elif e.type == pg.MOUSEBUTTONDOWN:
        x, y = pg.mouse.get_pos()
        x, y = x//SQ_SIZE, y//SQ_SIZE
        print(gs.board[y][x])
        # print(x, y)
    drawGameState(screen, gs)
    clock.tick(60)
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
