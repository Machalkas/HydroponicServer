from django.urls import path
from .views import farmRegistration, getFarms, farmAuthorization, websocketDebug

urlpatterns=[
    path('debug/', websocketDebug),
    path('api/farm-registration/', farmRegistration.as_view()),
    path('api/farm-authorization/', farmAuthorization.as_view()),
    path('api/get-farms/', getFarms.as_view()),
]