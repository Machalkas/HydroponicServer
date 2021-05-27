from django.urls import path
# from .views import farmRegistration, getFarms, farmAuthorization, websocketDebug
from . import views

urlpatterns=[
    path('autch', views.auth, name="Autch"),
]