import socket
import threading

host='127.0.0.1'
port=5557

sever=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sever.connect((host,port))

nickname=input("Enter your nickname \t")

def receive(server):
    while True:
        try:
            message=server.recv(1024).decode('ascii')
            if message == 'NICK':
                server.send(nickname.encode('ascii'))
            else:
                print(f"received message from server: {message}")

        except Exception as e:
            print(f"server might be closed... {e}")
            server.close()
            break

def send_message(server):
    while True:
        try:
            message=input("Enter the message to be send to server \t")
            server.send(f"{nickname}: {message}".encode('ascii'))
        except Exception as e:
            print(f"server might be closed... {e}")
            server.close()
            break

receive_thread=threading.Thread(target=receive, args=(sever,))
send_thread=threading.Thread(target=send_message, args=(sever,))

receive_thread.start()
send_thread.start()
