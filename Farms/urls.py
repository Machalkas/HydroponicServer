from django.urls import path
from .views import farmRegistration

urlpatterns=[
    path('farm-registration/', farmRegistration.as_view()),
]