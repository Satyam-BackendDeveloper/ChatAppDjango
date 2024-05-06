from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class Signup(APIView):
    def post(self, request):
        request_data=request.data
        username = request_data.get("username",None)
        password1 = request_data.get("password",None)
        password2 = request_data.get("password",None)

        if password1 != password2:
            return Response({"status":False, "message":"Password does not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            User.objects.get(username=username)
            return Response({"status":False, "message":"User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            print(f"password1: {password1}")
            user = User.objects.create_user(username=username, password=password1)
            return Response({"status":True, "message":f"User {user.username} created successfully"}, status=status.HTTP_200_OK)

class Login(APIView):
    def post(self, request):
        request_data=request.data
        username = request_data.get("username",None)
        password = request_data.get("password",None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({"status":True, "message":"Successfully logged in"}, status=status.HTTP_200_OK)
            else:
                return Response({"status":False, "message":"User is not active. Contact administrator!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":False, "message":"Username and Password Doesn't match!"}, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def get(self, request):
        try:
            logout(request)    
            return Response({"status":True, "message":"Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":False, "message":f"Unexpected exception occured in logging out: {e}"}, status=status.HTTP_404_NOT_FOUND)

        