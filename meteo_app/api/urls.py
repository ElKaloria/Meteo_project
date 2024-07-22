from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'meteo_app'


urlpatterns = [
    path('', views.CityHistory.as_view(), name='city_history'),
]