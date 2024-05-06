from rest_framework.views import APIView
from .models import Room
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer

class GetRoom(APIView):
    def get(self, request, room_name):
        room_queryset=Room.objects.none()
        response=None
        
        try:
            room_queryset=Room.objects.get(name=room_name)
            response=[room_queryset.name]
        except Room.DoesNotExist:
            return Response({"status":False, "data":response, "error":"No room with given name"}, status=status.HTTP_404_NOT_FOUND) 

        return Response({"status":True, "data":response}, status=status.HTTP_200_OK)
    
class GetAllRoomsAPI(APIView):
    def get(self, request):
        room_queryset=Room.objects.none()
        response=None
        
        room_queryset=Room.objects.all()
        if room_queryset:
            response=room_queryset.values_list('name',flat=True)
            return Response({"status":True, "data":response}, status=status.HTTP_200_OK)
        else:
            return Response({"status":False, "data":"No Rooms Found"}, status=status.HTTP_404_NOT_FOUND)


class CreateRooms(APIView):
    def post(self, request):
        request_data=request.data
        serializer=RoomSerializer(data=request_data)
        
        if serializer.is_valid():
            room_name=request_data.get('name',False)
            description=request_data.get('description',False)
            serializer.save()
            return Response({"status":True, "data": f"Chat Room with name {room_name} created successfully"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"status":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)