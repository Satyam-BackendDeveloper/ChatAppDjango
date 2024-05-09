from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from django.core.management import call_command
from .models import Room

# @receiver(post_save, sender=Room)
def create_websocket_connections(instance,**kwargs):
    print("inside signals...")
    try:
        host='127.0.0.1'
        port=instance.port
        room_name=instance.name
        call_command('start_websocket_server', port=int(port), room_name=room_name)
    except Exception as e :
        print({"status":False, "data":"Error occured in creating websocket server for this room", "error":e})    