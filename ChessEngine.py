#Info about the current state and determining current valid moves with a move log

class GameState():
    def __init__(self):
        #board
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.moveFunctions = {'P':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLoc = (7, 4)
        self.blackKingLoc = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.inCheck = False
        self.pins = []
        self.checks = []
    
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        # update king location
        if (move.pieceMoved == "wK"):
            self.whiteKingLoc = (move.endRow,move.endCol)
        elif (move.pieceMoved == "bK"):
            self.blackKingLoc = (move.endRow,move.endCol)
    
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update king location
            if (move.pieceMoved == "wK"):
                self.whiteKingLoc=(move.startRow,move.startCol)
            elif (move.pieceMoved == "bK"):
                self.blackKingLoc=(move.startRow,move.startCol)
    
    #Moves with Checks
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLoc[0]
            kingCol = self.whiteKingLoc[1]
        else:
            kingRow = self.blackKingLoc[0]
            kingCol = self.blackKingLoc[1]
        if (self.inCheck):
            if (len(self.checks) == 1):
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol][1]
                validSquares = []
                # if its a knight, knig must move or capture the opponent's knight
                if (pieceChecking == 'N'):
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        # check[2] and check[3] are the direction of the check
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if (0 <= validSquare[0] < 8 and 0 <= validSquare[1] < 8):
                            if (validSquare[0] == checkRow and validSquare[1] == checkCol):
                                break
                # get rid of any moves that do not block the check or move the king
                # might need fix later    <----------------------------
                newMoves = []
                for move in moves:
                    if (move.pieceMoved[1] == 'K' or (move.endRow, move.endCol) in validSquares):
                        newMoves.append(move)
                moves = newMoves
            # if there are two or more checks, the king must move
            else:
                self.getKingMoves(kingRow, kingCol, moves) 
        # not in check, so all moves are fine
        else:
            moves = self.getAllPossibleMoves()
        
        return moves
                
                    
        # # generate all possible moves
        # moves = self.getAllPossibleMoves()
        # # for each move, make the move and check if the king is in check
        # # if not then its a valid move
        # validmoves = []
        # for move in moves:
        #     # suppose its white turn
        #     # make the move
        #     self.makeMove(move)  # now its black turn 
        #     self.whiteToMove = not self.whiteToMove  # switch to white turn back to check for checks
        #     # check if the move puts the king in check
        #     # generate all moves for the opponent
        #     # for each of your moves, see if any of the opponent moves attack your king
        #     # if not then its a valid move
        #     if not self.isCheck():
        #         validmoves.append(move)
        #     self.whiteToMove = not self.whiteToMove  # switch back to black turn
        #     # undo the move
        #     self.undoMove()
        # if len(validmoves) == 0:
        #     if self.isCheck():
        #         self.checkMate = True
        #     else:   
        #         self.staleMate = True
        # else:
        #     # need to update these for undo moves
        #     self.checkMate = False
        #     self.staleMate = False
        # return validmoves
    
    # Determine if the current player is in check
    # def isCheck(self):
    #     if self.whiteToMove:
    #         return self.squareUnderAttack(self.whiteKingLoc[0], self.whiteKingLoc[1])
    #     else:
    #         return self.squareUnderAttack(self.blackKingLoc[0], self.blackKingLoc[1])

    # # Determine if the enemy can attack the square r,c
    # def squareUnderAttack(self,r,c):
    #     self.whiteToMove = not self.whiteToMove  # switch to opponent's turn
    #     # check all possible moves of the opponent
    #     oppMoves = self.getAllPossibleMoves()
    #     self.whiteToMove = not self.whiteToMove  # switch back to current player's turn
    #     for move in oppMoves:
    #         if move.endRow == r and move.endCol == c:
    #             return True
    #     return False
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if(turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
    
    def getPawnMoves(self,r,c,moves):
        print(self.pins)
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
            
        if (self.whiteToMove):                                                # white pawn
            if (self.board[r-1][c] == "--"):
                if not piecePinned or pinDirection == (-1, 0):                       # move forward
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if (r == 6 and self.board[r-2][c] == "--"):                       # 2sq pawn moves
                        moves.append(Move((r,c),(r-2,c),self.board))
            if (c - 1 >= 0):                                                      #capturing with pawn
                if (self.board[r-1][c-1][0]  == 'b'):                            #left capture
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r,c),(r-1,c-1),self.board))            
            if (c + 1 < 8):                                                      #right capture
                if (self.board[r-1][c+1][0]  == 'b'):
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r,c),(r-1,c+1),self.board))
        else:                                                               # black pawn
            if self.board[r+1][c]  ==  "--":
                if not piecePinned or pinDirection == (1, 0):                       # move forward
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r == 1 and self.board[r+2][c] == "--":                       # 2sq pawn moves
                        moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0:                                                      #capturing with pawn
                if self.board[r+1][c-1][0]  == 'w':                           #left capture
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<8:                                                       #right capture
                if self.board[r+1][c+1][0]  == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r,c),(r+1,c+1),self.board))
            
    def getRookMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if (self.board[r][c][1] != "Q"):   # can't remove queen from pin on rook move, only remove on bishop move
                    self.pins.remove(self.pins[i])
                break
        directions=((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow< 8 and 0 <= endCol<8:  # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece=self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:                               # enemy piece
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:                                                       # ally piece
                            break
                else:  # off board                                                           # outside board
                    break

    def getKnightMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
            
        
        knightMoves=  ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if (0 <= endRow <= 7 and 0 <= endCol <= 7):                                   # in limit of board
                if not piecePinned:
                    endPiece=self.board[endRow][endCol]
                    if (endPiece[0] != allyColor):                                      # no ally on landing sq
                        moves.append(Move((r,c),(endRow,endCol),self.board))

    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if (self.board[r][c][1] != "Q"):   # can't remove queen from pin on rook move, only remove on bishop move
                    self.pins.remove(self.pins[i])
                break
        directions=((-1, -1), (-1, 1), (1, -1), (1, 1)) # up left, up right, down left, down right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if (0 <= endRow <= 7 and 0 <= endCol <= 7):
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece=self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:                               # enemy piece
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:                                                       # ally piece
                            break
                else:                                                           # outside board
                    break
    
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    
    def getKingMoves(self,r,c,moves):
        kingMoves = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r+kingMoves[i][0]
            endCol = c+kingMoves[i][1]
            if (0 <= endRow <= 7 and 0 <= endCol <= 7):                                   # in limit of board
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!=allyColor:                                      # no ally on landing sq
                    # place king on end square and check if it is in check
                    if (allyColor == "w"):
                        self.whiteKingLoc = (endRow, endCol)
                    else:
                        self.blackKingLoc = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:  # not in check
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    # reset king location
                    if (allyColor == "w"):
                        self.whiteKingLoc = (r, c)
                    else:
                        self.blackKingLoc = (r, c)

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if (self.whiteToMove):
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLoc[0]
            startCol = self.whiteKingLoc[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLoc[0]
            startCol = self.blackKingLoc[1]
        # check outwards for pins and checks
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        # first 4 are orthogonal, last 4 are diagonal
        for j in range(len(directions)):
            dir = directions[j]
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow + dir[0] * i
                endCol = startCol + dir[1] * i
                if ((0 <= endRow < 8) and (0 <= endCol < 8)):
                    endPiece = self.board[endRow][endCol]
                    if ((endPiece[0] == allyColor) and (endPiece[1] != "K")):
                        if possiblePin == (): # first ally piece can be a pin
                            possiblePin = (endRow, endCol, dir[0], dir[1])
                        else:  # second ally piece cannot be a pin
                            break
                    elif (endPiece[0] == enemyColor):
                        type = endPiece[1]
                        # 5 possibilities for pins
                        # 1. rook pinning orthogonal
                        # 2. bishop pinning diagonal
                        # 3. 1 square diagonal king pinning and its a pawn
                        # 4. any direction queen pinning
                        # 5. any direction 1 square away and piece is a king to make sure the king doesn't move to another king
                        if ((0 <= j <= 3 and type == "R") or \
                            (4 <= j <= 7 and type == "B") or \
                            (i == 1 and type == "P" and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5)) or \
                            (type == 'Q') or (i == 1 and type == "K"))):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, dir[0], dir[1]))
                                break 
                            else: # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # empty square   
                            break 
                else:  # outside board                   
                    break
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (2, -1), (1, 2), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if (0 <= endRow < 8 and 0 <= endCol < 8):
                endPiece = self.board[endRow][endCol]
                if (endPiece[0] == enemyColor and endPiece[1] == "N"):
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
        
#All possible moves
class Move():
    ranksToRows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}
    filestoCols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filestoCols.items()}
    def __init__(self,startSq,endSq,board):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000+ self.startCol*100+self.endRow*10+self.endCol              #unique move ids
        # print(self.moveID)
    
    #Overriding equals method since we used Move class(classes equality)
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]