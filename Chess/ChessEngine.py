import copy
class GameState():
    def __init__(self):
        self.board= [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions= {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves }
        self.whiteToMove= True
        self.moveLog= []
        self.whiteKingLocation= (7, 4)
        self.blackKingLocation= (0, 4)
        self.checkMate= False
        self.staleMate= False
        self.enpassantPossible= ()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight= CastleRights(True, True, True, True)
        self.castleRightLog= [CastleRights(True, True, True, True)]
        self.colsToFiles= {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        self.rowsToRanks= {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"}
        
    
    def makeMove(self, move, promotionChoice= 'Q'):
        self.board[move.startRow][move.startCol]= "--"
        self.board[move.endRow][move.endCol]= move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove= not self.whiteToMove
        if move.pieceMoved== 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved== 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]= move.pieceMoved[0]+ promotionChoice
        
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol]= "--"
        
        if move.pieceMoved[1]== 'p' and abs(move.startRow- move.endRow)==2:
            self.enpassantPossible= ((move.startRow+ move.endRow)//2, move.endCol)
        else:
            self.enpassantPossible= ()

        if move.isCastleMove:
            if move.endCol - move.startCol ==2:
                self.board[move.endRow][move.endCol-1]= self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1]= '--'
            else:
                self.board[move.endRow][move.endCol+1]= self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2]= '--'

        self.enpassantPossibleLog.append(self.enpassantPossible)
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        


    
    def undoMove(self):
        if len(self.moveLog) !=0:
            move= self.moveLog.pop()
            self.board[move.startRow][move.startCol]= move.pieceMoved
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove= not self.whiteToMove
            if move.pieceMoved== 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved== 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol]= '--'
                self.board[move.startRow][move.endCol]= move.pieceCaptured
            
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
            
            self.castleRightLog.pop()
            castle_rights = copy.deepcopy(self.castleRightLog[-1])
            self.currentCastlingRight = castle_rights

            if move.isCastleMove:
                if move.endCol - move.startCol ==2:
                    self.board[move.endRow][move.endCol+1]= self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1]= '--'
                else:
                    self.board[move.endRow][move.endCol-2]= self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1]= '--'
            current_fen = self.to_fen() # Get FEN BEFORE undoing the last state
            
            self.checkMate = False
            self.staleMate = False
    
    def getValidMoves(self):
        tempEnpassantPossible= self.enpassantPossible
        moves= self.getAllPossibleMoves()
        tempCastleRights= CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        if self.whiteToMove:
            self.getCastleMoves(7, 4 , moves)
        else:
            self.getCastleMoves(0, 4, moves)
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove= not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove= not self.whiteToMove
            self.undoMove()
        if len(moves)== 0:
            if self.inCheck():
                self.checkMate= True
            else:
                self.staleMate= True
       

        self.enpassantPossible= tempEnpassantPossible
        self.currentCastlingRight= tempCastleRights
        return moves
    
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol ==7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol ==0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False
    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    
    def squareUnderAttack(self, r, c):
        self.whiteToMove= not self.whiteToMove
        oppMoves= self.getAllPossibleMoves()
        self.whiteToMove= not self.whiteToMove
        for move in oppMoves:
            if move.endRow== r and move.endCol== c:
                return True
        return False



    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn= self.board[r][c][0]
                if (turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece= self.board[r][c][1]
                    self.moveFunctions[piece](r,c, moves)
        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c]=="--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r==6 and self.board[r-2][c]== "--":
                    moves.append(Move((r,c),(r-2,c), self.board))
    
            if c-1>=0:
                if self.board[r-1][c-1][0]== 'b':
                    moves.append(Move((r,c),(r-1,c-1), self.board))
                elif (r-1, c-1)== self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1), self.board, isEnpassantMove=True))

            if c+1<=7:
                if self.board[r-1][c+1][0]== 'b':
                    moves.append(Move((r,c),(r-1,c+1), self.board))
                elif (r-1, c+1)== self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1), self.board, isEnpassantMove=True))
        else:
            if self.board[r+1][c]=="--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r==1 and self.board[r+2][c]== "--":
                    moves.append(Move((r,c),(r+2,c), self.board))
            if c-1>=0:
                if self.board[r+1][c-1][0]== 'w':
                    moves.append(Move((r,c),(r+1,c-1), self.board))
                elif (r+1, c-1)== self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c-1), self.board,  isEnpassantMove=True))
            if c+1<=7:
                if self.board[r+1][c+1][0]== 'w':
                    moves.append(Move((r,c),(r+1,c+1), self.board))
                elif (r+1, c+1)== self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c+1), self.board, isEnpassantMove=True))
    
    def getRookMoves(self, r, c, moves):
        directions= ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor= "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow= r + d[0]*i
                endCol= c + d[1]*i
                if 0<= endRow <8 and 0 <= endCol <8:
                    endPiece= self.board[endRow][endCol]
                    if endPiece== "--":
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                    elif endPiece[0]== enemyColor:
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
                    
    def getKnightMoves(self, r, c, moves):
        knightMoves= ((-2,-1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor= "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow= r + m[0]
            endCol= c + m[1]
            if 0<= endRow <8 and 0 <= endCol <8:
                endPiece= self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol), self.board))


        

    def getBishopMoves(self, r, c, moves):
        directions= ((-1,-1), (-1, 1), (1, -1), (1, 1))
        enemyColor= "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow= r + d[0]*i
                endCol= c + d[1]*i
                if 0<= endRow <8 and 0 <= endCol <8:
                    endPiece= self.board[endRow][endCol]
                    if endPiece== "--":
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                    elif endPiece[0]== enemyColor:
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves= ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor= "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow= r + kingMoves[i][0]
            endCol= c + kingMoves[i][1]
            if 0<= endRow <8 and 0 <= endCol <8:
                endPiece= self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol), self.board))
     
    
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    
    def getKingsideCastleMoves(self, r, c, moves):
        if c + 2 < 8 and self.board[r][c+1]== '--' and self.board[r][c+2]== '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c), (r, c+2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1]== '--' and self.board[r][c-2]== '--' and self.board[r][c-3]== '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))
    
    def to_chess_board(self):
        """
        Converts the current game state to a python-chess Board object.
        """
        import chess
        fen = self.to_fen()
        return chess.Board(fen)
    def to_fen(self):
        """
        Converts the current board state to a FEN string.
        """
        fen = ""
        # 1. Piece placement
        for r in range(8):
            empty = 0
            for c in range(8):
                piece = self.board[r][c]
                if piece == '--':
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    
                    p_type = piece[1]
                    p_color = piece[0]
                    
                    if p_color == 'w':
                        fen += p_type.upper()
                    else:
                        fen += p_type.lower()
            if empty > 0:
                fen += str(empty)
            if r < 7:
                fen += '/'
        
        # 2. Active color
        fen += ' ' + ('w' if self.whiteToMove else 'b')

        # 3. Castling availability
        fen += ' '
        castling = ""
        if self.currentCastlingRight.wks: castling += 'K'
        if self.currentCastlingRight.wqs: castling += 'Q'
        if self.currentCastlingRight.bks: castling += 'k'
        if self.currentCastlingRight.bqs: castling += 'q'
        fen += castling if castling else '-'

        # 4. En passant target square
        fen += ' '
        if self.enpassantPossible:
            fen += self.colsToFiles[self.enpassantPossible[1]] + self.rowsToRanks[self.enpassantPossible[0]]
        else:
            fen += '-'
            
        # 5. Halfmove clock (not essential for this purpose, can be 0)
        fen += ' 0'
        # 6. Fullmove number (not essential, can be 1)
        fen += ' 1'

        return fen
    
    


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks= wks
        self.bks= bks
        self.wqs= wqs
        self.bqs= bqs

        
                    

class Move():
    ranksToRows= {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks= {v: k for k,v in ranksToRows.items()}
    filesToCols= {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles= {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove= False, isCastleMove= False):
        self.startRow= startSq[0]
        self.startCol= startSq[1]
        self.endRow= endSq[0]
        self.endCol= endSq[1]
        self.pieceMoved= board[self.startRow][self.startCol]
        self.pieceCaptured= board[self.endRow][self.endCol]
      

        self.isPawnPromotion= (self.pieceMoved=='wp' and self.endRow==0) or (self.pieceMoved== 'bp' and self.endRow==7)
        self.isEnpassantMove= isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured= 'wp' if self.pieceMoved== 'bp' else 'bp'

        self.isCastleMove= isCastleMove
        self.moveID= self.startRow *1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

           