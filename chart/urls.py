from django.urls import path
from chart import views

app_name = "chart"
urlpatterns = [
    path('genre_view/', views.genre_distribution_view, name='genre_chart'),
    path('pop_genre_chart/', views.pop_chart_view, name='pop_chart'),
]