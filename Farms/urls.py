from django.urls import path
from .views import farmRegistration, getFarms

urlpatterns=[
    path('farm-registration/', farmRegistration.as_view()),
    path('get-farms/', getFarms.as_view()),
]