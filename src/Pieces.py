__author__ = 'yaron'

import json

class Piece():

    WHITE = 1
    BLACK = 0

    def __init__(self, row,col, color):
        """
        :param row: Row index of the piece
        :param col: Col index of the piece
        :param color: Color of the piece
        :except Exception: Wrong color
        :return: None
        """
        if not (color is self.WHITE or color is self.BLACK):
            raise Exception("Wrong color")
        self.row = row
        self.col = col
        self.color = color

    def __str__(self):
        """
        :return: String representation
        """
        return "%s(row - %d, col - %d)" %("W" if self.color==self.WHITE else "B", self.row, self.col)

    def __unicode__(self):
        """
        :return: String representation
        """
        return "%s(row - %d, col - %d)" %("W" if self.color==self.WHITE else "B", self.row, self.col)

    def to_json(self):
        return { 'row' : self.row , 'col' : self.col }

    def move(self, d_row, d_col):
        """
        Move the piece to the desired coordinates
        :param d_row: The desired row to move
        :param d_col: The desired column to move
        :return: True on success
        """
        if self.check_borders(d_row, d_col) and self.check_pos(d_row, d_col):
            self.col = d_col
            self.row = d_row
            return True
        return False
    
    def check_borders(self, d_row, d_col):
        """
        Check if the coordinates are inside the board
        :param d_row: The desired row
        :param d_col: The desired column
        :param N: Dimension
        :return:
        """
        if d_row < 0 or d_row > 7:
            return False
        if d_col < 0 or d_col > 7:
            return False

        return True

    def check_pos(self, d_row, d_col):
        """
        Check if the new position is valid
        :param d_row: The desired row
        :param d_col: The desired column
        :return: True on success
        """
        return False

    def restricted_positions(self, king=None):
        """
        :return: The restricted positions
        """
        return []

    def possible_moves(self, king=None):
        """
        :return: The possible moves
        """
        return []


class King(Piece):
    """
    This is the King class which inherits from Piece
    """

    def check_pos(self, d_row, d_col):
        """
        Check if the new position is valid
        :param d_row: The desired row
        :param d_col: The desired column
        :return: True on success
        """
        dist = abs(d_row-self.row) + abs(d_col-self.col)

        if dist == 1 or (dist == 2 and self.row != d_row and self.col != d_col):
            return True
        else:
            return False

    def restricted_positions(self, king=None):
        lis = self.possible_moves()
        lis.append((self.row,self.col))
        return lis

    def possible_moves(self, king=None):
        rows = []
        cols = []
        if self.row + 1 <= 7:
            rows.append(self.row+1)
        if self.row - 1 >= 0:
            rows.append(self.row-1)
        if self.col + 1 <= 7:
            cols.append(self.col+1)
        if self.col - 1 >= 0:
            cols.append(self.col-1)
        rows.append(self.row)
        cols.append(self.col)

        moves = [(row, col) for row in rows for col in cols]
        moves.remove((self.row, self.col))

        return moves


class Rook(Piece):
    """
    This is the Rook class which inherits from Piece
    """

    def check_pos(self, d_row, d_col):
        if d_row == self.row and d_col != self.col:
            return True
        if d_row != self.row and d_col == self.col:
            return True

        return False

    def possible_moves(self, king=None):
        pos = []
        for x in range(0,8):
            if x != self.row:
                pos.append((x, self.col))
            if x != self.col:
                pos.append((self.row, x))

        for p in pos:

            if p == (king.row, king.col):
                pos.remove(p)

            if (self.row == king.row and king.col > self.col):
                if p[1]>king.col:
                    pos.remove(p)
            if (self.row == king.row and king.col < self.col):
                if p[1]<king.col:
                    pos.remove(p)
            if (self.col == king.col and king.row > self.row):
                if p[0]>king.row:
                    pos.remove(p)
            if (self.col == king.col and king.row < self.row):
                if p[0]<king.row:
                    pos.remove(p)

        return pos

    def restricted_positions(self, king=None):
        lis = self.possible_moves(king)
        lis.append((self.row, self.col))
        return lis

    def check_move_validity(self, piece, row, col):
        if row != self.row and col != self.col:
            return False
        if row == piece.row and col == piece.col:
            return False
        if col < piece.col and col < self.col and  self.col > piece.col and piece.row == self.row:
            return False
        elif row < piece.row and row < self.row and self.row < piece.row and piece.col == self.col:
            return False
        elif col > piece.col and col > self.col and self.col < piece.col and piece.row == self.row:
            return False
        elif row > piece.row and row > self.row and self.row > piece.row and piece.col == self.col:
            return False
        return True


