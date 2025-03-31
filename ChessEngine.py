#Info about the current state and determining current valid moves with a move log

class GameState():
    def __init__(self):
        #board is a 8x8 2d list, each element of the list has 2 characters
        #The first character represents the color of the piece, 'b' or 'w'
        #The second character represents the type of the piece,
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
        self.enpassantPossible = () #corridnates of enpassant cell
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True) # white king side, black king side, white queen side, black queen side
        # castle log to keep track of castling rights and tracks and undo them easily
        # self.castleRightsLog = [self.currentCastlingRights]  # this does not make a copy of the object, it just makes a reference to the object. So when we change the object, it will change in the list as well. So we need to make a copy of the object and append it to the list.
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wKS, self.currentCastlingRights.bKS,
                                             self.currentCastlingRights.wQS, self.currentCastlingRights.bQS)]  # this does not make a copy of the object, it just makes a reference to the object. So when we change the object, it will change in the list as well. So we need to make a copy of the object and append it to the list.
    
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

        # update castle rights when a rook gets captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False
        # handle pawn promotion currently by input from user
        # need to change this to a better way later
        if (move.isPawnPromotion):
            promotedPiece = input("Promote to Queen(Q), Rook(R), Bishop(B), Knight(N): ").upper()
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        # enpassant move
        if (move.isEnpassantMove):
            self.board[move.startRow][move.endCol] = "--"   # remove the pawn that was captured enpassant
        #update enpassant
        if (move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2):   # pawn moved two tiles
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()
        
        # castle move, note that king is already moved to the end square because of above code
        if (move.isCastleMove):
            if (move.endCol == 6): # king side castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # move rook to king side
                self.board[move.endRow][move.endCol + 1] = "--"  # remove rook from old position
            else:                  # queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][0]  # move rook from leftmost square
                self.board[move.endRow][0] = "--"  # remove rook from old position

        self.enpassantPossibleLog.append(self.enpassantPossible)
        # update castle rights
        self.updateCastleRights(move)
        
        
        
    
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
            # undo enpassant
            if (move.isEnpassantMove):
                self.board[move.endRow][move.endCol] = "--"  #landing square remains blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured  # restore the pawn that was captured enpassant
               
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
            # restore castling rights
            self.castleRightsLog.pop()  # remove the last castling rights
            previousCastleRights = self.castleRightsLog[-1]  # get the previous castling rights
            self.currentCastlingRights = previousCastleRights  # restore the castling rights
            
            # undo castle move
            if (move.isCastleMove):  # note that king is already moved to the end square because of above code
                if (move.endCol == 6):  # king side castle
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]  # move rook to old position
                    self.board[move.endRow][move.endCol - 1] = "--"  # remove rook from new position
                else:                   # queen side castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]  # move rook to old position
                    self.board[move.endRow][move.endCol + 1] = "--"  # remove rook from new position
            self.checkMate = False
            self.staleMate = False
            
    
    def updateCastleRights(self,move):
        if (move.pieceMoved == "wK"):
            self.currentCastlingRights.wKS = False
            self.currentCastlingRights.wQS = False
        elif (move.pieceMoved == "bK"):
            self.currentCastlingRights.bKS = False
            self.currentCastlingRights.bQS = False
        elif (move.pieceMoved == "wR"):
            if (move.startRow == 7 and move.startCol == 0):  # queen side rook
                self.currentCastlingRights.wQS = False
            elif (move.startRow == 7 and move.startCol == 7):  # king side rook
                self.currentCastlingRights.wKS = False
        elif (move.pieceMoved == "bR"):
            if (move.startRow == 0 and move.startCol == 0):  # queen side rook
                self.currentCastlingRights.bQS = False
            elif (move.startRow == 0 and move.startCol == 7):  # king side rook
                self.currentCastlingRights.bKS = False
        # update the castle rights log
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wKS, self.currentCastlingRights.wQS,
                                                 self.currentCastlingRights.bKS, self.currentCastlingRights.bQS))
    
    #Moves with Checks
    def getValidMoves(self):
        # store current castling rights
        currCastleRights = CastleRights(self.currentCastlingRights.wKS, self.currentCastlingRights.bKS,
                                        self.currentCastlingRights.wQS, self.currentCastlingRights.bQS)
        
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
            # check for king castle moves, we don't need colors here as they already point to appropriate king location
            self.getCastleMoves(kingRow, kingCol, moves)
        
        if (len(moves) == 0):   # either checkmate or stalemate
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
            
        self.currentCastlingRights = currCastleRights  # restore the castling rights
        return moves
                
                    
        # generate all possible moves
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
    def isCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLoc[0], self.whiteKingLoc[1])
        else:
            return self.squareUnderAttack(self.blackKingLoc[0], self.blackKingLoc[1])

    # Determine if the enemy can attack the square r,c
    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove  # switch to opponent's turn
        # check all possible moves of the opponent
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch back to current player's turn
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if(turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)  # call appropriate functions
        return moves
    
    def getPawnMoves(self,r,c,moves):
        # print(self.pins)
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
            
        if (self.whiteToMove):                                                # white pawn
            moveAmount = -1
            startRow = 6
            enemyColor = 'b'
            kingRow,kingCol = self.whiteKingLoc
        else:
            moveAmount = 1
            startRow = 1
            enemyColor = 'w'
            kingRow,kingCol = self.blackKingLoc
        
        if self.board[r + moveAmount][c] == '--':#1 square move
            if not piecePinned or pinDirection == (moveAmount,0):
                moves.append(Move((r,c),(r + moveAmount,c),self.board))
                if r == startRow and self.board[r + 2*moveAmount][c] == '--': #2 square moves
                  moves.append(Move((r,c),(r + 2 * moveAmount,c),self.board))
        if c - 1 >= 0: # capture to the left
            if not piecePinned or pinDirection == (moveAmount,-1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    moves.append(Move((r,c),(r + moveAmount,c - 1),self.board))
                if (r + moveAmount,c - 1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r: 
                        if kingCol < c: #king is to the left of the pawn
                            #inside thhe king and pawn,outside means 
                            insideRange = range(kingCol + 1,c - 1)
                            outsideRange = range(c + 1,8)
                        else:
                            insideRange = range(kingCol - 1,c,-1)
                            outsideRange = range(c - 2,-1,-1)
                        for i in insideRange:
                            if self.board[r][i] != '--': #some other pieces beside en-passant pawn blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != '--':
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                      moves.append(Move((r,c),(r + moveAmount,c - 1),self.board,isEnpassantMove = True))
        if c + 1 <= 7: #capture to the right
            if not piecePinned or pinDirection == (moveAmount,1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    moves.append(Move((r,c),(r + moveAmount,c + 1),self.board))
                if (r + moveAmount,c + 1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r: 
                        if kingCol < c: #king is to the left of the pawn
                            #inside thhe king and pawn,outside means 
                            insideRange = range(kingCol + 1,c)
                            outsideRange = range(c + 2,8)
                        else:
                            insideRange = range(kingCol - 1,c + 1,-1)
                            outsideRange = range(c - 1,-1,-1)
                        for i in insideRange:
                            if self.board[r][i] != '--': #some other pieces beside en-passant pawn blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != '--':
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c),(r + moveAmount,c + 1),self.board,isEnpassantMove = True))
                
                
            
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
        # knight moves
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
                if endPiece[0] != allyColor:                                      # no ally on landing sq
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
        # getting castle moves here causes infinite recursion and we check this in getValidMoves
        # self.getCastleMoves(r, c, moves)
                        
    def getCastleMoves(self, r, c, moves):
        # print("checking castle moves")
        if (self.inCheck):
            return
        if ((self.whiteToMove and self.currentCastlingRights.wKS) or (not self.whiteToMove and self.currentCastlingRights.bKS)):
            self.getKingSideCastleMoves(r, c, moves)
        if ((self.whiteToMove and self.currentCastlingRights.wQS) or (not self.whiteToMove and self.currentCastlingRights.bQS)):
            self.getQueenSideCastleMoves(r, c, moves)
        
    def getKingSideCastleMoves(self, r, c, moves):
        if (self.board[r][c+1] == '--' and self.board[r][c+2] == '--'):
            # if (self.whiteToMove):    <---- maybe fix this later
                if (not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2)):
                    moves.append(Move((r,c),(r,c+2),self.board, isCastleMove = True))
            # else:
            #     if (not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2)):
            #         moves.append(Move((r,c),(r,c+2),self.board, isCastleMove = True))
        
    def getQueenSideCastleMoves(self, r, c, moves):   
        if (self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--'):
            # if (self.whiteToMove):
                if (not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2)):  # no need to check for check in third square
                    moves.append(Move((r,c),(r,c-2),self.board, isCastleMove = True))
            # else:
            #     if (not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2)):
            #         moves.append(Move((r,c),(r,c-2),self.board, isCastleMove = True))
 
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
        
        
class CastleRights():
    def __init__(self, wKS, bKS, wQS, bQS):
        self.wKS = wKS
        self.bKS = bKS
        self.wQS = wQS
        self.bQS = bQS
        
        
#All possible moves
class Move():
    ranksToRows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}
    filestoCols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filestoCols.items()}
    
    def __init__(self,startSq,endSq,board, isEnpassantMove = False, isCastleMove = False):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]    
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        #pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        #en passant
        self.isEnpassantMove = isEnpassantMove
        if (isEnpassantMove):
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'  # the pawn that was captured enpassant
        #castle move
        self.isCastleMove = isCastleMove
        #castle rights

        self.isCapture = self.pieceCaptured != '--'
        
        #assign each move a unique id
        self.moveID = 1000 * self.startRow + 100 * self.startCol + 10 * self.endRow + self.endCol              #unique move ids
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
    
    #overriding the str() function
    def __str__(self):
        #castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        
        endSquare = self.getRankFile(self.endRow,self.endCol)
        #pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
            
        #two of the same type of piece moving to a square,Nbd if both knights can move to d2
        #also adding + for check move, and # for a checkmate move

        #piece moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare
