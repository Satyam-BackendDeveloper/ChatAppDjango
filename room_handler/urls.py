from django.urls import path
from . import views

urlpatterns=[
    path('get_room/<str:room_name>/', views.GetRoom.as_view(), name='room'),
    path('create_rooms/', views.CreateRooms.as_view()),
    path('get_all_rooms/', views.GetAllRoomsAPI.as_view(), name='get_all_rooms'),
    path('chat_type_selection/', views.ChatTypeSelection.as_view()),
    path('view_all_users', views.ViewUsers.as_view(), name='all_users'),
    path('private_chat/<str:user_id>', views.PrivateChatView.as_view(), name='private_chat'),
    
]