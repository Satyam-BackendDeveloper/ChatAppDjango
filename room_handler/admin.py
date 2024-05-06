from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')
    search_fields = ('name', 'description')

admin.site.register(Room, RoomAdmin)