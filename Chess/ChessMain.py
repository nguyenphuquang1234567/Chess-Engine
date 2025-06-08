import pygame as p
import ChessEngine
import sys
import chess 
import chess.engine
engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish")
WIDTH= 512 +55
HEIGHT= 512
DIMENSION= 8
SQ_SIZE= HEIGHT // DIMENSION
MAX_FPS=15
IMAGES= {}

def loadImages():
    pieces=['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece]= p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    p.mixer.init()
    move_sound = p.mixer.Sound("Chess/sound/move.wav")
    capture_sound = p.mixer.Sound("Chess/sound/capture.wav")
    start_game = p.mixer.Sound("Chess/sound/r.wav")
    castle = p.mixer.Sound("Chess/sound/castle.wav")
    check = p.mixer.Sound("Chess/sound/Check.wav")
    gameover = p.mixer.Sound("Chess/sound/gameover.wav")

    screen= p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock= p.time.Clock()
    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()
    mode = choose_game_mode_gui(screen)
    colorChoice = getPlayerColor(screen)
    
    validMoves= gs.getValidMoves()
    moveMade= False
    animate= False
    loadImages()
    running= True
    sqSelected= ()
    playerClicks= []
    gameOver = False

     # --- AI Integration Start ---
    # Add these lines to your main function
    # Choose if a player is human or AI
    playerOne = True if colorChoice == 'white' else False 
    playerTwo = False if colorChoice == 'white' else True
    eval_score = update_evaluation(gs, engine)

    waitingForHumanMove = False

    while running:
        isHumanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running= False
                engine.quit()
            elif e.type== p.MOUSEBUTTONDOWN:
                if mode == "ENGINE":
                    if colorChoice == 'white':
                     if not gameOver and isHumanTurn:
                        location= p.mouse.get_pos()
                        col= location[0]//SQ_SIZE
                        row = location[1]// SQ_SIZE
                        if sqSelected== (row,col):
                            sqSelected= ()
                            playerClicks= []
                        else:
                            sqSelected= (row,col)
                            playerClicks.append(sqSelected)
                        
                        if len(playerClicks)==2:
                            move= ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print("\n" + move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    if validMoves[i].isPawnPromotion:
                                        promotionChoice = drawPromotionMenu(screen, gs.whiteToMove and 'w' or 'b')
                                        gs.makeMove(validMoves[i], promotionChoice)
                                        if move.pieceCaptured != "--" and not gs.inCheck():
                                            capture_sound.play()
                                        else:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                move_sound.play()
                                    else:
                                        gs.makeMove(validMoves[i])
                                        if validMoves[i].isEnpassantMove:
                                            capture_sound.play()
                                        elif move.pieceCaptured != "--" and not gs.inCheck():
                                            capture_sound.play()
                                        elif validMoves[i].isCastleMove:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                castle.play()
                                        else:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                move_sound.play()
                                    moveMade= True
                                    animate= True
                                    waitingForHumanMove = False
                                    sqSelected=()
                                    playerClicks=[]
                            if not moveMade:
                                playerClicks=[sqSelected]
                    if colorChoice == 'black':
                     if not gameOver and isHumanTurn:
                        location= p.mouse.get_pos()
                        col= location[0]//SQ_SIZE
                        row = 7 - location[1]// SQ_SIZE
                        if sqSelected== (row,col):
                            sqSelected= ()
                            playerClicks= []
                        else:
                            sqSelected= (row,col)
                            playerClicks.append(sqSelected)
                        
                        if len(playerClicks)==2:
                            move= ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print("\n" + move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    if validMoves[i].isPawnPromotion:
                                        promotionChoice = drawPromotionMenu(screen, gs.whiteToMove and 'w' or 'b')
                                        gs.makeMove(validMoves[i], promotionChoice)
                                        if move.pieceCaptured != "--" and not gs.inCheck():
                                            capture_sound.play()
                                        else:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                move_sound.play()
                                    else:
                                        gs.makeMove(validMoves[i])
                                        if validMoves[i].isEnpassantMove:
                                            capture_sound.play()
                                        elif move.pieceCaptured != "--" and not gs.inCheck():
                                            capture_sound.play()
                                        elif validMoves[i].isCastleMove:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                castle.play()
                                        else:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                move_sound.play()
                                    moveMade= True
                                    animate= True
                                    waitingForHumanMove = False
                                    sqSelected=()
                                    playerClicks=[]
                            if not moveMade:
                                playerClicks=[sqSelected]
        
                
                elif mode == "PVP": 
                 if colorChoice == 'white':
                    if not gameOver:
                        location= p.mouse.get_pos()
                        col= location[0]//SQ_SIZE
                        row = location[1]// SQ_SIZE
                        if sqSelected== (row,col):
                            sqSelected= ()
                            playerClicks= []
                        else:
                            sqSelected= (row,col)
                            playerClicks.append(sqSelected)
                        
                        if len(playerClicks)==2:
                            move= ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print("\n" + move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    if validMoves[i].isPawnPromotion:
                                        promotionChoice = drawPromotionMenu(screen, gs.whiteToMove and 'w' or 'b')
                                        gs.makeMove(validMoves[i], promotionChoice)
                                        if move.pieceCaptured != "--" and not gs.inCheck():
                                            capture_sound.play()
                                        else:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                move_sound.play()
                                    else:
                                        gs.makeMove(validMoves[i])
                                        if validMoves[i].isEnpassantMove:
                                            capture_sound.play()

                                        elif move.pieceCaptured != "--" and not gs.inCheck():
                                            capture_sound.play()
                                        elif validMoves[i].isCastleMove:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                castle.play()
                                        else:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                move_sound.play()
                                    moveMade= True
                                    animate= True
                                    waitingForHumanMove = False
                                    sqSelected=()
                                    playerClicks=[]
                            if not moveMade:
                                playerClicks=[sqSelected]
                 elif colorChoice == 'black':
                    if not gameOver:
                        location= p.mouse.get_pos()
                        col= location[0]//SQ_SIZE
                        row = 7- location[1]// SQ_SIZE
                        if sqSelected== (row,col):
                            sqSelected= ()
                            playerClicks= []
                        else:
                            sqSelected= (row,col)
                            playerClicks.append(sqSelected)
                        
                        if len(playerClicks)==2:
                            move= ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print("\n" + move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    if validMoves[i].isPawnPromotion:
                                        promotionChoice = drawPromotionMenu(screen, gs.whiteToMove and 'w' or 'b')
                                        gs.makeMove(validMoves[i], promotionChoice)
                                        if move.pieceCaptured != "--" and not gs.inCheck():
                                            capture_sound.play()
                                        else:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                move_sound.play()
                                    else:
                                        gs.makeMove(validMoves[i])
                                        if validMoves[i].isEnpassantMove:
                                            capture_sound.play()

                                        elif move.pieceCaptured != "--" and not gs.inCheck():
                                            capture_sound.play()
                                        elif validMoves[i].isCastleMove:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                castle.play()
                                        else:
                                            if gs.inCheck() or (gs.inCheck() and move.pieceCaptured != "--"):
                                                check.play()
                                            else:
                                                move_sound.play()
                                    moveMade= True
                                    animate= True
                                    waitingForHumanMove = False
                                    sqSelected=()
                                    playerClicks=[]
                            if not moveMade:
                                playerClicks=[sqSelected]

            elif e.type== p.KEYDOWN:
                if e.key== p.K_z:
                    gameOver = False
                    gs.undoMove()
                    move_sound.play()
                    moveMade= True
                    animate= False
                    waitingForHumanMove = True
                elif e.key== p.K_r:
                    mode = choose_game_mode_gui(screen)
                    colorChoice = getPlayerColor(screen)
                    if colorChoice == 'white':
                        start_game.play()
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected= ()
                        playerClicks= []
                        gameOver = False
                        moveMade = False
                        animate = False
                        waitingForHumanMove = True
                        eval_score = update_evaluation(gs, engine)
                    elif colorChoice == 'black':
                        start_game.play()
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected= ()
                        playerClicks= []
                        gameOver = False
                        moveMade = False
                        animate = False
                        waitingForHumanMove = False
                        eval_score = update_evaluation(gs, engine)
                    

        if not gameOver and not isHumanTurn and not waitingForHumanMove and mode=="ENGINE":
            board = gs.to_chess_board()
            result = engine.play(board, chess.engine.Limit(time=1.6)) 
            ai_move_uci = result.move.uci()
            # Convert UCI move to your Move object
            start_sq = chess.parse_square(ai_move_uci[0:2])
            end_sq = chess.parse_square(ai_move_uci[2:4])
            start_row = 7 - chess.square_rank(start_sq)
            start_col = chess.square_file(start_sq)
            end_row = 7 - chess.square_rank(end_sq)
            end_col = chess.square_file(end_sq)

            ai_move = ChessEngine.Move((start_row, start_col), (end_row, end_col), gs.board)
            
            for i in range(len(validMoves)):
                if ai_move == validMoves[i]:
                    if validMoves[i].isPawnPromotion:
                        promotion_choice = result.move.promotion
                        if promotion_choice:
                            gs.makeMove(validMoves[i], chess.piece_symbol(promotion_choice).upper())
                            if ai_move.pieceCaptured != "--" and not gs.inCheck():
                                capture_sound.play()
                            else:
                                if gs.inCheck() or (gs.inCheck() and ai_move.pieceCaptured != "--"):
                                    check.play()
                                else:
                                    move_sound.play()
                        else:
                            gs.makeMove(validMoves[i])
                            if ai_move.pieceCaptured != "--" and not gs.inCheck():
                                capture_sound.play()
                            else:
                                if gs.inCheck() or (gs.inCheck() and ai_move.pieceCaptured != "--"):
                                    check.play()
                                else:
                                    move_sound.play()
                    else:
                        gs.makeMove(validMoves[i])
                        if validMoves[i].isEnpassantMove:
                            capture_sound.play()
                        elif ai_move.pieceCaptured != "--" and not gs.inCheck():
                            capture_sound.play()
                        elif validMoves[i].isCastleMove:
                            if gs.inCheck() or (gs.inCheck() and ai_move.pieceCaptured != "--"):
                                check.play()
                            else:
                                castle.play()
                        else:
                            if gs.inCheck() or (gs.inCheck() and ai_move.pieceCaptured != "--"):
                                check.play()
                            else:
                                move_sound.play()
                    moveMade = True
                    animate = True
                    waitingForHumanMove = True
        elif mode == "Button": 
                if not gameOver:
                    board = gs.to_chess_board()
                    result = engine.play(board, chess.engine.Limit(time=1.6)) 
                    ai_move_uci = result.move.uci()
                    # Convert UCI move to your Move object
                    start_sq = chess.parse_square(ai_move_uci[0:2])
                    end_sq = chess.parse_square(ai_move_uci[2:4])
                    start_row = 7 - chess.square_rank(start_sq)
                    start_col = chess.square_file(start_sq)
                    end_row = 7 - chess.square_rank(end_sq)
                    end_col = chess.square_file(end_sq)

                    ai_move = ChessEngine.Move((start_row, start_col), (end_row, end_col), gs.board)
                    
                    for i in range(len(validMoves)):
                        if ai_move == validMoves[i]:
                            if validMoves[i].isPawnPromotion:
                                promotion_choice = result.move.promotion
                                if promotion_choice:
                                    gs.makeMove(validMoves[i], chess.piece_symbol(promotion_choice).upper())
                                    if ai_move.pieceCaptured != "--" and not gs.inCheck():
                                        capture_sound.play()
                                    else:
                                        if gs.inCheck() or (gs.inCheck() and ai_move.pieceCaptured != "--"):
                                            check.play()
                                        else:
                                            move_sound.play()
                                else:
                                    gs.makeMove(validMoves[i])
                                    if ai_move.pieceCaptured != "--" and not gs.inCheck():
                                        capture_sound.play()
                                    else:
                                        if gs.inCheck() or (gs.inCheck() and ai_move.pieceCaptured != "--"):
                                            check.play()
                                        else:
                                            move_sound.play()
                            else:
                                gs.makeMove(validMoves[i])
                                if validMoves[i].isEnpassantMove:
                                    capture_sound.play()
                                elif ai_move.pieceCaptured != "--" and not gs.inCheck():
                                    capture_sound.play()
                                elif validMoves[i].isCastleMove:
                                    if gs.inCheck() or (gs.inCheck() and ai_move.pieceCaptured != "--"):
                                        check.play()
                                    else:
                                        castle.play()
                                else:
                                    if gs.inCheck() or (gs.inCheck() and ai_move.pieceCaptured != "--"):
                                        check.play()
                                    else:
                                        move_sound.play()
                        moveMade = True
                        animate = True
                        waitingForHumanMove = False

        if moveMade:
            if animate and colorChoice=='white':
                animateMove(gs.moveLog[-1], screen, gs.board, clock, False)
            elif animate and colorChoice == 'black':
                animateMove(gs.moveLog[-1], screen, gs.board, clock, True)
            validMoves= gs.getValidMoves()
            moveMade= False
            animate= False
            eval_score = update_evaluation(gs, engine)
        if colorChoice == 'white':
            drawGameState(screen, gs, validMoves, sqSelected, flipped=False)
        elif colorChoice=='black':
            drawGameState(screen, gs, validMoves, sqSelected, flipped=True)
        drawEvaluationBar(screen, eval_score)
        
        
            
    
            
           
        if gs.checkMate:
            if not gameOver:
                gameover.play()
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            if not gameOver:
                gameover.play()
            gameOver = True
            drawText(screen, 'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()
        

def highlightSquare(screen, gs, validMoves, sqSelected, flipped=False):
    if sqSelected != ():
        r, c= sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s= p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            # Adjust drawing based on 'flipped'
            display_r = 7 - r if flipped else r
            screen.blit(s, (c* SQ_SIZE, display_r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    display_end_row = 7 - move.endRow if flipped else move.endRow
                    screen.blit(s, (move.endCol * SQ_SIZE, display_end_row * SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected, flipped=False): # Add flipped parameter
    drawBoard(screen, flipped)
    highlightSquare(screen, gs, validMoves, sqSelected, flipped)
    drawPieces(screen, gs.board, flipped)
    
def drawBoard(screen, flipped=False): 
    global colors
    colors = [p.Color("gray"), p.Color("white")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            display_row = 7 - r if flipped else r
            color = colors[(display_row + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, display_row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board, flipped=False): 
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                display_row = 7 - r if flipped else r
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, display_row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock, flipped=False): # Add flipped parameter
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 3
    frameCount = (abs(dR)+ abs(dC))* framesPerSquare
    for frame in range(frameCount +1):
        r, c= (move.startRow + dR * frame/frameCount, move.startCol + dC * frame/ frameCount)
        drawBoard(screen, flipped) # Pass flipped
        drawPieces(screen, board, flipped) # Pass flipped
        color= colors[(move.endRow+ move.endCol)% 2]

        # Adjust drawing based on 'flipped'
        display_end_row = 7 - move.endRow if flipped else move.endRow
        endSquare = p.Rect(move.endCol * SQ_SIZE, display_end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        # Adjust drawing based on 'flipped' for the moving piece
        display_r = 7 - r if flipped else r
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c* SQ_SIZE, display_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(360)


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2,2))

def drawPromotionMenu(screen, color):
    choices = ["Q", "R", "B", "N"]
    pieceKeys = [color + ch for ch in choices]
    menuWidth, menuHeight = 4 * SQ_SIZE, SQ_SIZE
    x = screen.get_width() // 2 - menuWidth // 2
    y = screen.get_height() // 2 - menuHeight // 2
    rect = p.Rect(x, y, menuWidth, menuHeight)

    p.draw.rect(screen, p.Color("white"), rect)
    p.draw.rect(screen, p.Color("black"), rect, 2)

    for i, pieceKey in enumerate(pieceKeys):
        screen.blit(IMAGES[pieceKey], (x + i * SQ_SIZE, y))

    p.display.flip()

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                mx, my = p.mouse.get_pos()
                if rect.collidepoint(mx, my):
                    index = (mx - x) // SQ_SIZE
                    return choices[index]

def choose_game_mode_gui(screen):
    while True:
        pvp_button, engine_button, new_button = draw_mode_selection(screen)
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                if pvp_button.collidepoint(event.pos):
                    return "PVP"
                elif engine_button.collidepoint(event.pos):
                    return "ENGINE"
                elif new_button.collidepoint(event.pos):
                    return "Button"
                

def draw_mode_selection(screen):
    font = p.font.SysFont("Arial", 36, True)
    screen.fill(p.Color("white"))

    pvp_button = p.Rect(150, 200, 200, 60)
    engine_button = p.Rect(150, 300, 200, 60)
    new_button = p.Rect(150, 400, 200, 60)

    p.draw.rect(screen, p.Color("gray"), pvp_button)
    p.draw.rect(screen, p.Color("gray"), engine_button)
    p.draw.rect(screen, p.Color("gray"), new_button)
 

    pvp_text = font.render("PVP", True, p.Color("black"))
    engine_text = font.render("Engine", True, p.Color("black"))
    fontn = p.font.SysFont("Arial", 20, True)  # Set font size to 48
    new_text = fontn.render("Engine vs engine", True, p.Color("black"))


    screen.blit(pvp_text, (pvp_button.x + 60, pvp_button.y + 10))
    screen.blit(engine_text, (engine_button.x + 40, engine_button.y + 10))
    screen.blit(new_text, (new_button.x + 20, new_button.y + 10))

    p.display.flip()
    return pvp_button, engine_button, new_button

def drawPlayerColor(screen):
    font = p.font.SysFont("Arial", 36, True)
    screen.fill(p.Color("white"))

    white_button = p.Rect(150, 200, 200, 60)
    black_button = p.Rect(150, 300, 200, 60)

    p.draw.rect(screen, p.Color("gray"), white_button)
    p.draw.rect(screen, p.Color("gray"), black_button)

    white_text = font.render("White", True, p.Color("black"))
    black_text = font.render("Black", True, p.Color("black"))

    screen.blit(white_text, (white_button.x + 60, white_button.y + 10))
    screen.blit(black_text, (black_button.x + 40, black_button.y + 10))
    p.display.flip()
    return white_button, black_button

def getPlayerColor(screen):
    while True:
        white_button, black_button = drawPlayerColor(screen)
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                if white_button.collidepoint(event.pos):
                    return "white"
                elif black_button.collidepoint(event.pos):
                    return "black"

def update_evaluation(board_state, stockfish_engine):
    board = board_state.to_chess_board()
    info = stockfish_engine.analyse(board, chess.engine.Limit(time=0.1))
    score = info["score"].white().score(mate_score=10000)
    return score if score is not None else 0

def drawEvaluationBar(screen, score):
    EVAL_BAR_WIDTH = 40
    EVAL_BAR_PADDING = 10
    BOARD_WIDTH = 8 * SQ_SIZE
    EVAL_BAR_X = BOARD_WIDTH + EVAL_BAR_PADDING

    # A score of 1000 centipawns (+10.00) will be our visual cap.
    # This prevents the bar from looking skewed with extreme evaluations.
    max_eval = 1000
    
    is_mate = abs(score) > 9000
    if is_mate:
        # If mate is detected, fill the bar completely for the winning side
        eval_for_bar = max_eval if score > 0 else -max_eval
    else:
        eval_for_bar = max(min(score, max_eval), -max_eval)

    # Map the score (from -max_eval to +max_eval) to a percentage of the bar's height
    white_percentage = 0.5 * (1 + eval_for_bar / max_eval)
    
    white_height = HEIGHT * white_percentage
    
    # Draw the bars
    white_rect = p.Rect(EVAL_BAR_X, 0, EVAL_BAR_WIDTH, white_height)
    p.draw.rect(screen, p.Color("white"), white_rect)
    
    black_rect = p.Rect(EVAL_BAR_X, white_height, EVAL_BAR_WIDTH, HEIGHT - white_height)
    p.draw.rect(screen, p.Color(30, 30, 30), black_rect)

    # Draw the score text
    font = p.font.SysFont("Arial", 16, True, False)
    if is_mate:
        mate_in = 10000 - abs(score)
        score_text = f"M{mate_in}"
    else:
        # Convert centipawns to a more readable format (e.g., +1.25)
        score_in_pawns = score / 100.0
        score_text = f"{score_in_pawns:+.2f}"
            
    # Position the text on the dividing line between the two colors
    text_color = p.Color("dark green") 
    text_surface = font.render(score_text, True, text_color)
    text_rect = text_surface.get_rect(center=(EVAL_BAR_X + EVAL_BAR_WIDTH / 2, white_height-7))
    
    # Clamp the text position to keep it from going off-screen
    text_rect.y = max(0, min(text_rect.y, HEIGHT - text_rect.height))
    
    screen.blit(text_surface, text_rect)
                

if __name__== "__main__":
    main()
