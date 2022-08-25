from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from slotstreamer.models import Slot

from authentication.models import PublicToken

from django.core import serializers

from channels.db import database_sync_to_async

import json

class SlotStreamerConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def _get_slot_list(self, room_ident):
        return serializers.serialize('json', Slot.objects.all().filter(room_id=room_ident))

    @database_sync_to_async
    def _add_new_slot(self, slot):
        for deserialized_obj in serializers.deserialize('json', slot):
            deserialized_obj.save()

    @database_sync_to_async
    def _get_slot_by_pk(self, pk):
        slot = Slot.objects.get(pk=pk)
        return slot

    @database_sync_to_async
    def token_is_provided(self, token):
        try:
            provided_token = PublicToken.objects.get(public_token=token)
            return provided_token is not None
        except:
            pass

    async def websocket_connect(self, event):
        self.public_token = self.scope['url_route']['kwargs']['public_token']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = 'slotstreamer_%s' % self.room_id

        if await self.token_is_provided(self.public_token): 
            self.slot_list = await self._get_slot_list(self.room_id)

            await self.channel_layer.group_add(
                self.room_group_id,
                self.channel_name,
            )

            await self.accept()

            await self.channel_layer.group_send(
                self.room_group_id,
                {
                    'type': 'slotsinfo',
                    'slot_list': self.slot_list,
                },
            )
        

    async def slotsinfo(self, event):
        slot_list = event['slot_list']

        await self.send(text_data=json.dumps({
            'slot_list': slot_list,
        }))

    async def websocket_disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.scope['url_route']['kwargs']['public_token']
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        slot_list = text_data_json['slot_list']

        slot_list_json = json.dumps(slot_list)

        await self._add_new_slot(slot_list_json)

        self.slot_list = await self._get_slot_list(self.scope['url_route']['kwargs']['room_id'])

        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'slotsinfo',
                'slot_list': self.slot_list,
            },
        )

        