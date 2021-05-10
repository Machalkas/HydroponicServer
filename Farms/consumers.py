import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from django.core.serializers import serialize

from .models import Farm, Statistic

class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        t=self.scope['url_route']['kwargs']['farm_token']
        self.farm = await self.get_farm(t)
        if self.farm:
            self.farm_token=self.farm.token
            await self.channel_layer.group_add(self.farm_token, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.farm_token, self.channel_name)
    
    async def receive(self, text_data):
        is_broadcast=False
        data=json.loads(text_data)
        action=data["action"]
        print(action)
        if action=='get_statistic':
            message = await self.get_statistic(self.farm)
            message={'statistic':json.loads(message)}
        elif action=='get_latest_statistic':
            message = await self.get_statistic(self.farm, True)
            message={'statistic':json.loads(message)}   
        elif action=='save_statistic':
            options=data["options"]
            message = await self.save_statistic(self.farm, options)
            if not message:
                message={'error':'fail to save statistic'}
            else:
                message={'sensors':options}
            is_broadcast=True
        else:
            message={'error':'fail to process request'}
        if is_broadcast:
            await self.channel_layer.group_send(self.farm_token, {'type':'broadcast','message':message})
        else:
            await self.send(text_data=json.dumps(message))


    async def broadcast(self, data):
        message=data['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_farm(self, k):
        try:
            return Farm.objects.get(token=k)
        except:
            return None

    @database_sync_to_async
    def get_statistic(self, farm, only_last=False, from_date=None, to_date=None):
        try:
            if only_last:
                st=Statistic.objects.latest("record_date")
                st=(st,)
            else:
                st=Statistic.objects.filter(farm=farm.pk)
                if from_date!=None:
                    st=st.filter(record_date>=from_date)
                if to_date!=None:
                    st=st.filter(record_date<=to_date)
            st=serialize('json', st)
            return st
        except:
            return None

    @database_sync_to_async
    def save_statistic(self, farm, sensors):
        try:
            sensors["farm_id"]=self.farm.pk
            st=Statistic.objects.create(**sensors)
            st.save()
            return True
        except:
            return False
