import json
import redis
from datetime import datetime as dt

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.core.serializers import serialize

from .models import Farm, Statistic

r = redis.Redis(host='localhost', port=6379, db=1)
r.flushdb()

class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        fid=self.scope['url_route']['kwargs']['farm_id']
        self.farm, self.farm_user = await self.get_farm(fid)
        self.farm_id=str(self.farm.id)
        self.is_farm=self.scope['is_farm']
        if self.is_farm:
            self.farm_client=self.scope["farm"]
        else:
            self.user=self.scope["user"]
        if self.is_farm :
            if self.farm_client==self.farm:
                await self.channel_layer.group_send(self.farm_id, {'type':'broadcast','message':{'farm_online':True}})
                await self.channel_layer.group_add(self.farm_id, self.channel_name)
                await self.accept()
                r.hset('farms', self.farm_id, 'true')
            else:
                await self.close()
        else:
            if self.user==self.farm_user:
                await self.channel_layer.group_add(self.farm_id, self.channel_name)
                await self.accept()
                await self.send(text_data=json.dumps({'farm_online':isOnline(self.farm_id)}))
            else:
                await self.close()



    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.farm_id, self.channel_name)
        if self.is_farm:
            r.hset('farms', self.farm_id, 'false')
            await self.channel_layer.group_send(self.farm_id, {'type':'broadcast','message':{'farm_online':False}})
    
    async def receive(self, text_data):
        is_broadcast=False
        data=json.loads(text_data)
        action=data["action"]
        print(action)
        if action=='get_statistic':
            options=data["options"]
            message = await self.get_statistic(self.farm, only_last=False, from_date=options.get("from_date",None), to_date=options.get("to_date",None))
            message={'statistic':json.loads(message)}
        elif action=='get_latest_statistic':
            message = await self.get_statistic(self.farm, only_last=True)
            message={'statistic':json.loads(message)}   
        elif action=='save_statistic':
            if not self.is_farm:
                message={'error':'you don`t have rights to run this action'}
            else:
                options=data["options"]
                message = await self.save_statistic(self.farm, options)
                if not message:
                    message={'error':'fail to save statistic'}
                else:
                    message={'sensors':options}
                is_broadcast=True
        elif action=='is_online':
            message={'farm_online':isOnline(self.farm_id)}
        else:
            message={'error':'fail to process request'}
        if is_broadcast:
            await self.channel_layer.group_send(self.farm_id, {'type':'broadcast','message':message})
        else:
            await self.send(text_data=json.dumps(message))



    async def broadcast(self, data):
        message=data['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_farm(self, id):
        try:
            f=Farm.objects.get(pk=id)
            return f, f.user
        except:
            return None

    @database_sync_to_async
    def get_statistic(self, farm, only_last=False, from_date=None, to_date=None):
        try:
            if only_last:
                st=Statistic.objects.latest("id")
                st=(st,)
            else:
                st=Statistic.objects.filter(farm=farm.pk)
                if from_date!=None:
                    from_date=dt.strptime(from_date, "%Y-%m-%dT%H:%M:%S")
                    st=st.filter(record_date__gte=from_date)#меньше или равно
                if to_date!=None:
                    to_date=dt.strptime(to_date, "%Y-%m-%dT%H:%M:%S")
                    st=st.filter(record_date__lte=to_date)#больше или равно
            st=serialize('json', st)
            return st
        except ZeroDivisionError:
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



def isOnline(fid:str):
    status=r.hget('farms',fid)
    if status!=None and status.decode()=='true':
        return True
    return False