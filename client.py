import pygame
from network import Network

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

def redrawBoard(color, width, height, game):
    win.fill(WHITE)

    left = (game.board_turn_position % 3) * 300
    top = (game.board_turn_position // 3) * 300
    if game.board_turn_position != -1:
        pygame.draw.rect(win, color, pygame.Rect(left, top, width, height))
    
    for i in range(len(game.megaboard.square)):
        for j in range(len(game.megaboard.square)):
            if game.megaboard.square[i][j] == 1:
                pygame.draw.circle(win, BLACK, (j*100+cell_size//2, i*100+cell_size//2), 50, 10)
            elif game.megaboard.square[i][j] == -1:
                pygame.draw.circle(win, RED, (j*100+cell_size//2, i*100+cell_size//2), 50, 10)

def drawMenu():
    win.fill(WHITE)
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Waiting for another player to join the game...", 1, BLACK)
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
    return True

def drawWinner(player):
    win.fill(WHITE)
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render(f"player {player} won !", 1, BLACK)
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
    return True

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    pygame.display.set_caption(f"Client {player}")
    print("You are player", player)

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
            redrawBoard(GREY, 300, 300, game)
            for i in range(10):
                if i%3==0:
                    pygame.draw.line(win, grid_color, (i * cell_size, 0), (i * cell_size, height), width=5) # Vertical lines
                    pygame.draw.line(win, grid_color, (0, i * cell_size), (height, i * cell_size), width=5) # Horizontal lines
                else:
                    pygame.draw.line(win, grid_color, (i * cell_size, 0), (i * cell_size, height))
                    pygame.draw.line(win, grid_color, (0, i * cell_size), (height, i * cell_size))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

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
        else:
            if game.winner == 1:  
                run = drawWinner(0)
            else:
                run = drawWinner(1)

        pygame.display.flip()

main()