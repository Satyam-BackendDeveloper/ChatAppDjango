import socket
import threading

host='127.0.0.1'
port=5557

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host,port))
server.listen()

nicknames=list()

connections=dict()

def broadcast(message, client):
    for websocket,nickname in connections.items():
        if websocket is not client :
            websocket.send(message)
def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message, client)
        except:
            nickname=connections[client]
            del connections[client]

            broadcast(f"{nickname} left the chat room!".encode('ascii'), client)
            nicknames.remove(nickname)
            client.close()
            break

def receive():
    while True:
        client, address = server.accept()
    
        client.send(f"NICK".encode('ascii'))
        nickname=client.recv(1024).decode('ascii')

        connections[client]=nickname
        nicknames.append(nickname)
        
        print(f"{address} connected to server with nickname {nickname}")
        client.send(f"connected to server".encode('ascii'))

        broadcast(f"{nickname} joined the chatroom!".encode('ascii'), client)

        thread=threading.Thread(target=handle, args=(client,))
        thread.start()

print(f"server listening at {host}:{port}...")
receive()

