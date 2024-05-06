from board import Board, MegaBoard
import ast

class Game:
    def __init__(self, id) -> None:
        self.id = id
        self.ready = False
        self.game_turn = 0
        self.player = 1 # 1 for player1 | -1 for player2
        self.megaboard = MegaBoard([Board() for _ in range(9)])
        self.board_turn_position = -1 # -1 for any, else 0 to 8
        self.bonus_turn = False
        self.winner = None

        print("game init")
    
    def connected(self):
        return self.ready

    def reset(self):
        self.game_turn += 1

    def bothWent(self):
        return self.p1Went and self.p2Went

    def game_update(self, board_number, case_position, player):
        if self.megaboard.edit(board_number, case_position, player):
            self.megaboard.print_mega_board()
            if self.megaboard.megaboard[self.board_turn_position].check_completed_board():
                print(f"Board {self.board_turn_position} has been completed")
                self.megaboard.valid_boards[self.board_turn_position] = False
                self.megaboard.flagged_boards[self.board_turn_position] = self.player
                self.winner = self.megaboard.check_won_game(self.player)
                self.bonus_turn = True

            print("flagged_boards:", self.board_turn_position, self.megaboard.flagged_boards)
            self.player *= -1

            if self.megaboard.valid_boards[case_position]:
                self.board_turn_position = case_position
            else:
                self.board_turn_position = -1

            return True
        
        return False

    def getPosOnBoard(self, move):
        cell_size = 100
        board_size = 300
        
        mouse_pos_board = (move[0] // board_size, move[1] // board_size)
        pos_board = mouse_pos_board[0]+mouse_pos_board[1]*3

        mouse_pos_cell_relative_to_board = ((move[0] % board_size) // cell_size, (move[1] % board_size) // cell_size)
        pos_cell = mouse_pos_cell_relative_to_board[0]+mouse_pos_cell_relative_to_board[1]*3

        return pos_board, pos_cell
    
    def play(self, player, move):
        move = ast.literal_eval(move)
        pos_board, pos_cell = self.getPosOnBoard(move)
        
        print("played:", pos_board, pos_cell, player)
        if player == 0:
            if self.board_turn_position != -1 and pos_board != self.board_turn_position:
                print("Invalid Board Position")
            else:
                if self.game_update(pos_board, pos_cell, self.player):
                    print(f"player {player} played")
                    print("-"*20)
        else:
            if self.board_turn_position != -1 and pos_board != self.board_turn_position:
                print("Invalid Board Position")
            else:
                if self.game_update(pos_board, pos_cell, self.player):
                    print(f"player {player} played")
      
