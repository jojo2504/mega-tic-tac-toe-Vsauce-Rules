class MegaBoard:
    def __init__(self, boards):
        self.megaboard = boards
        self.square = [
            self.megaboard[0].board[0] + self.megaboard[1].board[0] + self.megaboard[2].board[0],
            self.megaboard[0].board[1] + self.megaboard[1].board[1] + self.megaboard[2].board[1],
            self.megaboard[0].board[2] + self.megaboard[1].board[2] + self.megaboard[2].board[2],
            self.megaboard[3].board[0] + self.megaboard[4].board[0] + self.megaboard[5].board[0],
            self.megaboard[3].board[1] + self.megaboard[4].board[1] + self.megaboard[5].board[1],
            self.megaboard[3].board[2] + self.megaboard[4].board[2] + self.megaboard[5].board[2],
            self.megaboard[6].board[0] + self.megaboard[7].board[0] + self.megaboard[8].board[0],
            self.megaboard[6].board[1] + self.megaboard[7].board[1] + self.megaboard[8].board[1],
            self.megaboard[6].board[2] + self.megaboard[7].board[2] + self.megaboard[8].board[2]
        ]
        self.valid_boards = [True for _ in range(9)]
        self.valid_boards_remaining_cases = [9 for _ in range(9)]
        self.flagged_boards = [0 for _ in range(9)]

    def print_mega_board(self):
        for i in range(len(self.square)):
            if i%3 == 0:
                print()
            for j in range(len(self.square[i])):
                if j%3 == 0:
                    print(" ", end=' ')
                print(str(self.square[i][j]), end=' ')
            print()
        print()
    
    def edit(self, board_number, case_position, new_value):
        square_row = (board_number // 3) * 3 + case_position // 3
        square_col = (board_number % 3) * 3 + case_position % 3
        row = case_position // 3
        col = case_position % 3

        #print("played (edit):", board_number, case_position)
        
        try:     
            if self.megaboard[board_number].board[row][col] != 0 or self.valid_boards[board_number] == False:
                return False
            
            self.megaboard[board_number].board[row][col] = new_value
            self.square[square_row][square_col] = new_value
                 
            self.valid_boards_remaining_cases[board_number] -= 1
            if self.valid_boards_remaining_cases[board_number] == 0:
                self.valid_boards[board_number] = False

        except IndexError:
            return False
        
        return True
    
    def check_won_game(self, player):
        # Check rows
        for i in range(0, 9, 3):
            if self.flagged_boards[i] == self.flagged_boards[i+1] == self.flagged_boards[i+2] and self.flagged_boards[i] != 0:
                return player
        # Check columns
        for i in range(3):
            if self.flagged_boards[i] == self.flagged_boards[i+3] == self.flagged_boards[i+6] and self.flagged_boards[i] != 0:
                return player
        # Check diagonals
        if (self.flagged_boards[0] == self.flagged_boards[4] == self.flagged_boards[8]) and self.flagged_boards[0] != 0 or \
            (self.flagged_boards[2] == self.flagged_boards[4] == self.flagged_boards[6]) and self.flagged_boards[2] != 0:
            return player
        
        return None

class Board:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(self.cols)] for __ in range(self.cols)]

    def check_completed_board(self):
        # Check rows
        for i in range(3):
            if (self.board[i][0] == self.board[i][1] == self.board[i][2]) and self.board[i][0] != 0:
                print(f"{i}th rows")
                print(self.board[i][0], self.board[i][1], self.board[i][2])
                return True
        # Check columns
        for i in range(3):
            if (self.board[0][i] == self.board[1][i] == self.board[2][i]) and self.board[0][i] != 0:
                print(f"{i}th cols")
                print(self.board[0][i], self.board[1][i], self.board[2][i])
                return True
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and self.board[0][0] != 0 \
            or (self.board[0][2] == self.board[1][1] == self.board[2][0]) and self.board[0][2] != 0:
            print("some diags")
            return True
        return False

