from django.urls import path
from . import views

app_name = 'meteo_app'

urlpatterns = [
    path('search', views.meteo_request_view),
]