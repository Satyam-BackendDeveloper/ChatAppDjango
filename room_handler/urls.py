from django.urls import path
from . import views

urlpatterns=[
    path('get_room/<str:room_name>/', views.GetRoom.as_view()),
    path('create_rooms/', views.CreateRooms.as_view()),
    path('get_all_rooms/', views.GetAllRoomsAPI.as_view()),
]