import socket
from _thread import start_new_thread
import pickle

HOST = '127.0.0.1'
PORT = 60065
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen()
print('listen')
players = {}
cannons = {}
ID = 0


def threaded_clients(conn, id):
    global players
    try:
        while True:
            data = pickle.loads(conn.recv(1024))
            if not data:
                break

            if data[0] != 'hello':
                players[id]['x'], players[id]['y'], players[id]['score'] = data[0]
                cannons[id] = data[1]
                data = [players, cannons]
            else:
                players[id]['color'] = data[1]
                players[id]['x'], players[id]['y'] = data[2]
                data = [players, id]

            conn.send(pickle.dumps(data))

    except Exception as e:
        print(e)
        del players[id]
        del cannons[id]
        conn.close()


while True:
    host, addr = server_socket.accept()
    players[ID] = {'x': 0, 'y': 0, 'color': 0, 'id': ID, 'score': 0}
    start_new_thread(threaded_clients, (host, ID))

    ID += 1