class Bishop(Piece):

    def move(self, d_row, d_col):
        """
        Move the piece to the desired coordinates
        :param d_row: The desired row to move
        :param d_col: The desired column to move
        :return: True on success
        """
        if self.check_borders(d_row, d_col):
            self.col = d_col
            self.row = d_row
            return True
        return False
    

    def check_pos(self, d_row, d_col):
        """
        Check if the next move is valid
        :param d_row: The desired row
        :param d_col: The desired column
        :return: True on success
        """
        return (d_row, d_col) in self.possible_moves()

    def restricted_positions(self, king=None):
        """
        :return: The restricted positions
        """
        return self.possible_moves(king)
    
    def is_in_diags(self, d_row, d_col):
        """
        Check if the desired position is in piece diagonals
        :return: True if it is the case
                 False otherwise
        """
        all_diags = []
        for k in range(0,8):
            all_diags.append((self.row + k, self.col + k))
            all_diags.append((self.row - k, self.col - k))
            all_diags.append((self.row + k, self.col - k))
            all_diags.append((self.row - k, self.col + k))
        if (d_row, d_col) in all_diags:
            return True
        return False

    def possible_moves(self, king=None):
        """
        :return: The possible moves
        """
        diag1 = []
        for k in range(1, 8):
            if (king is not None and (self.row - k, self.col - k) == (king.row, king.col)) or (self.row - k < 0) or (self.col - k < 0):
                break
            else:
                diag1.append((self.row - k, self.col - k)) 

        for k in range(1, 8):
            if (king is not None and (self.row + k, self.col + k) == (king.row, king.col))  or (self.row + k >= 8) or (self.col + k >= 8 ):
                break
            else:
                diag1.append((self.row + k, self.col + k))

        diag2 = []
        for k in range(1, 8):
            if (king is not None and (self.row - k, self.col + k) == (king.row, king.col))  or (self.row - k < 0) or (self.col + k >= 8):
                break
            else:
                diag2.append((self.row - k, self.col + k))

        for k in range(1, 8):
            if (king is not None and (self.row + k, self.col - k) == (king.row, king.col))  or (self.row + k >= 8) or (self.col - k < 0):
                break
            else:
                diag2.append((self.row + k, self.col - k))

        return list(set(diag1) | set(diag2))
    
    def check_move_validity(self, piece, row, col):
        if row == piece.row and col == piece.col:
            return False
        if not self.is_in_diags(row, col):
            return False
        piece_on_diag = self.is_in_diags(piece.row, piece.col) 
        if piece_on_diag and row > self.row and col > self.col and row > piece.row and col > self.col and piece.row > self.row and piece.col > self.col:
            return False 
        elif piece_on_diag and row < self.row and col < self.col and row < piece.row and col < self.col and piece.row < self.row and piece.col < self.col:
            return False 
        elif piece_on_diag and row > self.row and col < self.col and row > piece.row and col < self.col and piece.row > self.row and piece.col < self.col:
            return False 
        elif piece_on_diag and row < self.row and col > self.col and row < piece.row and col > self.col and piece.row < self.row and piece.col > self.col:
            return False 
        return True


class BlackBishop(Bishop):
    pass


class WhiteBishop(Bishop):
    pass

class Queen(Piece):
    def check_pos(self, d_row, d_col):
        return (d_row, d_col) in self.possible_moves()
    
    def is_in_diags(self, d_row, d_col):
        """
        Check if the desired position is in piece diagonals
        :return: True if it is the case
                 False otherwise
        """
        all_diags = []
        for k in range(0,8):
            all_diags.append((self.row + k, self.col + k))
            all_diags.append((self.row - k, self.col - k))
            all_diags.append((self.row + k, self.col - k))
            all_diags.append((self.row - k, self.col + k))
        if (d_row, d_col) in all_diags:
            return True
        return False

    def possible_moves(self, king=None):
        diags = Bishop.possible_moves(self, king)
        lines = Rook.possible_moves(self, king)
        return list(set(diags) | set(lines))
    
    def restricted_positions(self, king=None):
        lis = self.possible_moves(king)
        lis.append((self.row, self.col))
        return lis
    
    def check_move_validity(self, piece, row, col):
        return (Rook.check_move_validity(self, piece, row, col) or Bishop.check_move_validity(self, piece, row, col))




def comparison(list1, list2):
    if len(list1) != len(list2):
        return False
    for x in list1:
        if x not in list2:
            return False
    return True

if __name__ == '__main__':
    # print("King")
    # k = King(6,3, Piece.BLACK)
    # print(k.possible_moves())
    # print("Rook")
    # r = Rook(5,2, Piece.WHITE)
    # r_moves = r.possible_moves(k) 
    # print(r_moves)
    # print("Bishop")
    # b = Bishop(5,2, Piece.WHITE)
    # b_moves = b.possible_moves(k)
    # print(b_moves)
    # print("Queen")
    # q = Queen(5,2, Piece.WHITE)
    # q_moves = q.possible_moves(k)
    # print(q_moves)

    # print(comparison(r_moves + b_moves, q_moves))

    b = Bishop(3,3, Piece.WHITE)
    r = Rook(3,3,Piece.WHITE)
    q = Queen(3,3,Piece.WHITE)
    piece = King(5,5, Piece.WHITE)
    x,y = 6,6
    print(f"Queen : {q.check_move_validity(piece,x,y)}")
    print(f"Bishop : {b.check_move_validity(piece,x,y)}")
    print(f"Rook : {r.check_move_validity(piece,x,y)}")