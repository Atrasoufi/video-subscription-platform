import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoStatusConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.group_name = 'video_updates'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to video updates.',
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    # Handler for group messages
    async def video_update(self, event):
        await self.send(text_data=json.dumps(event['data']))