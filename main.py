#For user input and handling gamestate

import pygame as p
import ChessEngine
import SmartMoveFinder

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 #for animations
IMAGES = {}

CURRENT_THEME = "theme1"  # Default theme
THEMES = {
    "theme1": "images/",
    "theme2": "images2/"  # Path to your new theme images
}

# Load images based on selected theme
def loadImages(theme_path):
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(theme_path + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = p.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        p.draw.rect(screen, color, self.rect)
        
        font = p.font.SysFont("comicsansms", 20)
        text_surf = font.render(self.text, True, p.Color("black"))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click[0]

# Theme selection screen
def theme_selection_screen():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess Theme Selection")
    clock = p.time.Clock()
    
    # Create buttons
    theme1_button = Button(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 50, "Lichess Theme", p.Color(181,135,99),p.Color(240,218,181) )
    theme2_button = Button(WIDTH//2 - 150, HEIGHT//2 + 10, 300, 50, "Chess.com Theme", p.Color(114,148,81), p.Color(236,236,208))
    
    running = True
    selected_theme = None
    
    while running:
        mouse_pos = p.mouse.get_pos()
        mouse_click = p.mouse.get_pressed()
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return None
                
        # Check button hover and clicks
        theme1_button.check_hover(mouse_pos)
        theme2_button.check_hover(mouse_pos)
        
        if theme1_button.is_clicked(mouse_pos, mouse_click):
            selected_theme = "theme1"
            running = False
            
        if theme2_button.is_clicked(mouse_pos, mouse_click):
            selected_theme = "theme2"
            running = False
            
        # Draw screen
        screen.fill(p.Color(253,251,212))
        
        # Draw title
        font = p.font.Font("freesansbold.ttf", 36)
        title_surf = font.render("Select Chess Theme", True, p.Color("black"))
        title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(title_surf, title_rect)
        
        # Draw buttons
        theme1_button.draw(screen)
        theme2_button.draw(screen)
        
        rule_font = p.font.Font("freesansbold.ttf", 22)
        rules = rule_font.render("Use Z to undo and R for restart", True, p.Color("black"))
        rule_rect = rules.get_rect(center=(WIDTH//2, 3*HEIGHT//4))
        screen.blit(rules, rule_rect)
        p.display.flip()
        clock.tick(MAX_FPS)
        
        # Add small delay to prevent multiple clicks
        if any(mouse_click):
            p.time.delay(200)
            
    return selected_theme


#main code- user input and updating graphics
def main():
    selected_theme = theme_selection_screen()
    if selected_theme is None:
        return
        
    # Load images based on selected theme
    loadImages(THEMES[selected_theme])
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate =False
    # print(gs.board)
    gameOver=False
    playerOne = True  # If a player is playing White it's true, if AI is playing it's false
    playerTwo = False  # If a player is playing Black it's true, if AI is playing it's false
    # loadImages()
    sqSelected = ()       # track of last click of user (tuple: (row, col))
    playerClicks = []     # track of player clicks (two tuples)
    running = True
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()         #coordinates of mouse click
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()          
                        playerClicks = []
                    else:   
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and humanTurn:
                        move=ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        # print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate=True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks=[sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
                    # pass
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # AI turn       
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves, True)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove, isAI=True)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock,selected_theme)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate=False
        drawGameState(screen,gs,validMoves, sqSelected,selected_theme)
        
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, "Black wins by checkmate  " )
            else:
                drawEndGameText(screen, "White wins by checkmate  ")

        elif gs.staleMate:
            gameOver = True
            drawEndGameText(screen, "StaleMate ")
                   
        clock.tick(MAX_FPS)
        p.display.flip()

#Highlights square selected and moves for piece selected
def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.moveLog)) > 0:
        last_move = game_state.moveLog[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.endCol* SQ_SIZE, last_move.endRow* SQ_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.whiteToMove else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
    

def drawGameState(screen,gs,validMoves, sqSelected,theme):
    drawBoard(screen, sqSelected,theme)               #draw the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen,gs.board)     #draw the pieces on the board
    drawPieces(screen, gs.board)     #draw the pieces on the board

def drawBoard(screen,  sqSelected,theme):
    if(theme=="theme1"):
        colors=[p.Color(240, 217, 181, 1), p.Color(181, 136, 99, 1)]
    else:
        colors=[p.Color(236,236,208,1),p.Color(114,148,81,1)]       #square colors
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c)%2)]
            if (r,c) == sqSelected:
                color = p.Color(130,151,105,1)
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                                 HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))
    

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))         #piece on board

def animateMove(move, screen, board, clock,theme):
    """
    Animating a move
    """
    # global colors
    colors=[p.Color(240,217,181,1),p.Color(181,136,99,1)]
    dRow = move.endRow - move.startRow
    dCol = move.endCol - move.startCol
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(dRow) + abs(dCol)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.startRow + dRow * frame / frame_count, move.startCol + dCol * frame / frame_count)
        drawBoard(screen , (row,col),theme)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        end_square = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enpassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                end_square = p.Rect(move.endCol * SQ_SIZE, enpassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
if __name__ == "__main__":
    main()