from django.urls import path
from .views import farmRegistration, getFarms, farmAuthorization

urlpatterns=[
    path('farm-registration/', farmRegistration.as_view()),
    path('farm-authorization/', farmAuthorization.as_view()),
    path('get-farms/', getFarms.as_view()),
]