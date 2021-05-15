from rest_framework import serializers

from .models import Farm

class FarmsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Farm
        exclude=['user','token']