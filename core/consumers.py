import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.connection_tracker import increment_clients, decrement_clients

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("logs_group", self.channel_name)
        await self.accept()
        increment_clients()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("logs_group", self.channel_name)
        decrement_clients()
    
    async def send_log(self, event):
        log = event['log']
        await self.send(text_data=json.dumps(log))