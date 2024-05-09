from rest_framework.views import APIView
from .models import Room
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer
from django.core.management import call_command
from django.db import transaction
import threading
from threading import Thread
from django.contrib.auth.models import User

class GetRoom(APIView):
    def get(self, request, room_name):
        room_queryset=Room.objects.none()
        response=None
        
        try:
            room_queryset=Room.objects.get(name=room_name)
            response={
                "name":room_queryset.name,
                "port":room_queryset.port
                }
        except Room.DoesNotExist:
            return Response({"status":False, "data":response, "error":"No room with given name"}, status=status.HTTP_404_NOT_FOUND) 

        return Response({"status":True, "data":response}, status=status.HTTP_200_OK)
    
class GetAllRoomsAPI(APIView):
    def get(self, request):
        room_queryset=Room.objects.none()
        response=None
        
        room_queryset=Room.objects.all()
        if room_queryset:
            response=room_queryset.values('name','port')
            return Response({"status":True, "data":response}, status=status.HTTP_200_OK)
        else:
            return Response({"status":False, "data":"No Rooms Found"}, status=status.HTTP_404_NOT_FOUND)


class CreateRooms(APIView):
    # def call_management_command_in_thread(self, port, room_name):
    #     call_command('start_websocket_connections', port=int(port), room_name=room_name)
    
    def post(self, request):
        request_data=request.data
        serializer=RoomSerializer(data=request_data)
        if serializer.is_valid():
            room_name=serializer.validated_data.get('room_name',False)
            description=serializer.validated_data.get('description',False)
            port=serializer.validated_data.get('port',None)
            serializer.save()

            return Response({"status":True, "data": {"port":port, "room_name":room_name, "description":description}, "message":"Chat room created successfully"}, status=status.HTTP_201_CREATED)

        return Response({"status":False, "error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class WebSocketThread(Thread):
    def __init__(self, port, room_name, host):
        super().__init__()
        self.port = port
        self.room_name = room_name
        self.host = host
        self.error = None

    def run(self):
        try:
            call_command('start_websocket_server', port=self.port, room_name=self.room_name, host=self.host)
        except Exception as e:
            print(f"error occured in creating server: {e}")
            self.error = e
    def join(self):
        threading.Thread.join(self)
        if self.error:
            raise self.error

class CreateWebsocketConnections(APIView):
    def post(self, request):
        request_data=request.data
        port=request_data.get('port',None)
        room_name=request_data.get('room_name',None)
        host=request_data.get('host',None)
        
        websocket_thread = WebSocketThread(port=port, room_name=room_name, host=host)
        websocket_thread.start()

        # try:
        #     websocket_thread.join()
        # except Exception as e:
        #     return Response({"status": False, "data": "Error occurred in creating websocket server for this room", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"status":True, "data": f"Websocket server created successfully"}, status=status.HTTP_201_CREATED)

class JoinRoom(APIView):
    def post(self, request):
        request_data=request.data
        room_name=request_data.get('room_name',None)
        user_name=request_data.get('user_name',None)

        try:
            Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return Response({"status":False, "data":f"Room {room_name} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"status":False, "data":f"User {user_name} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"status":True, "data": f"User {user_name} joined the room {room_name}"}, status=status.HTTP_200_OK)