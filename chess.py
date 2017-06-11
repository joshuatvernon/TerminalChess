import re

class NoneChessBoardPosition(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

class InvalidChessBoardPosition(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

class DeadChessPiece(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

class InvalidChessPieceColour(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

class InvalidChessMove(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

class ChessGame(object):
    """docstring for ChessGame."""
    def __init__(self, player1, player2):
        super().__init__()
        self.chessboard = ChessBoard()
        self.player1 = Player(player1, "White", self.chessboard.get_pieces("White"))
        self.player2 = Player(player2, "Black", self.chessboard.get_pieces("Black"))
        self.player1.set_opposition(self.player2)
        self.player2.set_opposition(self.player1)
        self.turn_player = str(self.player1)
    def __str__(self):
        game_str = "\n" + str(self.player2).center(49, " ") + "\n"
        pieces_str = " "
        for w in self.player1.get_pieces().values():
            if w.get_state() == False:
                pieces_str += w.get_symbol() + " "
        game_str += str(pieces_str).center(49, " ")
        # concatenate each row
        for i in range(8):
            game_str += "\n  -------------------------------------------------\n" + str(8 - i) + " |  "
            for j in range(8):
                game_str += str(self.chessboard.get_board()[i][j]) + "  |  "
            game_str = game_str[:len(game_str)-1]
        game_str += "\n  -------------------------------------------------\n     A     B     C     D     E     F     G     H     \n"
        pieces_str = " "
        for b in self.player2.get_pieces().values():
            if b.get_state() == False:
                pieces_str += b.get_symbol() + " "
        game_str += str(pieces_str).center(49, " ")
        game_str += "\n" + str(self.player1).center(49, " ") + "\n"
        return game_str
    def next_turn(self):
        print(self.turn_player[:len(str(self.turn_player))-8] + "'s turn (A1->B2):")
        move = input().strip()
        if bool(re.match(r'[a-hA-H]{1}[1-8]{1}\-\>[a-hA-H]{1}[1-8]{1}', move)):
            if self.turn_player == str(self.player1):
                if self.player1.set_move(move):
                    # next turn is player 2's
                    self.chessboard.update_board()
                    self.turn_player = str(self.player2)
                else:
                    print("Invalid move, try again!\n")
            else:
                if self.player2.set_move(move):
                    self.chessboard.update_board()
                    # next turn is player 1's
                    self.turn_player = str(self.player1)
                else:
                    print("Invalid move, try again!\n")
        else:
            print("Chess move must be formatted as A1->A2")
            # raise InvalidChessMove("Chess move must be formatted as A1->A2")

class Player(object):
    """docstring for Player."""
    def __init__(self, name, colour, pieces=None):
        super().__init__()
        self.name = name
        self.colour = colour
        self.pieces = pieces
        self.taken_pieces = None
        self.opposition = None
    def __str__(self):
        return self.name + " (" + self.colour + ")"
    def set_move(self, move):
        pos1 = (move[:1], int(move[1:2]))
        pos2 = (move[4:5], int(move[5:6]))
        for p in self.pieces.values():
            if p.get_position() == pos1:
                taking = False
                # check for pieces being taken
                for o in self.opposition.get_pieces().values():
                    if o.get_position() == pos2:
                        taking = True
                        o.set_state(False)
                # check for clashing ally pieces
                for a in self.pieces.values():
                    if a.get_position() == pos2:
                        return False
                if p.valid_move(pos2, taking):
                    p.
                    p.set_position(pos2)
                    return True
        return False
    def set_opposition(self, opposition):
        self.opposition = opposition
    def get_pieces(self):
        return self.pieces

# Movement edge cases
# - can't move onto a position with a ally piece occupying it already - DONE
# - must move to a valid position based on it ability e.g. diagonal, straight - DONE (not yet tested fully)
# - can't move through other pieces - except Knight
# - pawns start with 2 space ability - DONE
# - pawns can take pieces sideways - DONE
# - castling with king and rooks
# - can't move pieces if being checked unless it breaks the check
# - king can't move into check
# - pieces can't be moved if they leave the king in check

class ChessPiece(object):
    """docstring for ChessPiece."""
    def __init__(self, colour, name, symbol, position=None):
        super().__init__()
        self.colour = colour
        self.name = name
        self.symbol = symbol
        self.state = True
        self.position = None
        if position:
            self.set_position(position)
    def __str__(self):
        return self.colour + " " + self.name
    def get_symbol(self):
        return self.symbol
    def get_state(self):
        return self.state
    def set_state(self, state):
        self.state = state
    def get_position(self):
        if self.position:
            return self.position
        else:
            raise NoneChessBoardPosition("Accessing chess piece that doesn't have a set position")
    def set_position(self, position):
        if position == None or (isinstance(position, tuple) and len(position) == 2 and \
        isinstance(position[0], str) and isinstance(position[1], int)):
            self.position = position
        else:
            raise InvalidChessBoardPosition("Invalid Chess Board Positon, must be of string, int pair inside a tuple")

class King(ChessPiece):
    """docstring for King."""
    def __init__(self, colour, position=None):
        if colour.lower() == "white":
            super().__init__(colour, "King", chr(9812), position)
        elif colour.lower() == "black":
            super().__init__(colour, "King", chr(9818), position)
        else:
            raise InvalidChessPieceColour("Chess pieces can only be White or Black.")
    def valid_move(self, new_pos, taking=False):
        cypher = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        if abs(cypher[self.position[0]] - cypher[new_pos[0]]) > 1 or abs(self.position[1] - new_pos[1]) > 1:
            return False
        return True

class Queen(ChessPiece):
    """docstring for Queen."""
    def __init__(self, colour, position=None):
        if colour.lower() == "white":
            super().__init__(colour, "Queen", chr(9813), position)
        elif colour.lower() == "black":
            super().__init__(colour, "Queen", chr(9819), position)
        else:
            raise InvalidChessPieceColour("Chess pieces can only be White or Black.")
    def valid_move(self, new_pos, taking=False):
        if (abs(cypher[self.position[0]] - cypher[new_pos[0]]) == 0 or abs(self.position[1] - new_pos[1]) == 0) or \
        (abs(cypher[self.position[0]] - cypher[new_pos[0]]) == abs(self.position[1] - new_pos[1]) == 0):
            return True
        return False

class Bishop(ChessPiece):
    """docstring for Bishop."""
    def __init__(self, colour, position=None):
        if colour.lower() == "white":
            super().__init__(colour, "Bishop", chr(9815), position)
        elif colour.lower() == "black":
            super().__init__(colour, "Bishop", chr(9821), position)
        else:
            raise InvalidChessPieceColour("Chess pieces can only be White or Black.")
    def valid_move(self, new_pos, taking=False):
        cypher = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        if self.position[0] == new_pos[0] or self.position[1] == new_pos[1]:
            return False
        if abs(cypher[self.position[0]] - cypher[new_pos[0]]) == abs(self.position[1] - new_pos[1]):
            return True
        return False

class Knight(ChessPiece):
    """docstring for Knight."""
    def __init__(self, colour, position=None):
        if colour.lower() == "white":
            super().__init__(colour, "Knight", chr(9816), position)
        elif colour.lower() == "black":
            super().__init__(colour, "Knight", chr(9822), position)
        else:
            raise InvalidChessPieceColour("Chess pieces can only be White or Black.")
    def valid_move(self, new_pos, taking=False):
        cypher = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        if (abs(cypher[self.position[0]] - cypher[new_pos[0]]) == 1 and abs(self.position[1] - new_pos[1]) == 2) or \
        (abs(cypher[self.position[0]] - cypher[new_pos[0]]) == 2 and abs(self.position[1] - new_pos[1]) == 1):
            return True
        return False

class Rook(ChessPiece):
    """docstring for Rook."""
    def __init__(self, colour, position=None):
        if colour.lower() == "white":
            super().__init__(colour, "Rook", chr(9814), position)
        elif colour.lower() == "black":
            super().__init__(colour, "Rook", chr(9820), position)
        else:
            raise InvalidChessPieceColour("Chess pieces can only be White or Black.")
    def valid_move(self, new_pos, taking=False):
        if self.position[0] == new_pos[0] or self.position[1] == new_pos[1]:
            return True
        return False

class Pawn(ChessPiece):
    """docstring for Pawn."""
    def __init__(self, colour, position=None):
        self.first_move = True
        if colour.lower() == "white":
            super().__init__(colour, "Pawn", chr(9817), position)
        elif colour.lower() == "black":
            super().__init__(colour, "Pawn", chr(9823), position)
        else:
            raise InvalidChessPieceColour("Chess pieces can only be White or Black.")
    def valid_move(self, new_pos, taking=False):
        if new_pos[1] <= self.position[1] or new_pos[1] > self.position[1] + 2 \
        (new_pos[1] > self.position[1] + 1 and self.first_move == False) \
        abs(cypher[new_pos[0]] - cypher[self.position[0]]) > 1 \
        (abs(cypher[new_pos[0]] - cypher[self.position[0]]) == 1 and taking = False):
            return False
        self.first_move = False
        return True

class ChessBoard(object):
    """docstring for ChessBoard."""
    def __init__(self):
        super().__init__()
        self.board = []
        self.white_pieces = {}
        self.black_pieces = {}
        self.__setup_board()
        self.__create_pieces()
        self.__setup_pieces()
    def __setup_board(self):
        toggle = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(8):
            self.board.append([]) # append new row on board
            for j in range(8):
                if j % 2 == toggle:
                    self.board[i].append(ChessPosition("White", letters[j], 8 - i))
                else:
                    self.board[i].append(ChessPosition("Black", letters[j], 8 - i))
            toggle = abs(toggle - 1) # toggle row starting colour
    def __create_pieces(self):
        # create black pieces
        for i in range(8):
            exec('self.black_pieces["Pawn' + str(i+1) + '"] = Pawn("Black", self.board[1][i].get_position())')
        self.black_pieces["Rook1"] = Rook("Black", self.board[0][0].get_position())
        self.black_pieces["Knight1"] = Knight("Black", self.board[0][1].get_position())
        self.black_pieces["Bishop1"] = Bishop("Black", self.board[0][2].get_position())
        self.black_pieces["King"] = King("Black", self.board[0][3].get_position())
        self.black_pieces["Queen"] = Queen("Black", self.board[0][4].get_position())
        self.black_pieces["Bishop2"] = Bishop("Black", self.board[0][5].get_position())
        self.black_pieces["Knight2"] = Knight("Black", self.board[0][6].get_position())
        self.black_pieces["Rook2"] = Rook("Black", self.board[0][7].get_position())
        # create white pieces
        for i in range(8):
            exec('self.white_pieces["Pawn' + str(i+1) + '"] = Pawn("White", self.board[6][i].get_position())')
        self.white_pieces["Rook1"] = Rook("White", self.board[7][0].get_position())
        self.white_pieces["Knight1"] = Knight("White", self.board[7][1].get_position())
        self.white_pieces["Bishop1"] = Bishop("White", self.board[7][2].get_position())
        self.white_pieces["Queen"] = Queen("White", self.board[7][3].get_position())
        self.white_pieces["King"] = King("White", self.board[7][4].get_position())
        self.white_pieces["Bishop2"] = Bishop("White", self.board[7][5].get_position())
        self.white_pieces["Knight2"] = Knight("White", self.board[7][6].get_position())
        self.white_pieces["Rook2"] = Rook("White", self.board[7][7].get_position())
    def get_piece(self, colour, piece):
        # actually should pass the player in instead of the piece and call player.get_colour() to return the correct piece
        if colour == "White":
            if self.white_pieces[piece].get_state() == True:
                return self.white_pieces[piece]
            else:
                raise DeadChessPiece("Attempting to access a dead chess piece")
        else:
            if self.black_pieces[piece].get_state() == True:
                return self.black_pieces[piece]
            else:
                raise DeadChessPiece("Attempting to access a dead chess piece")
    def get_pieces(self, colour):
        if colour == "White":
            return self.white_pieces
        elif colour == "Black":
            return self.black_pieces
        else:
            raise InvalidChessPieceColour("Chess pieces can only be White or Black.")
    def set_pieces(self, colour, pieces):
        if colour == "White":
            self.white_pieces = pieces
        elif colour == "Black":
            self.black_pieces = pieces
        else:
            raise InvalidChessPieceColour("Chess pieces can only be White or Black.")
    def __setup_pieces(self):
        # Setup black rows
        self.board[0][0].set_piece(self.black_pieces["Rook1"])
        self.board[0][1].set_piece(self.black_pieces["Knight1"])
        self.board[0][2].set_piece(self.black_pieces["Bishop1"])
        self.board[0][3].set_piece(self.black_pieces["King"])
        self.board[0][4].set_piece(self.black_pieces["Queen"])
        self.board[0][5].set_piece(self.black_pieces["Bishop2"])
        self.board[0][6].set_piece(self.black_pieces["Knight2"])
        self.board[0][7].set_piece(self.black_pieces["Rook2"])
        for i in range(8):
            eval('self.board[1][i].set_piece(self.black_pieces["Pawn' + str(i+1) + '"])')
        # Setup white rows
        for i in range(8):
            eval('self.board[6][i].set_piece(self.white_pieces["Pawn' + str(i+1) + '"])')
        self.board[7][0].set_piece(self.white_pieces["Rook1"])
        self.board[7][1].set_piece(self.white_pieces["Knight1"])
        self.board[7][2].set_piece(self.white_pieces["Bishop1"])
        self.board[7][3].set_piece(self.white_pieces["Queen"])
        self.board[7][4].set_piece(self.white_pieces["King"])
        self.board[7][5].set_piece(self.white_pieces["Bishop2"])
        self.board[7][6].set_piece(self.white_pieces["Knight2"])
        self.board[7][7].set_piece(self.white_pieces["Rook2"])
    def get_board(self):
        return self.board
    def update_board(self):
        cypher = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        for i in range(8):
            for j in range(8):
                self.board[i][j].set_piece(None)
                for w in self.white_pieces.values():
                    pos = w.get_position()
                    if cypher[pos[0]] == j and pos[1] == 8-i and w.get_state() == True:
                        self.board[i][j].set_piece(w)
                for b in self.black_pieces.values():
                    pos = b.get_position()
                    if cypher[pos[0]] == j and pos[1] == 8-i and b.get_state() == True:
                        self.board[i][j].set_piece(b)

    def __str__(self):
        board_string = ""
        for i in range(8):
            for j in range(8):
                board_string += "("
                board_string = board_string + str(self.board[i][j].get_piece()) + ", " if self.board[i][j].get_piece() != None else board_string
                board_string += self.board[i][j].get_colour() + "-" + self.board[i][j].get_letter() + str(self.board[i][j].get_number()) + "), "
            board_string = board_string[:len(board_string)-2] + "\n"
        return board_string

class ChessPosition(object):
    """docstring for ChessPosition."""
    def __init__(self, colour, letter, number, piece=None):
        super().__init__()
        self.colour = colour
        self.letter = letter
        self.number = number
        self.piece = piece
    def get_colour(self):
        return self.colour
    def get_letter(self):
        return self.letter
    def get_number(self):
        return self.number
    def get_position(self):
        """Return a tuple of the position."""
        return (self.letter, self.number)
    def get_piece(self):
        """Return current piece on position if there is one, else return None"""
        return self.piece
    def set_piece(self, piece):
        """Set the piece that is currently on the position."""
        self.piece = piece
    def __str__(self):
        return self.piece.get_symbol() if self.piece else " "

def main():
    c = ChessGame("Joshua", "Mitchell")
    while True:
        print(c)
        c.next_turn()

if __name__ == "__main__":
    main()
