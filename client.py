import pygame
import game
from network import Network
from typing import Tuple, NewType

pygame.font.init()

width = 900
height = 900
win = pygame.display.set_mode((width, height))

background_color = (255, 255, 255)  # White
win.fill(background_color)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREY  = (128, 128, 128)

grid_color = BLACK

cell_size = height // 9
board_size = height // 3

Surface = NewType("Surface", pygame.Surface)
Game = NewType("Game", game.Game)

class Button:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                print("Trying to connect to the server")
                return True
        return False
    
    def draw(self, win: Surface):
        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(win, self.color, self.rect, 2)

def offlineMenuBoard(button):
    win.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if button.handle_event(event):
            return False
        
    button.draw(win)

    pygame.display.flip()

    return True

def drawBoard(color: Tuple[int, int, int], game: Game, player: int, n: Network) -> bool:
    win.fill(WHITE)

    left = (game.board_turn_position % 3) * 300
    top = (game.board_turn_position // 3) * 300
    if game.board_turn_position != -1:
        pygame.draw.rect(win, color, pygame.Rect(left, top, board_size, board_size))
    
    for i in range(len(game.megaboard.square)):
        for j in range(len(game.megaboard.square)):
            if game.megaboard.square[i][j] == 1:
                pygame.draw.circle(win, BLACK, (j*100+cell_size//2, i*100+cell_size//2), 50, 10)
            elif game.megaboard.square[i][j] == -1:
                pygame.draw.circle(win, RED, (j*100+cell_size//2, i*100+cell_size//2), 50, 10)

    for i in range(10):
        if i%3==0:
            pygame.draw.line(win, grid_color, (i * cell_size, 0), (i * cell_size, height), width=5) # Vertical lines
            pygame.draw.line(win, grid_color, (0, i * cell_size), (height, i * cell_size), width=5) # Horizontal lines
        else:
            pygame.draw.line(win, grid_color, (i * cell_size, 0), (i * cell_size, height))
            pygame.draw.line(win, grid_color, (0, i * cell_size), (height, i * cell_size))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = str(pygame.mouse.get_pos())
            if player == 0:
                if game.player == -1:
                    print("its not your turn")
                    print(game.megaboard.square)
                else:
                    n.send(pos)
            else:
                if game.player == 1:
                    print("its not your turn")
                else:
                    n.send(pos)

    return True

def drawMenu():
    win.fill(WHITE)
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Waiting for another player to join the game...", 1, BLACK)
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
    return True

def drawWinner(player, n: Network) -> bool:
    win.fill(WHITE)
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render(f"Player {player} won !", 1, BLACK)
    text2 = font.render(f"Left click to play again", 1, BLACK)
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2  + 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            n.send("reset")

    return True

def main():
    run = True
    clock = pygame.time.Clock()

    connect_button = Button(width//2, height//2, 100, 50, "noob")
    while True:
        if not offlineMenuBoard(connect_button):
            try:
                n = Network()
                player = int(n.getP())
                pygame.display.set_caption(f"Client {player}")
                print("You are player", player)
                break
            except TypeError as e:
                print(e)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False 
            print("Couldnt connect")

        if not game.connected():
            run = drawMenu()

        elif game.winner is None:
            run = drawBoard(GREY, game, player, n)

        else:
            if game.winner == 1:  
                run = drawWinner(0)
            else:
                run = drawWinner(1)

        pygame.display.flip()

main()