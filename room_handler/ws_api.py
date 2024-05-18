import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name=f"chat_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, message):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        ) 
    
    async def receive(self, text_data=None):
        data=json.loads(text_data)
        username=data.get('username')
        message=data.get('message')
        room_name=data.get('room_name')
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "username":username,
                "message":message,
                "room_name":room_name,
                "type":"websocket.message"
            }
        )
    
    async def websocket_message(self, event):
        username=event.get('username')
        message=event.get('message')
        room_name=event.get('room_name')
        
        await self.send(json.dumps(
            {
                "username":username,
                "message":message,
                "room_name":room_name
            } 
        ))

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id=int(self.scope['url_route']['kwargs']['sender'])
        self.receiver_id=int(self.scope['url_route']['kwargs']['receiver'])
        self.group_id=None
        if self.sender_id > self.receiver_id:
            self.group_id=self.sender_id - self.receiver_id
        else:
            self.group_id=self.receiver_id - self.sender_id

        self.room_group_name=f"chat_{self.group_id}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, message):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        ) 
    
    async def receive(self, text_data=None):
        data=json.loads(text_data)
        username=data.get('username')
        message=data.get('message')
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "username":username,
                "message":message,
                "type":"websocket.message"
            }
        )
    
    async def websocket_message(self, event):
        username=event.get('username')
        message=event.get('message')
        
        await self.send(json.dumps(
            {
                "username":username,
                "message":message
            } 
        ))