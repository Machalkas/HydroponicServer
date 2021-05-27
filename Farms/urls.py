from django.urls import path
# from .views import farmRegistration, getFarms, farmAuthorization, websocketDebug
from . import views

urlpatterns=[
    path('', views.index, name="MainPage"),
    path('debug/', views.websocketDebug),
    path('api/farm-registration/', views.farmRegistration.as_view()),
    path('api/farm-authorization/', views.farmAuthorization.as_view()),
    path('api/get-farms/', views.getFarms.as_view()),
]