from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('add-question/', views.add_question, name='add_question'),

    path('view-questions/', views.view_questions, name='view_questions'),

    path('start/', views.start_quiz, name='start_quiz'),

    path('quiz/', views.questions, name='questions'),
]
