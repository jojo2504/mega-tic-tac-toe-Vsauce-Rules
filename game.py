from board import Board, MegaBoard

class Game:
    player_number = 2

    def __init__(self) -> None:
        self.game_turn = 0 # 0 for player1 - 1 for player2
        self.state = 0 # 0 for idle - 1 for playing
        self.megaboard = MegaBoard([Board() for _ in range(9)])
        self.case_turn_position = -1 # -1 for any, else 0 to 8

    def run(self):
        while True:
            if self.game_turn % 2 == 0:
                self.play(0)
            else:
                self.play(0)
            self.game_turn += 1

    def play(self, player):
        pass

    def print_board(self):
        print(self.megaboard)

        