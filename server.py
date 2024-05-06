import socket
from _thread import *
import pickle
from game import Game
from config import serverIP

server = serverIP
port = 5555

print(server)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
    print("s binded")
except socket.error as e:
    str(e)

s.listen()
print("Server started, waiting for a connection")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameID):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameID in games:
                game = games[gameID]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(p, data)
                    
                    reply = game
                    conn.sendall(pickle.dumps(reply))          
            else:
                break
        except:
            break
        
    print("Lost connection")
    print("Closing game", gameID)
    try:
        del games[gameID]
    except:
        pass

    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("-"*20)
    print("connected to:", addr)

    idCount += 1
    p = 0
    gamesID = (idCount-1)//2
    print(idCount)

    if idCount % 2 == 1:
        games[gamesID] = Game(gamesID)
        print(f"creating a new game... n°{gamesID}")
    else:
        games[gamesID].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gamesID))