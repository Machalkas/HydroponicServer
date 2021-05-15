from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Farm
from Users.models import User
from stringGenerator import generateUnicque

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
        
