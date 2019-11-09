import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Thread


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        reciever = self.scope['url_route']['kwargs']['username']
        self.sender = self.scope['user']
        thread = await self.get_thread(self.sender, reciever)
        self.room_group_name = f'chat_{thread.id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def websocket_receive(self, event):
        payload = json.loads(event['text'])
        message = payload['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(json.dumps({
            'message': message,
            'sender': self.sender.username
        }))

    @database_sync_to_async
    def get_thread(self, sender, reciever):
        return Thread.objects.get_thread_or_create(sender, reciever)
