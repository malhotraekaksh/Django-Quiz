from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('questions/', views.questions, name='questions'),
]
