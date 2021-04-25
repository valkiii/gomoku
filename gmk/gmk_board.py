import copy
from collections import defaultdict
from gmk.gmk_types import Player, Point

__all__ = [
    'Board',
    'GameState',
    'Move',
]

class IllegalMoveError(Exception):
    pass

class Board():
    def __init__(self,num_rows,num_cols):
        self._grid = {}
        self.num_rows = num_rows
        self.num_cols = num_cols

    def place(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        self._grid[point] = player

    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get(self, point):
        """Return the content of a point on the board.
        Returns None if the point is empty, or a Player if there is a
        stone on that point.
        """
        return self._grid.get(point)


class Move:
    def __init__(self, point):
        self.point = point
    @classmethod
    def play(cls, point):
        return Move(point=point)

class GameState():
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    def apply_move(self, move):
        """Return the new GameState after applying the move."""
        next_board = copy.deepcopy(self.board)
        next_board.place(self.next_player, move.point)
        return GameState(next_board, self.next_player.other, move)

    @classmethod
    def new_game(cls,num_rows,num_cols):
        board = Board(num_rows,num_cols)
        return GameState(board, Player.x, None)

    def is_valid_move(self, move, player):
        return self.board.get(move.point) is None

    def legal_moves(self, point,player):
        moves = []
        for row in self.board.num_rows:
            for col in self.board.num_cols:
                move = Move(Point(row, col))
                if self.is_valid_move(move.point,player):
                    moves.append(move)
        return moves

    def is_over(self,point, player, return_neigh=False):
        if self._has_5_in_a_row(player, point, return_neigh=return_neigh)[0]:
            return True
        if all(self.board.get(Point(row, col)) is not None
               for row in range(1,self.board.num_rows+1)
               for col in range(1,self.board.num_cols+1)):
            return True
        return False

    def _has_5_in_a_row(self, player, point, return_neigh=False):
        
        neig_dict = {
            'horizontal':0,
            'vertical':0,
            'obl_l':0,
            'obl_r':0
        }

        # Vertical
        row, col = point.row - 1, point.col
        while row >= 1:
            if self.board.get(Point(col, row)) == player:
                neig_dict['vertical'] += 1
                row -= 1
            else:
                break
                
        row, col = point.row + 1, point.col
        while row <= self.board.num_rows:
            if self.board.get(Point(col, row)) == player:
                neig_dict['vertical'] += 1
                row += 1
            else:
                break
        
        # Horizontal
        row, col = point.row, point.col -1
        while col >= 1:
            if self.board.get(Point(col, row)) == player:
                neig_dict['horizontal'] += 1
                col -= 1
            else:
                break
                
        row, col = point.row, point.col +1
        while col <= self.board.num_rows:
            if self.board.get(Point(col, row)) == player:
                neig_dict['horizontal'] += 1
                col += 1
            else:
                break
        
        
        # Oblique Left
        row, col = point.row +1, point.col -1
        while row <= self.board.num_rows and col >= 1:
            if self.board.get(Point(col, row)) == player:
                neig_dict['obl_l'] += 1
                col -= 1
                row += 1
            else:
                break
                
        row, col = point.row -1, point.col +1
        while col <= self.board.num_cols and row >= 1:
            if self.board.get(Point(col, row)) == player:
                neig_dict['obl_l'] += 1
                col += 1
                row -= 1
            else:
                break
                
        # Oblique Right
        row, col = point.row -1, point.col -1
        while row >= 1 and col >= 1:
            if self.board.get(Point(col, row)) == player:
                neig_dict['obl_r'] += 1
                col -= 1
                row -= 1
            else:
                break
                
        row, col = point.row +1, point.col +1
        while col <= self.board.num_cols and row <= self.board.num_rows:
            if self.board.get(Point(col, row)) == player:
                neig_dict['obl_r'] += 1
                col += 1
                row += 1
            else:
                break
        if return_neigh:
            print(neig_dict)
        if max(neig_dict.values()) >= 4:
            return (True,neig_dict)
        return (False,None)

    def winner(self,player,point):
        if self._has_5_in_a_row(player,point)[0]:
            return player
        return None