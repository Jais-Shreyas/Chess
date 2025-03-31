import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

knightScores = [[1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]]

whitePawnScores = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

blackPawnScores = list(reversed(whitePawnScores))  # Simply flipping the whitePawnScores

# Alternatively, writing it explicitly:
# blackPawnScores = [
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 0, 0, 1, 1, 1],
#     [1, 2, 3, 3, 3, 3, 2, 1],
#     [1, 2, 3, 4, 4, 3, 2, 1],
#     [2, 3, 3, 5, 5, 3, 3, 2],
#     [5, 6, 6, 7, 7, 6, 6, 5],
#     [8, 8, 8, 8, 8, 8, 8, 8],
#     [8, 8, 8, 8, 8, 8, 8, 8]
# ]

bishopScores = [
    [4,3,2,1,1,2,3,4],
    [3,4,3,2,2,3,4,3],
    [2,3,4,3,3,4,3,2],
    [1,2,3,4,4,3,2,1],
    [1,2,3,4,4,3,2,1],
    [2,3,4,3,3,4,3,2],
    [3,4,3,2,2,3,4,3],
    [4,3,2,1,1,2,3,4]
]

rookScores = [
    [4,4,4,4,4,4,4,4],
    [3,3,3,3,3,3,3,3],
    [2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [2,2,2,2,2,2,2,2],
    [3,3,3,3,3,3,3,3],
    [4,4,4,4,4,4,4,4]
]

queenScores = [
    [4,3,3,2,2,3,3,4],
    [3,3,2,2,2,2,3,3],
    [3,2,2,1,1,2,2,3],
    [2,2,1,1,1,1,2,2],
    [2,2,1,1,1,1,2,2],
    [3,2,2,1,1,2,2,3],
    [3,3,2,2,2,2,3,3],
    [4,3,3,2,2,3,3,4]
]

kingScores = [
    [0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,0],
    [0,1,2,2,2,2,1,0],
    [0,1,2,3,3,2,1,0],
    [0,1,2,3,3,2,1,0],
    [0,1,2,2,2,2,1,0],
    [0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0]
]

piecePositionScores = {
    "N": knightScores,
    "B": bishopScores,
    "R": rookScores,
    "Q": queenScores,
    "K": kingScores,
    "wP":whitePawnScores,
    "bP":blackPawnScores
}

weight = {
            "N": .5,
            "B": .3,
            "R": .2,
            "Q": .1,
            "K": .2 , # Change to 10 in the endgame
            "P": .2
        }

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3  # Reduced from 3 to make AI more responsive
num_moves = 0

# Initialize global variables
nextMove = None
counter = 0

# Find the best move on the material alone

# def findBestMove(gs, validMoves):
#     turnMultiplier = 1 if gs.whiteToMove else -1
#     opponentMinMaxScore = CHECKMATE
#     bestPlayerMove = None
#     random.shuffle(validMoves)
#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         opponentMoves = gs.getValidMoves()
#         if gs.staleMate:
#             opponentMaxScore = STALEMATE
#         elif gs.checkMate:
#             opponentMaxScore = -CHECKMATE
#         else:
#             opponentMaxScore = -CHECKMATE
#             for opponentsMove in opponentMoves :
#                 gs.makeMove(opponentsMove)
#                 gs.getValidMoves()
#                 if gs.checkMate:
#                     score = CHECKMATE
#                 elif gs.staleMate:
#                     score = STALEMATE
#                 else:
#                     score = -turnMultiplier * scoreMaterial(gs.board)
#                 if score > opponentMaxScore:
#                     opponentMaxScore = score
#                 gs.undoMove()
#         if opponentMaxScore < opponentMinMaxScore:
#             opponentMinMaxScore = opponentMaxScore
#             bestPlayerMove = playerMove
#         gs.undoMove()
#     return bestPlayerMove


# Helper method to make first recursive call

def findBestMove(gs, validMoves,returnQueue):
    global nextMove,counter 
    nextMove = None
    random.shuffle(validMoves)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1)
    print(counter)
    returnQueue.put(nextMove)


def findMoveMinMax(gs, validMoves, depth, whiteToMove, isAI = False):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    random.shuffle(validMoves)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move, isAI)
            nextMoves = gs.getValidMoves(isAI)
            score = findMoveMinMax(gs, nextMoves, depth - 1, False, isAI)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    print(move,score)
            gs.undoMove()
        return maxScore
    
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move, isAI)
            nextMoves = gs.getValidMoves(isAI)
            score = findMoveMinMax(gs, nextMoves, depth - 1, True, isAI)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


# a positive score is good for white, a negative score is good for black

def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.staleMate:
        return STALEMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                #score it positionally
                piecePositionScore = 0
                if square[1] != 'P':
                    piecePositionScore = piecePositionScores[square[1]][row][col] * weight[square[1]]
                    if square[1] == 'K' and counter >= 23:
                        piecePositionScore *= 5
                else :
                   if counter <= 12:
                        piecePositionScore = piecePositionScores[square][row][col] * 0.2
                   elif counter <= 25:
                       piecePositionScore = piecePositionScores[square][row][col] * 0.3
                   else:
                       piecePositionScore = piecePositionScores[square][row][col] * 0.5

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore
    return score
    

def findMoveNegaMax(gs,validMoves,depth,turnMultiplier):
    global nextMove,counter

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score =  -findMoveNegaMax(gs,nextMoves,depth - 1,-turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove,counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs,nextMoves,depth - 1,-beta,-alpha,-turnMultiplier)  # Fixed recursive call
        gs.undoMove()
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

# Score the board based on material.

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

def findRandomMove(validMoves):
    """
    Picks and returns a random valid move when the AI can't find a good move or times out.
    """
    if validMoves:
        return random.choice(validMoves)
    return None