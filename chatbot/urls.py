from django.urls import path
from . import views

urlpatterns = [
    path('webhook', views.index, name="index"), 
]
