import json
import redis
from datetime import date, datetime as dt

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.core.serializers import serialize

from .models import Farm, Statistic, Timetable

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
            status=r.hget('farms', self.farm_id)
            if self.farm_client==self.farm and (status==None or status.decode()=='false'):
                await self.channel_layer.group_send(self.farm_id, {'type':'broadcast','message':{'is_online':True}})
                await self.channel_layer.group_add(self.farm_id, self.channel_name)
                await self.accept()
                r.hset('farms', self.farm_id, 'true')
                self.del_from_reddis=True
            else:
                self.del_from_reddis=False
                await self.close()
        else:
            if self.user==self.farm_user:
                await self.channel_layer.group_add(self.farm_id, self.channel_name)
                await self.accept()
                await self.send(text_data=json.dumps({'is_online':isOnline(self.farm_id)}))
            else:
                await self.close()



    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.farm_id, self.channel_name)
        if self.is_farm:
            if self.del_from_reddis:
                r.hset('farms', self.farm_id, 'false')
            await self.channel_layer.group_send(self.farm_id, {'type':'broadcast','message':{'is_online':False}})
    
    async def receive(self, text_data):
        is_broadcast=False
        # print(text_data)
        try:
            data=json.loads(text_data)
            action=data["action"]
        except:
            await self.send(text_data=json.dumps({"error":"data format is not correct"}))
            return
        print(action)
        if action=='get_statistic':
            try:
                options=data["options"]
            except:
                options={}
            message = await self.get_statistic(self.farm, only_last=False, from_date=options.get("from_date",None), to_date=options.get("to_date",None))
            message={'statistic':json.loads(message)}
        elif action=='get_latest_statistic':
            message = await self.get_statistic(self.farm, only_last=True)
            message={'statistic':json.loads(message)}   
        elif action=='save_statistic':
            if not self.is_farm:
                message={'error':'not enough rights to perform this action'}
            else:
                options=data["options"]
                message = await self.save_statistic(self.farm, options)
                if not message:
                    message={'error':'failed to save statistics'}
                else:
                    message={'statistic':options}
                    is_broadcast=True
        elif action=='sensors_data':
            if not self.is_farm:
                message={'error':'not enough rights to perform this action'}
            else:
                message={'sensors_data':data["options"]}
                is_broadcast=True
        elif action=='is_online':
            message={'is_online':isOnline(self.farm_id)}
        elif action=='farm_name':
            message={'farm_name':self.farm.name}
        elif action=='get_timetable':
            message=await self.get_timetable(self.farm)
            message={'timetable':json.loads(message)}
        elif action=='save_timetable':
            options=data["options"]
            await self.save_timetable(options)
            message=await self.get_timetable(self.farm)
            message={'timetable':json.loads(message)}
            is_broadcast=True
        elif action=="executors":
            message={"executors":data["options"]}
            is_broadcast=True
        elif action=="executor_state":
            if not self.is_farm:
                message={'error':'not enough rights to perform this action'}
            else:
                message={"executor_state":data["options"]}
                is_broadcast=True
        else:
            message={'error':'failed request'}
        if is_broadcast:
            await self.channel_layer.group_send(self.farm_id, {'type':'broadcast','message':message})
        else:
            # print(message)
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
        except:
            return json.dumps([])
    
    @database_sync_to_async
    def get_timetable(self, farm):
        try:
            tm=Timetable.objects.filter(farm=farm.pk)
            tm=serialize('json',tm)
            return tm
        except:
            return json.dumps([])

    @database_sync_to_async
    def save_statistic(self, farm, sensors):
        try:
            sensors["farm_id"]=self.farm.pk
            st=Statistic.objects.create(**sensors)
            st.save()
            return True
        except:
            return False
    
    @database_sync_to_async
    def save_timetable(self, timetable):
        delete=Timetable.objects.filter(farm=self.farm.pk)
        for i in timetable:
            if timetable[i]["action"]=="delete":
                delete.get(date=dt.strptime(i,"%d.%m.%Y")).delete()
            elif timetable[i]["action"]=="change" and timetable[i]["data"]:
                timetable[i]["data"]['farm_id']=self.farm.pk
                timetable[i]["data"]['date']=dt.strptime(timetable[i]["data"]['date'],"%d.%m.%Y")
                try:
                    change=Timetable.objects.create(**timetable[i]["data"])
                    change.save()
                except:
                    Timetable.objects.filter(farm=self.farm.pk).filter(date=timetable[i]["data"]['date']).update(**timetable[i]["data"])

            




def isOnline(fid:str):
    status=r.hget('farms',fid)
    if status!=None and status.decode()=='true':
        return True
    return False