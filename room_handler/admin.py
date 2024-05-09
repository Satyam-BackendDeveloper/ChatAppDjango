from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'description')
    list_filter = ('room_name', 'description')
    search_fields = ('room_name', 'description')

admin.site.register(Room, RoomAdmin)