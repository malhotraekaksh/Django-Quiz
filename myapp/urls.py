from django.urls import path
from . import views

urlpatterns = [
    path('', views.questions, name='questions'),
    path('add-question/', views.add_question, name='add_question'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('upload/', views.upload_questions, name='upload_questions'),
]
