import time
from collections import defaultdict
import random
from gmk import agent
from gmk import gmk_board
from gmk import gmk_types
from gmk.utils import print_board, print_move
import time 

def main():
    game = gmk_board.GameState.new_game(num_cols=15,num_rows=15)
    bot = agent.naive.RandomBot()
    print_board(game.board)
    move = bot.select_move(game)
    game = game.apply_move(move)
    flag_end = True
    while flag_end:
        time.sleep(0.1)
        
        print_board(game.board)
        move = bot.select_move(game)
        print(move.point,game.next_player)
        if game.is_over(move.point,game.next_player,return_neigh = True):
            flag_end = False
            winner = game.winner(game.next_player,move.point)
        game = game.apply_move(move)

    print_board(game.board)
    if winner is None:
        print("It's a draw.")
    else:
        print('Winner: ' + str(winner))


if __name__ == '__main__':
    main()