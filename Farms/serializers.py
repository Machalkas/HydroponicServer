import redis
from rest_framework import serializers

from .models import Farm

r = redis.Redis(host='localhost', port=6379, db=1)

class FarmsSerializer(serializers.ModelSerializer):
    is_online=serializers.SerializerMethodField(method_name='view_online')
    class Meta:
        model=Farm
        exclude=['user','token']
    
    def view_online(self, obj):
        status=r.hget('farms', obj.id)
        if status!=None and status.decode()=='true':
            return True
        return False