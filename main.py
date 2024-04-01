import client  
import server
from game import Game

def main(*args, **kwargs):
    game = Game()
    game.megaboard.megaboard[0].board[0][0] = 1
    game.megaboard.megaboard[4].board[0][0] = 1
    print(game.megaboard.print_mega_board())

if __name__ == '__main__':
    main()