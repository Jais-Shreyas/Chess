class GameState():
  def __init__(self):
    self.board = [
      ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['--', '--', '--', '--', '--', '--', '--', '--'],
      ['--', '--', '--', '--', '--', '--', '--', '--'],
      ['--', '--', '--', '--', '--', '--', '--', '--'],
      ['--', '--', '--', '--', '--', '--', '--', '--'],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
    ]
    self.whiteMove = True
    self.moveLog = []
  
  def makeMove(self, move):
    self.board[move.startRow][move.startCol] = '--'   # vacant that square
    self.board[move.endRow][move.endCol] = move.pieceMoved    # move the piece to the new square
    self.moveLog.append(move)   # add move to the log
    self.whiteMove = not self.whiteMove  # swap turns
  
  def Undo(self):
    if (len(self.moveLog) != 0):
      move = self.moveLog.pop()
      self.board[move.startRow][move.startCol] = move.pieceMoved
      self.board[move.endRow][move.endCol] = move.pieceCaptured
      self.whiteMove = not self.whiteMove  #swap turns back

  def getValidMoves(self):
    return self.getAllPossibleMoves()
  
  def getAllPossibleMoves(self):
    moves = [Move((6, 4), (4, 4), self.board)]   # temporarily assigned a value
    for r in range(len(self.board)):
      for c in range(len(self.board[r])):
        clr = self.board[r][c][0]      # clr = colour of piece
        piece = self.board[r][c][1]    # piece = type of piece  
        if (clr == 'w' and self.whiteMove) or (clr == 'b' and not self.whiteMove):
          if piece == 'P':
            self.getPawnMoves(r, c, moves)
          elif piece == 'R':
            self.getRookMoves(r, c, moves)
          elif piece == 'N':
            self.getKnightMoves(r, c, moves)
          elif piece == 'B':
            self.getBishopMoves(r, c, moves)
          elif piece == 'Q':
            self.getQueenMoves(r, c, moves)
          elif piece == 'K':
            self.getKingMoves(r, c, moves)
    return moves
            
  def getPawnMoves(self, r, c, moves):
    pass
  
  def getRookMoves(self, r, c, moves):
    pass
  
  def getKnightMoves(self, r, c, moves):
    pass
  
  def getBishopMoves(self, r, c, moves):
    pass
  
  def getQueenMoves(self, r, c, moves):
    pass
  
  def getKingMoves(self, r, c, moves):
    pass
  
class Move():
  '''
        0  1  2  3  4  5  6  7
        _______________________
  0   8|__|__|__|__|__|__|__|__|
  1   7|__|__|__|__|__|__|__|__|
  2   6|__|__|__|__|__|__|__|__|
  3   5|__|__|__|__|__|__|__|__|
  4   4|__|__|__|__|__|__|__|__|
  5   3|__|__|__|__|__|__|__|__|
  6   2|__|__|__|__|__|__|__|__|
  7   1|__|__|__|__|__|__|__|__|
        a  b  c  d  e  f  g  h 
  '''
  ranksToRows = { '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0 }
  rowsToRanks = { 7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 2: '6', 1: '7', 0: '8' }
  filesToCols = { 'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7 }
  colsToFiles = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h' }
  
  def __init__(self, startSq, endSq, board):
    self.startRow = startSq[0]
    self.startCol = startSq[1]
    self.endRow = endSq[0]
    self.endCol = endSq[1]
    self.pieceMoved = board[self.startRow][self.startCol]
    self.pieceCaptured = board[self.endRow][self.endCol]
    self.moveID = 1000 * self.startRow + 100 * self.startCol + 10 * self.endRow + self.endCol
    
  def __eq__(self, other):
    if isinstance(other, Move):
      return self.moveID == other.moveID
    return False
  
  def getChessNotation(self):
    return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
  
  def getRankFile(self, r, c):
    return self.colsToFiles[c] + self.rowsToRanks[r]
    
    