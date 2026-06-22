from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),   # 👈 HOME = dashboard

    path('dashboard/', views.dashboard, name='dashboard'),

    path('add-question/', views.add_question, name='add_question'),

    path('start/', views.start_quiz, name='start_quiz'),

    path('quiz/', views.questions, name='questions'),
]
