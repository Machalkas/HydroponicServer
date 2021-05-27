from django.shortcuts import render
import requests

# Create your views here.

def auth(request):
    return render(request ,"Users/autch.html")
