from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache
from channels.layers import get_channel_layer

class UserStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        channel_layer = get_channel_layer()
        await channel_layer.group_add(
            'user-status',
            self.channel_name
        )

    async def disconnect(self, code):
        channel_layer = get_channel_layer()
        await channel_layer.group_discard(
            'user-status',
            self.channel_name
        )

    async def receive(self, text_data):
        # Update the cache when a message is received
        await self.update_cache()

    async def update_cache(self):
        # Get the user's status from the database
        users = await database_sync_to_async(Users.objects.all)()
        user_statuses = [(user.id, user.status) for user in users]

        # Update the cache
        await database_sync_to_async(cache.set)('user_statuses', user_statuses)

    async def user_status_changed(self, event):
        # Handle the message sent by the signal handler
        await self.update_cache()