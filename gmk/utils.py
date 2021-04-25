from gmk import gmk_types

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' . ',
    gmk_types.Player.x: '\33[41m x \33[0m',
    gmk_types.Player.o: '\33[43m o \33[0m'
}

def print_move(player,move):
    move_str = '%s%d' % (COLS[move.point.col -1 ], move.point.row)
    print('%s %s' %(player,move_str))

def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gmk_types.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' % (bump, row, ''.join(line)))
    print('    ' + '  '.join(COLS[:board.num_cols]))

def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gmk_types.Point(row=row, col=col)