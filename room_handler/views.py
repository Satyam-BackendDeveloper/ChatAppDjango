from rest_framework.views import APIView
from .models import Room
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class GetRoom(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, room_name):
        room_queryset=Room.objects.none()
        response=None
        
        try:
            room_queryset=Room.objects.get(room_name=room_name)
        except Room.DoesNotExist:
            return Response({"status":False, "data":response, "error":"No room with given name"}, status=status.HTTP_404_NOT_FOUND) 

        return render(request, 'room.html', {'room':room_queryset})

class GetAllRoomsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        room_queryset=Room.objects.all()
        return render(request,'rooms.html', {'rooms':room_queryset})


class CreateRooms(APIView):
    permission_classes = [IsAuthenticated]
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

class ChatTypeSelection(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return render(request,'chat_type_selection.html', {})
    
class PrivateChatView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        receiver=User.objects.get(id=user_id)
        return render(request,'private_chat.html', {"receiver":receiver})

class ViewUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users=User.objects.exclude(id=request.user.id)
        return render(request,'all_users.html', {"users":users})
