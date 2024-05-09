from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
import os
import socket 
import threading


if hasattr(settings, 'PROJECT_ROOT'):
    ROOT = settings.PROJECT_ROOT
else:
    raise ImproperlyConfigured('Set "PROJECT_ROOT" as project root in settings.py')
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--host',       help='host of the websocket server', default='127.0.0.1')
        parser.add_argument('--port',       help='port of the websocket server', type=int, default=5555)
        parser.add_argument('--room_name',  help='chat room in which this websocket server is running', default='Room1')

    manage_py = os.path.join(ROOT, 'manage.py')

    def handle( self, 
                host,
                port,
                room_name,
                **kwargs):
        server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen()

        print(f"server is listening at {host}:{port} for room {room_name}")

        self.receive(server)


    connections=dict()

    def broadcast(self, message, connected_client):
        for other_client, user_name in self.connections.items():
            if connected_client is not other_client:
                other_client.send(message)

    def messages_from_clients(self,client):
        while True:
            try:
                message=client.recv(1024)
                self.broadcast(message, client)
            except Exception as e:
                print(f"connection with client closed due to: {e}")
                user_name=self.connections[client]
                del self.connections[client]

                self.broadcast(f"{user_name} left the chat room!", client)
                client.close()
                break
        
    
    def receive(self, server):
        while True:
            try:
                client, address= server.accept()
                client.send(f"user_name".encode('ascii'))
                
                user_name=client.recv(1024).decode('ascii')
                print(f"{address} connected with username {user_name}")
                client.send(f"connected to server".encode('ascii'))
            
                self.connections[client] = user_name

                self.broadcast(f"{user_name} joined the chat".encode('ascii'), client)

                thread=threading.Thread(target=self.messages_from_clients, args=(client,))
                thread.start()
                
            except Exception as e:
                user_name=self.connections[client]
                print(f"closing the connection with username {user_name} due to {e}")
                self.broadcast(f"{user_name} left the chat room!", client)
                del self.connections[client]
                client.close()
    

