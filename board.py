class MegaBoard:
    def __init__(self, boards):
        self.megaboard = [board for board in boards]

    def print_mega_board(self):
        for board in self.megaboard:
            print(board)
            print("--------------")

class Board:
    def __init__(self, rows=3, cols=3) -> None:
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(self.cols)] for __ in range(self.cols)]
        self.noob = "noob"
    
    def check_win(self):
        pass

    def color_case(self):
        pass

    def __str__(self) -> str:
        return str(self.board)


