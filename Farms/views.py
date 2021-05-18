from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import response
from rest_framework.serializers import Serializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Farm
from stringGenerator import generateUnicque
from .serializers import FarmsSerializer

@login_required
def websocketDebug(self):
    return render(self, 'Farms/websocket_debug.html')

class farmRegistration(APIView):
    def post(self, request):
        u=authenticate(email=request.POST.get("email"), password=request.POST.get("password"))
        if u is None:
            return Response(data={"error":"Пользователь не найден"}, status=400)
        p=False
        n=request.POST.get("name")
        p=request.POST.get("is_public")
        t=generateUnicque(Farm, "token",size=100)
        params={'user':u, 'token':t, "is_public":bool(p)}
        if n is not None:
            params['name']=n
        f=Farm.objects.create(**params)
        f.save()
        return Response(data={"token":f.token}, status=201)

class farmAuthorization(APIView):
    def post(self, request):
        u=authenticate(email=request.POST.get("email"), password=request.POST.get("password"))  
        if u is None:
            return Response(data={"error":"Пользователь не найден"}, status=400)
        n=request.POST.get("name")
        if n is None:
            return Response({'error':'Название фермы обязательноеполе'},status=400)
        try:
            f=Farm.objects.get(user=u, name=n)
        except:
            return Response({'error':'Ферма с именем '+n+' не найдена'})
        f.token=generateUnicque(Farm, "token",size=100)
        f.save()
        return Response(data={"token":f.token}, status=200)

class getFarms(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        f=Farm.objects.filter(user=request.user)
        serializer=FarmsSerializer(f, many=True)
        return Response({'farms':serializer.data})
