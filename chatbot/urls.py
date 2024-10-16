from django.urls import path, include
from chatbot import views

app_name = "chatbot"
urlpatterns = [
    path('window/', views.window_view, name='window'),
    path('api/', views.answer_view, name='answer'),
]
